"""Core functionality for tzst archives."""

import io
import os
import stat
import tarfile
import tempfile
import time
from pathlib import Path
from typing import BinaryIO, Callable, List, Optional, Sequence, Union

import zstandard as zstd

from .exceptions import TzstArchiveError, TzstDecompressionError

# Check if extraction filters are supported (Python 3.12+)
EXTRACTION_FILTERS_SUPPORTED = hasattr(tarfile, "data_filter")


# Custom exception classes for older Python versions
class _FilterError(Exception):
    """Base class for filter errors in older Python versions."""

    def __init__(self, member):
        self.tarinfo = member
        super().__init__(f"Filter error for member: {member.name}")


class _AbsolutePathError(_FilterError):
    """Raised when a member has an absolute path."""

    pass


class _OutsideDestinationError(_FilterError):
    """Raised when a member would be extracted outside destination."""

    pass


class _SpecialFileError(_FilterError):
    """Raised when a member is a special file (device, pipe, etc.)."""

    pass


class _AbsoluteLinkError(_FilterError):
    """Raised when a link has an absolute path."""

    pass


class _LinkOutsideDestinationError(_FilterError):
    """Raised when a link points outside destination."""

    pass


# Use built-in exceptions if available, otherwise use custom ones
if EXTRACTION_FILTERS_SUPPORTED:
    AbsolutePathError = tarfile.AbsolutePathError
    OutsideDestinationError = tarfile.OutsideDestinationError
    SpecialFileError = tarfile.SpecialFileError
    AbsoluteLinkError = tarfile.AbsoluteLinkError
    LinkOutsideDestinationError = tarfile.LinkOutsideDestinationError
else:
    AbsolutePathError = _AbsolutePathError
    OutsideDestinationError = _OutsideDestinationError
    SpecialFileError = _SpecialFileError
    AbsoluteLinkError = _AbsoluteLinkError
    LinkOutsideDestinationError = _LinkOutsideDestinationError


# Backward compatibility: Custom filter implementations for Python < 3.12
def _is_within_directory(directory: str, target: str) -> bool:
    """Check if target path is within directory (prevents path traversal)."""
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)
    return os.path.commonpath([abs_directory, abs_target]) == abs_directory


def _fully_trusted_filter(member: tarfile.TarInfo, path: str) -> tarfile.TarInfo:
    """
    Backward compatibility implementation of fully_trusted_filter.
    Return member unchanged - no security filtering.
    """
    return member


def _tar_filter(member: tarfile.TarInfo, path: str) -> tarfile.TarInfo:
    """
    Backward compatibility implementation of tar_filter.

    Implements the 'tar' filter security policy:
    - Strip leading slashes from filenames
    - Refuse to extract files with absolute paths
    - Refuse to extract files outside destination
    - Clear high mode bits (setuid, setgid, sticky) and group/other write bits
    """
    # Create a copy to avoid modifying the original
    member = member.replace()

    # Strip leading slashes and path separators
    member.name = member.name.lstrip("/" + os.sep)
    if member.linkname:
        member.linkname = member.linkname.lstrip("/" + os.sep)

    # Check for absolute paths (even after stripping slashes)
    if os.path.isabs(member.name):
        raise AbsolutePathError(member)
    if member.linkname and os.path.isabs(member.linkname):
        raise AbsoluteLinkError(member)

    # Check if extraction would end up outside destination
    target_path = os.path.join(path, member.name)
    if not _is_within_directory(path, target_path):
        raise OutsideDestinationError(member)

    # For symbolic/hard links, check link target
    if member.islnk() or member.issym():
        if member.linkname:
            if os.path.isabs(member.linkname):
                raise AbsoluteLinkError(member)
            # Check if link target would be outside destination
            link_target = os.path.join(path, member.linkname)
            if not _is_within_directory(path, link_target):
                raise LinkOutsideDestinationError(member)

    # Clear dangerous mode bits if mode is set
    if member.mode is not None:
        # Clear setuid, setgid, sticky bits
        member.mode &= ~(stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX)
        # Clear group/other write permissions
        member.mode &= ~(stat.S_IWGRP | stat.S_IWOTH)

    return member


def _data_filter(member: tarfile.TarInfo, path: str) -> tarfile.TarInfo:
    """
    Backward compatibility implementation of data_filter.

    Implements the 'data' filter security policy (most restrictive):
    - All tar_filter restrictions
    - Refuse to extract device files (including pipes)
    - Refuse to extract links with absolute paths or pointing outside destination
    - Set safe permissions for regular files
    - Clear user/group info for security
    """
    # First apply tar_filter restrictions
    member = _tar_filter(member, path)

    # Refuse device files and pipes
    if member.ischr() or member.isblk() or member.isfifo():
        raise SpecialFileError(member)

    # Refuse links (both symbolic and hard) that are problematic
    if member.islnk() or member.issym():
        if member.linkname:
            # Refuse absolute link paths
            if os.path.isabs(member.linkname):
                raise AbsoluteLinkError(member)
            # Refuse links pointing outside destination
            link_target = os.path.join(path, member.linkname)
            if not _is_within_directory(path, link_target):
                raise LinkOutsideDestinationError(member)

    # Set safe permissions for regular files and hard links
    if member.isfile() or member.islnk():
        if member.mode is not None:
            # Set owner read and write permissions
            member.mode |= stat.S_IRUSR | stat.S_IWUSR
            # Remove group & other executable if owner doesn't have it
            if not (member.mode & stat.S_IXUSR):
                member.mode &= ~(stat.S_IXGRP | stat.S_IXOTH)
    else:
        # For directories and other files, set mode to 0o755 (safe default)
        # We can't set to None in older Python versions
        member.mode = 0o755

    # Clear user and group info for security (set to safe defaults)
    # We can't set to None in older Python versions
    member.uid = 0
    member.gid = 0
    member.uname = "root"
    member.gname = "root"

    return member


# Map filter names to functions for backward compatibility
_FILTER_FUNCTIONS = {
    "fully_trusted": _fully_trusted_filter,
    "tar": _tar_filter,
    "data": _data_filter,
}


def _get_filter_function(
    filter_arg: Optional[Union[str, Callable]],
) -> Optional[Union[str, Callable]]:
    """
    Get the appropriate filter function for the given filter argument.

    Returns:
        - Built-in filter string if Python 3.12+ and filter is a string
        - Custom filter function if Python < 3.12 and filter is a string
        - The filter itself if it's a callable
        - None if filter is None
    """
    if filter_arg is None:
        return None

    if callable(filter_arg):
        return filter_arg

    if isinstance(filter_arg, str):
        if EXTRACTION_FILTERS_SUPPORTED:
            # Use built-in filters for Python 3.12+
            return filter_arg
        else:
            # Use custom filters for Python < 3.12
            if filter_arg in _FILTER_FUNCTIONS:
                return _FILTER_FUNCTIONS[filter_arg]
            else:
                raise ValueError(f"Unknown filter: {filter_arg}")

    raise TypeError(f"Filter must be None, string, or callable, got {type(filter_arg)}")


class TzstArchive:
    """A class for handling .tzst/.tar.zst archives."""

    def __init__(
        self,
        filename: Union[str, Path],
        mode: str = "r",
        compression_level: int = 3,
        streaming: bool = False,
    ):
        """
        Initialize a TzstArchive.

        Args:
            filename: Path to the archive file
            mode: Open mode ('r', 'w', 'a')
            compression_level: Zstandard compression level (1-22)
            streaming: If True, use streaming mode for reading (reduces memory usage
                      for very large archives but may limit some tarfile operations
                      that require seeking. Recommended for archives > 100MB)
        """
        self.filename = Path(filename)
        self.mode = mode
        self.compression_level = compression_level
        self.streaming = streaming
        self._tarfile: Optional[tarfile.TarFile] = None
        self._fileobj: Optional[BinaryIO] = None
        self._compressed_stream: Optional[
            Union[zstd.ZstdCompressionWriter, zstd.ZstdDecompressionReader, io.BytesIO]
        ] = None

        # Validate mode
        valid_modes = ["r", "w", "a"]
        if mode not in valid_modes:
            raise ValueError(
                f"Invalid mode '{mode}'. Must be one of: {', '.join(valid_modes)}"
            )

        # Validate compression level
        if not 1 <= compression_level <= 22:
            raise ValueError(
                f"Invalid compression level '{compression_level}'. Must be between 1 and 22."
            )

        # Check for unsupported modes immediately - provide clear documentation
        if mode.startswith("a"):
            raise NotImplementedError(
                "Append mode is not currently supported for .tzst/.tar.zst archives. "
                "This would require decompressing the entire archive, adding new files, "
                "and recompressing, which is complex and potentially slow for large archives. "
                "Alternatives: 1) Create multiple archives, 2) Recreate the archive with all files, "
                "3) Use standard tar format for append operations, then compress separately."
            )

    def __enter__(self):
        """Enter context manager."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        self.close()

    def open(self):
        """Open the archive."""
        try:
            if self.mode.startswith("r"):
                # Read mode
                self._fileobj = open(self.filename, "rb")
                dctx = zstd.ZstdDecompressor()

                if self.streaming:
                    # Streaming mode - use stream reader directly (memory efficient)
                    # Note: This may limit some tarfile operations that require seeking
                    self._compressed_stream = dctx.stream_reader(self._fileobj)
                    self._tarfile = tarfile.open(
                        fileobj=self._compressed_stream, mode="r|"
                    )
                else:
                    # Buffer mode - decompress to memory buffer for random access
                    # Better compatibility but higher memory usage for large archives
                    decompressed_chunks = []
                    with dctx.stream_reader(self._fileobj) as reader:
                        while True:
                            chunk = reader.read(8192)
                            if not chunk:
                                break
                            decompressed_chunks.append(chunk)
                    decompressed_data = b"".join(decompressed_chunks)
                    self._compressed_stream = io.BytesIO(decompressed_data)
                    self._tarfile = tarfile.open(
                        fileobj=self._compressed_stream, mode="r"
                    )

            elif self.mode.startswith("w"):
                # Write mode - use streaming compression
                self._fileobj = open(self.filename, "wb")
                cctx = zstd.ZstdCompressor(
                    level=self.compression_level, write_content_size=True
                )
                self._compressed_stream = cctx.stream_writer(self._fileobj)
                self._tarfile = tarfile.open(fileobj=self._compressed_stream, mode="w|")
            elif self.mode.startswith("a"):
                # Append mode - for tar.zst, this is complex as we need to decompress,
                # add files, and recompress. For simplicity, we'll raise an error for now.
                raise NotImplementedError(
                    "Append mode is not currently supported for .tzst/.tar.zst archives. "
                    "This would require decompressing the entire archive, adding new files, "
                    "and recompressing, which is complex and potentially slow for large archives. "
                    "Alternatives: 1) Create multiple archives, 2) Recreate the archive with all files, "
                    "3) Use standard tar format for append operations, then compress separately."
                )
            else:
                raise ValueError(f"Invalid mode: {self.mode}")
        except Exception as e:
            self.close()
            if "zstd" in str(e).lower():
                raise TzstDecompressionError(f"Failed to open archive: {e}") from e
            else:
                raise TzstArchiveError(f"Failed to open archive: {e}") from e

    def close(self):
        """Close the archive."""
        if self._tarfile:
            try:
                self._tarfile.close()
            except Exception:
                pass
            self._tarfile = None

        if self._compressed_stream:
            try:
                self._compressed_stream.close()
            except Exception:
                pass
            self._compressed_stream = None

        if self._fileobj:
            try:
                self._fileobj.close()
            except Exception:
                pass
            self._fileobj = None

    def add(
        self,
        name: Union[str, Path],
        arcname: Optional[str] = None,
        recursive: bool = True,
    ):
        """
        Add a file or directory to the archive.

        Args:
            name: Path to file or directory to add
            arcname: Alternative name for the file in the archive
            recursive: If True, add directories recursively
        """
        if not self._tarfile:
            raise RuntimeError("Archive not open")
        if not self.mode.startswith("w"):
            raise RuntimeError("Archive not open for writing")

        path = Path(name)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {name}")

        self._tarfile.add(str(path), arcname=arcname, recursive=recursive)

    def extract(
        self,
        member: Optional[str] = None,
        path: Union[str, Path] = ".",
        set_attrs: bool = True,
        numeric_owner: bool = False,
        filter: Optional[Union[str, Callable]] = "data",
    ):
        """
        Extract files from the archive.

        Args:
            member: Specific member to extract (None for all)
            path: Destination directory
            set_attrs: Whether to set file attributes
            numeric_owner: Whether to use numeric owner
            filter: Extraction filter for security. Can be:
                   - 'data': Safe filter for cross-platform data archives (default, recommended)
                   - 'tar': Honor most tar features but block dangerous ones
                   - 'fully_trusted': Honor all metadata (use only for trusted archives)
                   - None: Use default behavior (may show deprecation warning in Python 3.12+)
                   - callable: Custom filter function

        Warning:
            Never extract archives from untrusted sources without proper filtering.
            The 'data' filter is recommended for most use cases as it prevents
            dangerous security issues like path traversal attacks.

        Note:
            In streaming mode, extracting specific members is not supported.
            Some extraction operations may be limited due to the sequential
            nature of streaming mode.
        """
        if not self._tarfile:
            raise RuntimeError("Archive not open")
        if not self.mode.startswith("r"):
            raise RuntimeError("Archive not open for reading")

        extract_path = Path(path)
        extract_path.mkdir(parents=True, exist_ok=True)

        if self.streaming and member:
            # Specific member extraction not supported in streaming mode
            raise RuntimeError(
                "Extracting specific members is not supported in streaming mode. "
                "Please use non-streaming mode for selective extraction, or extract all files."
            )

        # Prepare extraction arguments
        extract_kwargs = {}

        # Add filter argument if supported (Python 3.12+)
        if EXTRACTION_FILTERS_SUPPORTED:
            extract_kwargs["filter"] = filter
        elif filter is not None and filter != "data":
            # Warn if user specified a filter but it's not supported
            print(
                "Warning: Extraction filters are not supported in this Python version. "
                "Consider upgrading to Python 3.12+ for enhanced security features.",
            )
        else:
            # Use backward-compatible filter for Python < 3.12
            filter_function = _get_filter_function(filter)
            extract_kwargs["filter"] = filter_function

        try:
            if member:
                self._tarfile.extract(member, path=extract_path, **extract_kwargs)
            else:
                self._tarfile.extractall(path=extract_path, **extract_kwargs)
        except (tarfile.StreamError, OSError) as e:
            if self.streaming and (
                "seeking" in str(e).lower() or "stream" in str(e).lower()
            ):
                raise RuntimeError(
                    "Extraction failed in streaming mode due to archive structure limitations. "
                    "This archive may require non-streaming mode for extraction. "
                    f"Original error: {e}"
                ) from e
            else:
                raise

    def extractfile(self, member: Union[str, tarfile.TarInfo]):
        """
        Extract a file-like object from the archive.

        Args:
            member: Member name or TarInfo object

        Returns:
            File-like object or None if member is not a file
        """
        if not self._tarfile:
            raise RuntimeError("Archive not open")
        if not self.mode.startswith("r"):
            raise RuntimeError("Archive not open for reading")

        return self._tarfile.extractfile(member)

    def getmembers(self) -> List[tarfile.TarInfo]:
        """Get list of all members in the archive."""
        if not self._tarfile:
            raise RuntimeError("Archive not open")
        if not self.mode.startswith("r"):
            raise RuntimeError("Archive not open for reading")

        return self._tarfile.getmembers()

    def getnames(self) -> List[str]:
        """Get list of all member names in the archive."""
        if not self._tarfile:
            raise RuntimeError("Archive not open")
        if not self.mode.startswith("r"):
            raise RuntimeError("Archive not open for reading")

        return self._tarfile.getnames()

    def list(self, verbose: bool = False) -> List[dict]:
        """
        List contents of the archive.

        Args:
            verbose: Include detailed information

        Returns:
            List of file information dictionaries
        """
        if not self._tarfile:
            raise RuntimeError("Archive not open")
        if not self.mode.startswith("r"):
            raise RuntimeError("Archive not open for reading")

        members = self.getmembers()
        result = []

        for member in members:
            info = {
                "name": member.name,
                "size": member.size,
                "is_file": member.isfile(),
                "is_dir": member.isdir(),
                "is_link": member.islnk(),
                "is_symlink": member.issym(),
            }

            if verbose:
                info.update(
                    {
                        "mode": member.mode,
                        "uid": member.uid,
                        "gid": member.gid,
                        "mtime": member.mtime,
                        "mtime_str": time.strftime(
                            "%Y-%m-%d %H:%M:%S", time.localtime(member.mtime)
                        ),
                        "linkname": member.linkname,
                        "uname": member.uname,
                        "gname": member.gname,
                    }
                )

            result.append(info)

        return result

    def test(self) -> bool:
        """
        Test the integrity of the archive.

        Returns:
            True if archive is valid, False otherwise
        """
        if not self._tarfile:
            raise RuntimeError("Archive not open")
        if not self.mode.startswith("r"):
            raise RuntimeError("Archive not open for reading")

        try:
            # Try to iterate through all members and read file contents
            for member in self.getmembers():
                if member.isfile():
                    # Try to extract each file to verify integrity
                    fileobj = self.extractfile(member)
                    if fileobj:
                        # Read the entire file to verify decompression
                        while True:
                            chunk = fileobj.read(8192)
                            if not chunk:
                                break
            return True
        except Exception:
            return False


# Convenience functions


def create_archive(
    archive_path: Union[str, Path],
    files: Sequence[Union[str, Path]],
    compression_level: int = 3,
    use_temp_file: bool = True,
) -> None:
    """
    Create a new .tzst archive with atomic file operations.

    Args:
        archive_path: Path for the new archive
        files: List of files/directories to add
        compression_level: Zstandard compression level (1-22)
        use_temp_file: If True, create archive in temporary file first, then move
                      to final location for atomic operation
    """
    # Validate compression level
    if not 1 <= compression_level <= 22:
        raise ValueError(
            f"Invalid compression level '{compression_level}'. Must be between 1 and 22."
        )

    archive_path = Path(archive_path)

    # Ensure archive has correct extension
    if archive_path.suffix.lower() not in [".tzst", ".zst"]:
        if archive_path.suffix.lower() == ".tar":
            archive_path = archive_path.with_suffix(".tar.zst")
        else:
            archive_path = archive_path.with_suffix(archive_path.suffix + ".tzst")

    # Use temporary file for atomic operation if requested
    if use_temp_file:
        temp_fd = None
        temp_path = None
        try:
            # Create temporary file in same directory as target for atomic move
            temp_fd, temp_path_str = tempfile.mkstemp(
                suffix=".tmp", prefix=f".{archive_path.name}.", dir=archive_path.parent
            )
            os.close(temp_fd)  # Close file descriptor, we'll open with TzstArchive
            temp_path = Path(temp_path_str)

            # Create archive in temporary location
            _create_archive_impl(temp_path, files, compression_level)

            # Atomic move to final location
            temp_path.replace(archive_path)

        except Exception:
            # Clean up temporary file on error
            if temp_path and temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception:
                    pass
            raise
    else:
        # Direct creation (non-atomic)
        _create_archive_impl(archive_path, files, compression_level)


def _create_archive_impl(
    archive_path: Path,
    files: Sequence[Union[str, Path]],
    compression_level: int,
) -> None:
    """Internal implementation for creating archives."""
    # Find common parent directory for relative paths
    if files:
        file_paths = [Path(f) for f in files if Path(f).exists()]
        if file_paths:
            # Find the common parent directory
            try:
                common_parent = Path(os.path.commonpath([p.parent for p in file_paths]))
            except ValueError:
                # No common path, use parent of first file
                common_parent = file_paths[0].parent

            # Change to common parent directory to get relative paths
            original_cwd = Path.cwd()
            try:
                os.chdir(common_parent)
                with TzstArchive(archive_path, "w", compression_level) as archive:
                    for file_path in file_paths:
                        # Calculate relative path from common parent
                        relative_path = file_path.relative_to(common_parent)
                        archive.add(str(relative_path))
            finally:
                os.chdir(original_cwd)
        else:
            raise FileNotFoundError("No valid files found")
    else:
        # Empty archive
        with TzstArchive(archive_path, "w", compression_level) as archive:
            pass


def extract_archive(
    archive_path: Union[str, Path],
    extract_path: Union[str, Path] = ".",
    members: Optional[List[str]] = None,
    flatten: bool = False,
    streaming: bool = False,
    filter: Optional[Union[str, Callable]] = "data",
) -> None:
    """
    Extract files from a .tzst archive.

    Args:
        archive_path: Path to the archive
        extract_path: Destination directory
        members: Specific members to extract (None for all)
        flatten: If True, extract without directory structure
        streaming: If True, use streaming mode (memory efficient for large archives)
        filter: Extraction filter for security. Can be:
               - 'data': Safe filter for cross-platform data archives (default, recommended)
               - 'tar': Honor most tar features but block dangerous ones
               - 'fully_trusted': Honor all metadata (use only for trusted archives)
               - None: Use default behavior (may show deprecation warning in Python 3.12+)
               - callable: Custom filter function

    Warning:
        Never extract archives from untrusted sources without proper filtering.
        The 'data' filter is recommended for most use cases as it prevents
        dangerous security issues like path traversal attacks.
    """
    with TzstArchive(archive_path, "r", streaming=streaming) as archive:
        if flatten:
            # Extract files without directory structure
            extract_dir = Path(extract_path)
            extract_dir.mkdir(parents=True, exist_ok=True)

            if members:
                member_list = [m for m in archive.getmembers() if m.name in members]
            else:
                member_list = archive.getmembers()

            for member in member_list:
                if member.isfile():
                    # Extract to flat directory
                    filename = Path(member.name).name
                    fileobj = archive.extractfile(member)
                    if fileobj:
                        with open(extract_dir / filename, "wb") as f:
                            f.write(fileobj.read())
        else:
            # Extract with full directory structure
            if members:
                for member in members:
                    archive.extract(member, extract_path, filter=filter)
            else:
                archive.extract(path=extract_path, filter=filter)


def list_archive(
    archive_path: Union[str, Path], verbose: bool = False, streaming: bool = False
) -> List[dict]:
    """
    List contents of a .tzst archive.

    Args:
        archive_path: Path to the archive
        verbose: Include detailed information
        streaming: If True, use streaming mode (memory efficient for large archives)

    Returns:
        List of file information dictionaries
    """
    with TzstArchive(archive_path, "r", streaming=streaming) as archive:
        return archive.list(verbose=verbose)


def test_archive(archive_path: Union[str, Path], streaming: bool = False) -> bool:
    """
    Test the integrity of a .tzst archive.

    Args:
        archive_path: Path to the archive
        streaming: If True, use streaming mode (memory efficient for large archives)

    Returns:
        True if archive is valid, False otherwise
    """
    try:
        # Open a fresh archive instance for testing
        with TzstArchive(archive_path, "r", streaming=streaming) as archive:
            # Try to iterate through all members and read file contents
            for member in archive.getmembers():
                if member.isfile():
                    # In streaming mode, extractfile may not work properly with r| mode
                    # So we'll just check that we can iterate through members
                    if streaming:
                        # For streaming mode, just verify we can read the member info
                        # This tests that the archive structure is valid
                        continue
                    else:
                        # Try to extract each file to verify integrity
                        fileobj = archive.extractfile(member)
                        if fileobj:
                            # Read the entire file to verify decompression
                            while True:
                                chunk = fileobj.read(8192)
                                if not chunk:
                                    break
            return True
    except Exception:
        return False
