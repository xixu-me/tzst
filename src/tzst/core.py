"""Core functionality for tzst archives."""

import io
import os
import tarfile
import time
from pathlib import Path
from typing import BinaryIO, List, Optional, Sequence, Union

import zstandard as zstd

from .exceptions import TzstArchiveError, TzstDecompressionError


class TzstArchive:
    """A class for handling .tzst/.tar.zst archives."""

    def __init__(
        self, filename: Union[str, Path], mode: str = "r", compression_level: int = 3
    ):
        """
        Initialize a TzstArchive.

        Args:
            filename: Path to the archive file
            mode: Open mode ('r', 'w', 'a')
            compression_level: Zstandard compression level (1-22)
        """
        self.filename = Path(filename)
        self.mode = mode
        self.compression_level = compression_level
        self._tarfile: Optional[tarfile.TarFile] = None
        self._fileobj: Optional[BinaryIO] = None
        self._compressed_stream: Optional[
            Union[zstd.ZstdCompressionWriter, zstd.ZstdDecompressionReader]
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

        # Check for unsupported modes immediately
        if mode.startswith("a"):
            raise NotImplementedError(
                "Append mode is not supported for compressed tar archives"
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
                # Read mode - decompress to memory buffer for random access
                self._fileobj = open(self.filename, "rb")
                dctx = zstd.ZstdDecompressor()
                # Use streaming decompression to handle archives without content size
                decompressed_chunks = []
                with dctx.stream_reader(self._fileobj) as reader:
                    while True:
                        chunk = reader.read(8192)
                        if not chunk:
                            break
                        decompressed_chunks.append(chunk)
                decompressed_data = b"".join(decompressed_chunks)
                self._compressed_stream = io.BytesIO(decompressed_data)
                self._tarfile = tarfile.open(fileobj=self._compressed_stream, mode="r")
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
                    "Append mode is not supported for compressed tar archives"
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
    ):
        """
        Extract files from the archive.

        Args:
            member: Specific member to extract (None for all)
            path: Destination directory
            set_attrs: Whether to set file attributes
            numeric_owner: Whether to use numeric owner
        """
        if not self._tarfile:
            raise RuntimeError("Archive not open")
        if not self.mode.startswith("r"):
            raise RuntimeError("Archive not open for reading")

        extract_path = Path(path)
        extract_path.mkdir(parents=True, exist_ok=True)

        if member:
            self._tarfile.extract(member, path=extract_path)
        else:
            self._tarfile.extractall(path=extract_path)

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
) -> None:
    """
    Create a new .tzst archive.

    Args:
        archive_path: Path for the new archive
        files: List of files/directories to add
        compression_level: Zstandard compression level (1-22)
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
) -> None:
    """
    Extract files from a .tzst archive.

    Args:
        archive_path: Path to the archive
        extract_path: Destination directory
        members: Specific members to extract (None for all)
        flatten: If True, extract without directory structure
    """
    with TzstArchive(archive_path, "r") as archive:
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
                    archive.extract(member, extract_path)
            else:
                archive.extract(path=extract_path)


def list_archive(archive_path: Union[str, Path], verbose: bool = False) -> List[dict]:
    """
    List contents of a .tzst archive.

    Args:
        archive_path: Path to the archive
        verbose: Include detailed information

    Returns:
        List of file information dictionaries
    """
    with TzstArchive(archive_path, "r") as archive:
        return archive.list(verbose=verbose)


def test_archive(archive_path: Union[str, Path]) -> bool:
    """
    Test the integrity of a .tzst archive.

    Args:
        archive_path: Path to the archive

    Returns:
        True if archive is valid, False otherwise
    """
    try:
        # Open a fresh archive instance for testing
        with TzstArchive(archive_path, "r") as archive:
            # Try to iterate through all members and read file contents
            for member in archive.getmembers():
                if member.isfile():
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
