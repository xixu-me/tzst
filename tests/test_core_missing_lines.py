"""Tests to cover missing lines in core.py for improved coverage."""

import tarfile
from unittest.mock import MagicMock, patch

import pytest

from tzst.core import TzstArchive
from tzst.exceptions import TzstArchiveError, TzstDecompressionError


class TestCoreMissingLines:
    """Test specific missing lines in core.py."""

    def test_append_mode_error_handling(self, temp_dir):
        """Test append mode error handling (lines 126-137)."""
        archive_path = temp_dir / "test.tzst"

        # Test append mode raises NotImplementedError
        with pytest.raises(
            NotImplementedError, match="Append mode is not currently supported"
        ):
            TzstArchive(archive_path, mode="a")

    def test_invalid_mode_error_after_open(self, temp_dir):
        """Test invalid mode error in __enter__ method (line 137)."""
        archive_path = temp_dir / "test.tzst"

        # Create archive instance with invalid mode after validation passes
        archive = TzstArchive.__new__(TzstArchive)
        archive.filename = archive_path
        archive.mode = "invalid"  # Set invalid mode after construction
        archive.compression_level = 3
        archive.streaming = False
        archive._tarfile = None
        archive._fileobj = None
        archive._compressed_stream = None

        with pytest.raises(TzstArchiveError, match="Failed to open archive"):
            archive.__enter__()

    def test_zstd_error_handling_in_open(self, temp_dir):
        """Test zstd error handling during archive opening (lines 133-137)."""
        archive_path = temp_dir / "test.tzst"

        # Create a file that will cause zstd decompression error
        archive_path.write_bytes(b"invalid zstd data")

        # Try to open as read mode - should raise TzstDecompressionError
        with pytest.raises(TzstDecompressionError, match="Failed to open archive"):
            with TzstArchive(archive_path, mode="r"):
                pass

    def test_generic_error_handling_in_open(self, temp_dir):
        """Test generic error handling during archive opening."""
        archive_path = temp_dir / "test.tzst"

        # Mock to raise a generic exception (not zstd-related)
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            with pytest.raises(TzstArchiveError, match="Failed to open archive"):
                with TzstArchive(archive_path, mode="r"):
                    pass

    def test_close_error_handling(self, temp_dir):
        """Test error handling in close method (lines 146-157)."""
        archive_path = temp_dir / "test.tzst"

        # Create archive and manually set objects that will raise on close
        with TzstArchive(archive_path, mode="w") as archive:
            pass

        # Now manually create problematic objects
        archive = TzstArchive.__new__(TzstArchive)
        archive._tarfile = MagicMock()
        archive._tarfile.close.side_effect = Exception("Close error")
        archive._compressed_stream = MagicMock()
        archive._compressed_stream.close.side_effect = Exception("Close error")
        archive._fileobj = MagicMock()
        archive._fileobj.close.side_effect = Exception("Close error")

        # close() should handle exceptions gracefully
        archive.close()  # Should not raise

        assert archive._tarfile is None
        assert archive._compressed_stream is None
        assert archive._fileobj is None

    def test_archive_not_open_for_reading_errors(self, temp_dir):
        """Test RuntimeError for operations on archives not open for reading (lines 186, 188, 192)."""
        archive_path = temp_dir / "test.tzst"

        # Create archive in write mode
        with TzstArchive(archive_path, mode="w") as archive:
            # Test getmembers() on write mode
            with pytest.raises(RuntimeError, match="Archive not open for reading"):
                archive.getmembers()

            # Test getnames() on write mode
            with pytest.raises(RuntimeError, match="Archive not open for reading"):
                archive.getnames()

            # Test extractfile() on write mode
            with pytest.raises(RuntimeError, match="Archive not open for reading"):
                archive.extractfile("test")

    def test_streaming_member_extraction_error(self, temp_dir):
        """Test streaming mode member extraction error (lines 242, 249-254)."""
        # Create a test archive first
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        archive_path = temp_dir / "test.tzst"
        with TzstArchive(archive_path, mode="w") as archive:
            archive.add(str(test_file), arcname="test.txt")

        # Try to extract specific member in streaming mode
        with TzstArchive(archive_path, mode="r", streaming=True) as archive:
            members = archive.getmembers()
            member = members[0]

            extract_dir = temp_dir / "extract"
            extract_dir.mkdir()  # Should raise RuntimeError for specific member extraction in streaming mode
            with pytest.raises(
                RuntimeError,
                match="Extracting specific members is not supported in streaming mode",
            ):
                archive.extract(member=member.name, path=extract_dir)

    def test_streaming_extraction_failure_handling(self, temp_dir):
        """Test streaming extraction failure handling (lines 263-272)."""
        # Create archive first
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        archive_path = temp_dir / "test.tzst"
        with TzstArchive(archive_path, mode="w") as archive:
            archive.add(
                str(test_file), arcname="test.txt"
            )  # Mock tarfile to raise StreamError
        with TzstArchive(archive_path, mode="r", streaming=True) as archive:
            extract_dir = temp_dir / "extract"
            extract_dir.mkdir()

            # Mock extractall to raise StreamError with streaming-related message
            with patch.object(
                archive._tarfile,
                "extractall",
                side_effect=tarfile.StreamError("seeking not supported"),
            ):
                with pytest.raises(
                    RuntimeError, match="Extraction failed in streaming mode"
                ):
                    archive.extract(path=extract_dir)

    def test_extractfile_not_open_error(self, temp_dir):
        """Test extractfile when archive is not open (line 307)."""
        archive_path = temp_dir / "test.tzst"

        # Create closed archive
        archive = TzstArchive(archive_path, mode="r")
        # Don't open it

        with pytest.raises(RuntimeError, match="Archive not open"):
            archive.extractfile("test")

    def test_extractfile_write_mode_error(self, temp_dir):
        """Test extractfile in write mode (already covered but ensuring line coverage)."""
        archive_path = temp_dir / "test.tzst"

        with TzstArchive(archive_path, mode="w") as archive:
            with pytest.raises(RuntimeError, match="Archive not open for reading"):
                archive.extractfile("test")

    def test_add_method_not_open_error(self, temp_dir):
        """Test add method when archive is not open (line 325, 327)."""
        archive_path = temp_dir / "test.tzst"
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Create archive but don't open it
        archive = TzstArchive(archive_path, mode="w")

        with pytest.raises(RuntimeError, match="Archive not open"):
            archive.add(str(test_file))

    def test_add_method_read_mode_error(self, temp_dir):
        """Test add method in read mode (line 327)."""
        # Create archive first
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        archive_path = temp_dir / "test.tzst"
        with TzstArchive(archive_path, mode="w") as archive:
            archive.add(str(test_file), arcname="test.txt")

        # Try to add to archive in read mode
        with TzstArchive(archive_path, mode="r") as archive:
            with pytest.raises(RuntimeError, match="Archive not open for writing"):
                archive.add(str(test_file))

    def test_file_not_found_in_add(self, temp_dir):
        """Test file not found error in add method (line 373)."""
        archive_path = temp_dir / "test.tzst"
        missing_file = temp_dir / "missing.txt"

        with TzstArchive(archive_path, mode="w") as archive:
            with pytest.raises(FileNotFoundError):
                archive.add(str(missing_file))

    def test_add_method_generic_error_handling(self, temp_dir):
        """Test generic error handling in add method (line 375)."""
        archive_path = temp_dir / "test.tzst"
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        with TzstArchive(archive_path, mode="w") as archive:
            # Mock add to raise generic exception
            with patch.object(
                archive._tarfile,
                "add",
                side_effect=PermissionError("Permission denied"),
            ):
                with pytest.raises(TzstArchiveError, match="Failed to add"):
                    archive.add(str(test_file))

    def test_test_method_not_open_error(self, temp_dir):
        """Test test method when archive is not open (line 390-391)."""
        archive_path = temp_dir / "test.tzst"

        # Create archive but don't open it
        archive = TzstArchive(archive_path, mode="r")

        with pytest.raises(RuntimeError, match="Archive not open"):
            archive.test()

    def test_test_method_write_mode_error(self, temp_dir):
        """Test test method in write mode (line 391)."""
        archive_path = temp_dir / "test.tzst"

        with TzstArchive(archive_path, mode="w") as archive:
            with pytest.raises(RuntimeError, match="Archive not open for reading"):
                archive.test()

    def test_test_method_streaming_mode_info(self, temp_dir):
        """Test test method streaming mode information (line 427)."""
        # Create archive first
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        archive_path = temp_dir / "test.tzst"
        with TzstArchive(archive_path, mode="w") as archive:
            archive.add(str(test_file), arcname="test.txt")

        # Test in streaming mode - should provide different behavior info
        with TzstArchive(archive_path, mode="r", streaming=True) as archive:
            # This should work but may have streaming-specific behavior
            result = archive.test()
            assert isinstance(result, bool)

    def test_list_method_not_open_error(self, temp_dir):
        """Test list method when archive is not open (line 454-455)."""
        archive_path = temp_dir / "test.tzst"

        # Create archive but don't open it
        archive = TzstArchive(archive_path, mode="r")

        with pytest.raises(RuntimeError, match="Archive not open"):
            list(archive.list())

    def test_list_method_write_mode_error(self, temp_dir):
        """Test list method in write mode (line 455)."""
        archive_path = temp_dir / "test.tzst"

        with TzstArchive(archive_path, mode="w") as archive:
            with pytest.raises(RuntimeError, match="Archive not open for reading"):
                list(archive.list())

    def test_context_manager_exception_handling(self, temp_dir):
        """Test context manager exception handling (lines 502-504)."""
        archive_path = temp_dir / "test.tzst"

        # Store references for cleanup
        fileobj = None
        compressed_stream = None
        tarfile_obj = None

        # Test that close exceptions are suppressed during context manager exit
        with patch("tzst.core.TzstArchive.close", side_effect=Exception("Close error")):
            try:
                with TzstArchive(archive_path, mode="w") as archive:
                    # Store references to underlying objects for manual cleanup
                    fileobj = archive._fileobj
                    compressed_stream = archive._compressed_stream
                    tarfile_obj = archive._tarfile
                    raise ValueError("Test exception")
            except ValueError:
                pass  # Expected - the original exception should not be masked
            finally:
                # Manually clean up since mocked close() failed
                try:
                    if tarfile_obj:
                        tarfile_obj.close()
                except Exception:
                    pass
                try:
                    if compressed_stream:
                        compressed_stream.close()
                except Exception:
                    pass
                try:
                    if fileobj:
                        fileobj.close()
                except Exception:
                    pass
                # Ensure the file is removed to prevent permission errors
                try:
                    if archive_path.exists():
                        archive_path.unlink()
                except (PermissionError, OSError):
                    pass

            # The close exception should be suppressed by __exit__

    def test_streaming_mode_directory_creation_error(self, temp_dir):
        """Test directory creation error in streaming mode (line 521)."""
        # Create archive first
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        archive_path = temp_dir / "test.tzst"
        with TzstArchive(archive_path, mode="w") as archive:
            archive.add(str(test_file), arcname="test.txt")

        with TzstArchive(archive_path, mode="r", streaming=True) as archive:
            # Mock path creation to fail
            extract_dir = temp_dir / "extract"

            with patch("pathlib.Path.mkdir", side_effect=OSError("Permission denied")):
                with pytest.raises(OSError):
                    archive.extractall(path=extract_dir)

    def test_list_verbose_mode_edge_cases(self, temp_dir):
        """Test list method verbose mode edge cases (lines 573, 588-589)."""
        # Create archive with special files
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Create a directory
        test_dir = temp_dir / "test_dir"
        test_dir.mkdir()

        archive_path = temp_dir / "test.tzst"
        with TzstArchive(archive_path, mode="w") as archive:
            archive.add(str(test_file), arcname="test.txt")
            archive.add(str(test_dir), arcname="test_dir")

        with TzstArchive(archive_path, mode="r") as archive:
            # Test verbose listing
            items = list(archive.list(verbose=True))
            assert len(items) >= 2

            # Should have both file and directory entries
            file_items = [item for item in items if item.get("is_file", False)]
            dir_items = [item for item in items if item.get("is_dir", False)]

            assert len(file_items) >= 1
            assert len(dir_items) >= 1

    def test_extractall_with_members_parameter(self, temp_dir):
        """Test extractall with members parameter for selective extraction."""
        # Create archive with multiple files
        test_file1 = temp_dir / "test1.txt"
        test_file1.write_text("content1")
        test_file2 = temp_dir / "test2.txt"
        test_file2.write_text("content2")

        archive_path = temp_dir / "test.tzst"
        with TzstArchive(archive_path, mode="w") as archive:
            archive.add(str(test_file1), arcname="test1.txt")
            archive.add(str(test_file2), arcname="test2.txt")

        # Extract only specific members
        with TzstArchive(archive_path, mode="r") as archive:
            members = archive.getmembers()
            first_member = members[0]

            extract_dir = temp_dir / "extract"
            extract_dir.mkdir()

            # Extract only first member
            archive.extractall(path=extract_dir, members=[first_member])

            # Verify only one file was extracted
            extracted_files = list(extract_dir.glob("*.txt"))
            assert len(extracted_files) == 1
