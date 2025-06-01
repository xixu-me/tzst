"""Core functionality for tzst archives."""

import io
import os
import tarfile
import tempfile
import time
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import BinaryIO

import zstandard as zstd

from .exceptions import TzstArchiveError, TzstDecompressionError


class TzstArchive:
    """A class for handling .tzst/.tar.zst archives."""

    def __init__(
        self,
        filename: str | Path,
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
        self._tarfile: tarfile.TarFile | None = None
        self._fileobj: BinaryIO | None = None
        self._compressed_stream: (
            zstd.ZstdCompressionWriter
            | zstd.ZstdDecompressionReader
            | io.BytesIO
            | None
        ) = None

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
        """Open the archive.

        See Also:
            :meth:`close`: Method to close the archive
        """
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
        name: str | Path,
        arcname: str | None = None,
        recursive: bool = True,
    ):
        """
        Add a file or directory to the archive.

        Args:
            name: Path to file or directory to add
            arcname: Alternative name for the file in the archive
            recursive: If True, add directories recursively

        See Also:
            :func:`create_archive`: Convenience function for creating archives
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
        member: str | None = None,
        path: str | Path = ".",
        set_attrs: bool = True,
        numeric_owner: bool = False,
        filter: str | Callable | None = "data",
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

        See Also:
            :func:`extract_archive`: Convenience function for extracting archives
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

        # Prepare extraction arguments - filters are always supported in Python 3.12+
        extract_kwargs = {"filter": filter}

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

    def extractfile(self, member: str | tarfile.TarInfo):
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

    def getmembers(self) -> list[tarfile.TarInfo]:
        """Get list of all members in the archive."""
        if not self._tarfile:
            raise RuntimeError("Archive not open")
        if not self.mode.startswith("r"):
            raise RuntimeError("Archive not open for reading")

        return self._tarfile.getmembers()

    def getnames(self) -> list[str]:
        """Get list of all member names in the archive."""
        if not self._tarfile:
            raise RuntimeError("Archive not open")
        if not self.mode.startswith("r"):
            raise RuntimeError("Archive not open for reading")

        return self._tarfile.getnames()

    def list(self, verbose: bool = False) -> list[dict]:
        """
        List contents of the archive.

        Args:
            verbose: Include detailed information

        Returns:
            List of file information dictionaries

        See Also:
            :meth:`getmembers`: Get TarInfo objects for all archive members
            :meth:`getnames`: Get names of all archive members
            :func:`list_archive`: Convenience function for listing archives
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

        See Also:
            :func:`test_archive`: Convenience function for testing archive integrity
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
    archive_path: str | Path,
    files: Sequence[str | Path],
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

    See Also:
        :meth:`TzstArchive.add`: Method for adding files to an open archive
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
    files: Sequence[str | Path],
    compression_level: int,
) -> None:
    """Internal implementation for creating archives."""
    # Find common parent directory for relative paths
    if files:
        file_paths = [Path(f) for f in files if Path(f).exists()]
        if file_paths:  # Special handling for current directory "."
            current_dir = Path.cwd().resolve()
            if len(file_paths) == 1 and (
                str(file_paths[0]) == "." or file_paths[0].resolve() == current_dir
            ):  # When adding current directory, add its contents without "./" prefix
                with TzstArchive(archive_path, "w", compression_level) as archive:
                    # Add all items in current directory, excluding archive and temp files
                    archive_abs_path = archive_path.resolve()
                    archive_name = archive_path.name
                    for item in Path(".").iterdir():
                        item_abs_path = item.resolve()
                        # Skip archives and temp files for consistency
                        if (
                            item_abs_path == archive_abs_path
                            or item.name == archive_name
                            or (
                                item.name.startswith(".") and item.name.endswith(".tmp")
                            )
                            or item.suffix.lower() in [".tzst", ".zst"]
                            or item.name.lower().endswith(".tar.zst")
                        ):
                            continue
                        # Use item name as archive name to avoid "./" prefix
                        item_name = str(item.name).replace("\\", "/")
                        archive.add(str(item), arcname=item_name)
            else:
                # Find the common parent directory
                try:
                    common_parent = Path(
                        os.path.commonpath([p.parent for p in file_paths])
                    )
                except ValueError:
                    # No common path, use parent of first file
                    common_parent = file_paths[
                        0
                    ].parent  # Change to common parent directory to get relative paths
                original_cwd = Path.cwd()
                # Convert archive path to absolute to avoid issues when changing working directory
                absolute_archive_path = archive_path.resolve()
                try:
                    os.chdir(common_parent)
                    with TzstArchive(
                        absolute_archive_path, "w", compression_level
                    ) as archive:
                        for file_path in file_paths:
                            # Calculate relative path from common parent
                            relative_path = file_path.relative_to(common_parent)
                            # Normalize path separators and remove Windows prefixes
                            path_str = str(relative_path).replace("\\", "/")
                            if path_str.startswith("./") or path_str.startswith(".\\"):
                                path_str = path_str[2:]
                            # Use arcname to control the name in the archive
                            archive.add(str(relative_path), arcname=path_str)
                finally:
                    os.chdir(original_cwd)
        else:
            raise FileNotFoundError("No valid files found")
    else:
        # Empty archive
        with TzstArchive(archive_path, "w", compression_level) as archive:
            pass


def extract_archive(
    archive_path: str | Path,
    extract_path: str | Path = ".",
    members: list[str] | None = None,
    flatten: bool = False,
    streaming: bool = False,
    filter: str | Callable | None = "data",
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

    See Also:
        :meth:`TzstArchive.extract`: Method for extracting from an open archive
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
    archive_path: str | Path, verbose: bool = False, streaming: bool = False
) -> list[dict]:
    """
    List contents of a .tzst archive.

    Args:
        archive_path: Path to the archive
        verbose: Include detailed information
        streaming: If True, use streaming mode (memory efficient for large archives)

    Returns:
        List of file information dictionaries

    See Also:
        :meth:`TzstArchive.list`: Method for listing an open archive
    """
    with TzstArchive(archive_path, "r", streaming=streaming) as archive:
        return archive.list(verbose=verbose)


def test_archive(archive_path: str | Path, streaming: bool = False) -> bool:
    """
    Test the integrity of a .tzst archive.

    Args:
        archive_path: Path to the archive
        streaming: If True, use streaming mode (memory efficient for large archives)

    Returns:
        True if archive is valid, False otherwise

    See Also:
        :meth:`TzstArchive.test`: Method for testing an open archive
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
