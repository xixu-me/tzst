"""Tests for edge cases and error conditions in core.py to improve coverage.

This test file targets the specific missing lines identified in the coverage report,
focusing on error handling, edge cases, and less common code paths.
"""

import tarfile
from unittest.mock import Mock, patch

import pytest

from tzst.core import (
    ConflictResolution,
    TzstArchive,
    _handle_file_conflict,
    create_archive,
    extract_archive,
)


class TestConflictResolutionEdgeCases:
    """Test edge cases in conflict resolution handling."""

    def test_handle_file_conflict_invalid_string_resolution(self, temp_dir):
        """Test _handle_file_conflict with invalid string resolution."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing content")

        # Test with invalid string - should fallback to ASK
        result_action, result_path = _handle_file_conflict(
            target_path, "invalid_resolution", None
        )  # Should fallback to REPLACE when no interactive callback
        assert result_action == ConflictResolution.REPLACE
        assert result_path == target_path

    def test_handle_file_conflict_ask_with_callback(self, temp_dir):
        """Test ASK resolution with interactive callback."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing content")

        # Mock interactive callback that returns REPLACE
        mock_callback = Mock(return_value=ConflictResolution.REPLACE)

        result_action, result_path = _handle_file_conflict(
            target_path, ConflictResolution.ASK, mock_callback
        )

        assert result_action == ConflictResolution.REPLACE
        assert result_path == target_path
        mock_callback.assert_called_once_with(target_path)

    def test_handle_file_conflict_ask_without_callback(self, temp_dir):
        """Test ASK resolution without interactive callback."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing content")

        result_action, result_path = _handle_file_conflict(
            target_path, ConflictResolution.ASK, None
        )  # Should default to REPLACE when no callback available
        assert result_action == ConflictResolution.REPLACE
        assert result_path == target_path

    def test_handle_file_conflict_unknown_resolution(self, temp_dir):
        """Test handling of unknown resolution types."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing content")

        # Create a mock enum value that's not handled
        unknown_resolution = Mock()
        unknown_resolution.name = "UNKNOWN"

        result_action, result_path = _handle_file_conflict(
            target_path, unknown_resolution, None
        )

        # Should default to REPLACE for unknown resolutions
        assert result_action == ConflictResolution.REPLACE
        assert result_path == target_path


class TestArchiveErrorHandling:
    """Test error handling in archive operations."""

    def test_archive_streaming_extraction_error(self, temp_dir):
        """Test extraction error in streaming mode."""
        # Create a simple archive first
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        archive_path = temp_dir / "test.tzst"

        create_archive(archive_path, [test_file])

        # Mock tarfile to raise StreamError
        with patch("tarfile.open") as mock_open:
            mock_tarfile = Mock()
            mock_open.return_value.__enter__.return_value = mock_tarfile
            mock_tarfile.extractall.side_effect = tarfile.StreamError(
                "seeking not allowed"
            )

            archive = TzstArchive(archive_path, "r", streaming=True)
            archive._tarfile = mock_tarfile
            archive.streaming = True

            with pytest.raises(
                RuntimeError, match="Extraction failed in streaming mode"
            ):
                archive.extractall(temp_dir / "extract")

    def test_getmembers_archive_not_open(self):
        """Test getmembers when archive is not open."""
        archive = TzstArchive("dummy.tzst", "r")
        archive._tarfile = None

        with pytest.raises(RuntimeError, match="Archive not open"):
            archive.getmembers()

    def test_getmembers_wrong_mode(self, temp_dir):
        """Test getmembers when archive is not in read mode."""
        archive_path = temp_dir / "test.tzst"

        with TzstArchive(archive_path, "w") as archive:
            with pytest.raises(RuntimeError, match="Archive not open for reading"):
                archive.getmembers()

    def test_getnames_archive_not_open(self):
        """Test getnames when archive is not open."""
        archive = TzstArchive("dummy.tzst", "r")
        archive._tarfile = None

        with pytest.raises(RuntimeError, match="Archive not open"):
            archive.getnames()

    def test_getnames_wrong_mode(self, temp_dir):
        """Test getnames when archive is not in read mode."""
        archive_path = temp_dir / "test.tzst"

        with TzstArchive(archive_path, "w") as archive:
            with pytest.raises(RuntimeError, match="Archive not open for reading"):
                archive.getnames()


class TestCreateArchiveErrorHandling:
    """Test error handling in archive creation."""

    def test_create_archive_cleanup_on_error(self, temp_dir):
        """Test archive creation cleans up on error."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        archive_path = temp_dir / "test.tzst"

        # Test that errors during archive creation are properly handled
        # Simulate error by trying to create archive with invalid compression level
        with pytest.raises(ValueError, match="Invalid compression level"):
            create_archive(archive_path, [test_file], compression_level=50)

        # Archive should not be created when error occurs
        assert not archive_path.exists()

    def test_create_archive_common_path_no_common_parent(self, temp_dir):
        """Test create_archive when files have no common parent path."""
        file1 = temp_dir / "file1.txt"
        file1.write_text("content1")

        with patch("os.path.commonpath", side_effect=ValueError("no common path")):
            archive_path = temp_dir / "test.tzst"

            # Should use parent of first file as fallback
            create_archive(archive_path, [file1])

            assert archive_path.exists()


class TestExtractArchiveEdgeCases:
    """Test edge cases in archive extraction."""

    def test_extract_archive_exit_resolution(self, temp_dir):
        """Test extraction with EXIT conflict resolution."""
        # Create archive with multiple files
        file1 = temp_dir / "file1.txt"
        file1.write_text("content1")
        file2 = temp_dir / "file2.txt"
        file2.write_text("content2")

        archive_path = temp_dir / "test.tzst"
        create_archive(archive_path, [file1, file2])

        extract_dir = temp_dir / "extract"
        extract_dir.mkdir()

        # Create a conflicting file
        conflict_file = extract_dir / "file1.txt"
        conflict_file.write_text("existing content")

        # Extract with EXIT resolution
        extract_archive(
            archive_path, extract_dir, conflict_resolution=ConflictResolution.EXIT
        )

        # Should stop on first conflict
        assert conflict_file.read_text() == "existing content"
        assert not (extract_dir / "file2.txt").exists()

    def test_extract_archive_members_with_state_break(self, temp_dir):
        """Test extraction of specific members with state break."""
        # Create archive with multiple files
        file1 = temp_dir / "file1.txt"
        file1.write_text("content1")
        file2 = temp_dir / "file2.txt"
        file2.write_text("content2")

        archive_path = temp_dir / "test.tzst"
        create_archive(archive_path, [file1, file2])

        extract_dir = temp_dir / "extract"
        extract_dir.mkdir()

        # Mock ConflictResolutionState to return False for should_continue
        with patch("tzst.core.ConflictResolutionState") as mock_state_class:
            mock_state = Mock()
            mock_state.should_continue.return_value = False
            mock_state.apply_to_all = False
            mock_state_class.return_value = mock_state

            extract_archive(
                archive_path, extract_dir, members=["file1.txt", "file2.txt"]
            )

            # Should break early due to state.should_continue()
            assert mock_state.should_continue.called

    def test_extract_archive_with_filter_parameter(self, temp_dir):
        """Test extraction using filter parameter."""
        # Create archive with a file
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        archive_path = temp_dir / "test.tzst"
        create_archive(archive_path, [test_file])

        extract_dir = temp_dir / "extract"
        extract_dir.mkdir()

        # Mock filter function
        def mock_filter(member, path):
            return member

        # Extract with filter (tests the filter parameter branch)
        extract_archive(archive_path, extract_dir, filter=mock_filter)

        extracted_file = extract_dir / "test.txt"
        assert extracted_file.exists()
        assert extracted_file.read_text() == "test content"
