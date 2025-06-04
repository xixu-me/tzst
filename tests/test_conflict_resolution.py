# filepath: e:\GitHub\tzst\tests\test_conflict_resolution_clean.py
"""Comprehensive tests for conflict resolution functionality."""

from unittest.mock import Mock, patch

from tzst.cli import _interactive_conflict_callback
from tzst.core import (
    ConflictResolution,
    ConflictResolutionState,
    TzstArchive,
    _get_unique_filename,
    _handle_file_conflict,
    create_archive,
    extract_archive,
)


class TestConflictResolution:
    """Test conflict resolution enum and basic functionality."""

    def test_conflict_resolution_enum_values(self):
        """Test that all ConflictResolution enum values exist."""
        assert ConflictResolution.REPLACE.value == "replace"
        assert ConflictResolution.SKIP.value == "skip"
        assert ConflictResolution.REPLACE_ALL.value == "replace_all"
        assert ConflictResolution.SKIP_ALL.value == "skip_all"
        assert ConflictResolution.AUTO_RENAME.value == "auto_rename"
        assert ConflictResolution.AUTO_RENAME_ALL.value == "auto_rename_all"
        assert ConflictResolution.EXIT.value == "exit"
        assert ConflictResolution.ASK.value == "ask"


class TestUniqueFilename:
    """Test unique filename generation."""

    def test_get_unique_filename_basic(self, temp_dir):
        """Test basic unique filename generation."""
        # Create a file
        original_file = temp_dir / "test.txt"
        original_file.write_text("original")

        # Get unique name
        unique_path = _get_unique_filename(original_file)
        expected_path = temp_dir / "test_1.txt"

        assert unique_path == expected_path
        assert not unique_path.exists()

    def test_get_unique_filename_multiple_conflicts(self, temp_dir):
        """Test unique filename generation with multiple conflicts."""
        # Create multiple files
        original_file = temp_dir / "test.txt"
        conflict1 = temp_dir / "test_1.txt"
        conflict2 = temp_dir / "test_2.txt"

        original_file.write_text("original")
        conflict1.write_text("conflict1")
        conflict2.write_text("conflict2")

        # Get unique name
        unique_path = _get_unique_filename(original_file)
        expected_path = temp_dir / "test_3.txt"

        assert unique_path == expected_path
        assert not unique_path.exists()

    def test_get_unique_filename_no_extension(self, temp_dir):
        """Test unique filename generation for files without extension."""
        # Create a file without extension
        original_file = temp_dir / "README"
        original_file.write_text("readme content")

        # Get unique name
        unique_path = _get_unique_filename(original_file)
        expected_path = temp_dir / "README_1"

        assert unique_path == expected_path
        assert not unique_path.exists()

    def test_get_unique_filename_empty_stem(self, temp_dir):
        """Test unique filename generation for files with empty stem."""
        # Create a file with empty stem (just extension)
        original_file = temp_dir / ".gitignore"
        original_file.write_text("git ignore")

        # Get unique name
        unique_path = _get_unique_filename(original_file)
        expected_path = temp_dir / ".gitignore_1"

        assert unique_path == expected_path
        assert not unique_path.exists()


class TestHandleFileConflict:
    """Test file conflict handling function."""

    def test_handle_file_conflict_replace(self, temp_dir):
        """Test REPLACE conflict resolution."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing")

        resolution, final_path = _handle_file_conflict(
            target_path, ConflictResolution.REPLACE, None
        )

        assert resolution == ConflictResolution.REPLACE
        assert final_path == target_path

    def test_handle_file_conflict_skip(self, temp_dir):
        """Test SKIP conflict resolution."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing")

        resolution, final_path = _handle_file_conflict(
            target_path, ConflictResolution.SKIP, None
        )

        assert resolution == ConflictResolution.SKIP
        assert final_path is None

    def test_handle_file_conflict_replace_all(self, temp_dir):
        """Test REPLACE_ALL conflict resolution."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing")

        resolution, final_path = _handle_file_conflict(
            target_path, ConflictResolution.REPLACE_ALL, None
        )

        assert resolution == ConflictResolution.REPLACE_ALL
        assert final_path == target_path

    def test_handle_file_conflict_skip_all(self, temp_dir):
        """Test SKIP_ALL conflict resolution."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing")

        resolution, final_path = _handle_file_conflict(
            target_path, ConflictResolution.SKIP_ALL, None
        )

        assert resolution == ConflictResolution.SKIP_ALL
        assert final_path is None

    def test_handle_file_conflict_auto_rename(self, temp_dir):
        """Test AUTO_RENAME conflict resolution."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing")

        resolution, final_path = _handle_file_conflict(
            target_path, ConflictResolution.AUTO_RENAME, None
        )

        assert resolution == ConflictResolution.AUTO_RENAME
        assert final_path == temp_dir / "existing_1.txt"
        assert not final_path.exists()

    def test_handle_file_conflict_auto_rename_all(self, temp_dir):
        """Test AUTO_RENAME_ALL conflict resolution."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing")

        resolution, final_path = _handle_file_conflict(
            target_path, ConflictResolution.AUTO_RENAME_ALL, None
        )

        assert resolution == ConflictResolution.AUTO_RENAME_ALL
        assert final_path == temp_dir / "existing_1.txt"
        assert not final_path.exists()

    def test_handle_file_conflict_exit(self, temp_dir):
        """Test EXIT conflict resolution."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing")

        resolution, final_path = _handle_file_conflict(
            target_path, ConflictResolution.EXIT, None
        )

        assert resolution == ConflictResolution.EXIT
        assert final_path is None

    def test_handle_file_conflict_ask_with_callback(self, temp_dir):
        """Test ASK conflict resolution with callback."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing")

        mock_callback = Mock(return_value=ConflictResolution.REPLACE)

        resolution, final_path = _handle_file_conflict(
            target_path, ConflictResolution.ASK, mock_callback
        )

        assert resolution == ConflictResolution.REPLACE
        assert final_path == target_path
        mock_callback.assert_called_once_with(target_path)

    def test_handle_file_conflict_ask_no_callback(self, temp_dir):
        """Test ASK conflict resolution without callback defaults to REPLACE."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing")

        resolution, final_path = _handle_file_conflict(
            target_path, ConflictResolution.ASK, None
        )

        assert resolution == ConflictResolution.REPLACE
        assert final_path == target_path

    def test_handle_file_conflict_string_resolution_valid(self, temp_dir):
        """Test string-based conflict resolution."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing")

        resolution, final_path = _handle_file_conflict(target_path, "skip", None)

        assert resolution == ConflictResolution.SKIP
        assert final_path is None

    def test_handle_file_conflict_string_resolution_invalid(self, temp_dir):
        """Test invalid string conflict resolution defaults to REPLACE."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing")

        resolution, final_path = _handle_file_conflict(
            target_path, "invalid_resolution", None
        )

        assert resolution == ConflictResolution.REPLACE
        assert final_path == target_path

    def test_handle_file_conflict_unknown_resolution(self, temp_dir):
        """Test unknown conflict resolution defaults to REPLACE."""
        target_path = temp_dir / "existing.txt"
        target_path.write_text("existing")

        # Pass something that's not a valid enum value
        resolution, final_path = _handle_file_conflict(
            target_path, "completely_unknown", None
        )

        assert resolution == ConflictResolution.REPLACE
        assert final_path == target_path


class TestConflictResolutionState:
    """Test conflict resolution state management."""

    def test_initial_state(self):
        """Test initial state with different resolutions."""
        state1 = ConflictResolutionState(ConflictResolution.REPLACE)
        assert state1.current_resolution == ConflictResolution.REPLACE
        assert state1.should_continue() is True

        state2 = ConflictResolutionState(ConflictResolution.EXIT)
        assert state2.current_resolution == ConflictResolution.EXIT
        assert state2.should_continue() is False

    def test_update_resolution_replace_all(self):
        """Test updating to REPLACE_ALL."""
        state = ConflictResolutionState(ConflictResolution.ASK)
        state.update_resolution(ConflictResolution.REPLACE_ALL)

        assert state.current_resolution == ConflictResolution.REPLACE_ALL
        assert state.should_continue() is True

    def test_update_resolution_skip_all(self):
        """Test updating to SKIP_ALL."""
        state = ConflictResolutionState(ConflictResolution.ASK)
        state.update_resolution(ConflictResolution.SKIP_ALL)

        assert state.current_resolution == ConflictResolution.SKIP_ALL
        assert state.should_continue() is True

    def test_update_resolution_auto_rename_all(self):
        """Test updating to AUTO_RENAME_ALL."""
        state = ConflictResolutionState(ConflictResolution.ASK)
        state.update_resolution(ConflictResolution.AUTO_RENAME_ALL)

        assert state.current_resolution == ConflictResolution.AUTO_RENAME_ALL
        assert state.should_continue() is True

    def test_update_resolution_exit(self):
        """Test updating to EXIT."""
        state = ConflictResolutionState(ConflictResolution.ASK)
        state.update_resolution(ConflictResolution.EXIT)

        assert state.current_resolution == ConflictResolution.EXIT
        assert state.should_continue() is False

    def test_update_resolution_normal(self):
        """Test updating to normal resolution doesn't change state."""
        state = ConflictResolutionState(ConflictResolution.ASK)
        state.update_resolution(ConflictResolution.REPLACE)

        assert state.current_resolution == ConflictResolution.ASK
        assert state.should_continue() is True


class TestExtractArchiveConflictResolution:
    """Test extract_archive with conflict resolution."""

    def test_extract_with_replace_conflict_resolution(self, temp_dir):
        """Test extraction with REPLACE conflict resolution."""
        # Create archive
        archive_path = temp_dir / "test.tzst"
        source_file = temp_dir / "source.txt"
        source_file.write_text("archive content")

        create_archive(archive_path, [source_file])

        # Create extract directory with conflicting file
        extract_dir = temp_dir / "extract"
        extract_dir.mkdir()
        conflict_file = extract_dir / "source.txt"
        conflict_file.write_text("existing content")

        # Extract with REPLACE resolution
        extract_archive(
            archive_path, extract_dir, conflict_resolution=ConflictResolution.REPLACE
        )

        # Verify file was replaced
        assert conflict_file.read_text() == "archive content"

    def test_extract_with_skip_conflict_resolution(self, temp_dir):
        """Test extraction with SKIP conflict resolution."""
        # Create archive
        archive_path = temp_dir / "test.tzst"
        source_file = temp_dir / "source.txt"
        source_file.write_text("archive content")

        create_archive(archive_path, [source_file])

        # Create extract directory with conflicting file
        extract_dir = temp_dir / "extract"
        extract_dir.mkdir()
        conflict_file = extract_dir / "source.txt"
        conflict_file.write_text("existing content")

        # Extract with SKIP resolution
        extract_archive(
            archive_path, extract_dir, conflict_resolution=ConflictResolution.SKIP
        )

        # Verify file was not replaced
        assert conflict_file.read_text() == "existing content"

    def test_extract_with_interactive_callback(self, temp_dir):
        """Test extraction with interactive callback."""
        # Create archive
        archive_path = temp_dir / "test.tzst"
        source_file = temp_dir / "source.txt"
        source_file.write_text("archive content")

        create_archive(archive_path, [source_file])

        # Create extract directory with conflicting file
        extract_dir = temp_dir / "extract"
        extract_dir.mkdir()
        conflict_file = extract_dir / "source.txt"
        conflict_file.write_text("existing content")

        mock_callback = Mock(return_value=ConflictResolution.REPLACE)

        # Extract with interactive callback
        extract_archive(
            archive_path,
            extract_dir,
            conflict_resolution=ConflictResolution.ASK,
            interactive_callback=mock_callback,
        )

        # Verify callback was called and file was replaced
        mock_callback.assert_called_once()
        assert conflict_file.read_text() == "archive content"


class TestTzstArchiveConflictResolution:
    """Test extract_archive function with conflict resolution (corrected)."""

    def test_extract_archive_with_conflict_resolution(self, temp_dir):
        """Test extract_archive function with conflict resolution parameter."""
        # Create archive
        source_file = temp_dir / "source.txt"
        source_file.write_text("archive content")
        archive_path = temp_dir / "test.tzst"

        with TzstArchive(archive_path, mode="w") as archive:
            archive.add(str(source_file), arcname="source.txt")

        # Create conflicting file in extract directory
        extract_dir = temp_dir / "extract"
        extract_dir.mkdir()
        conflict_file = extract_dir / "source.txt"
        conflict_file.write_text("existing content")

        # Extract with REPLACE resolution using extract_archive function
        extract_archive(
            archive_path, extract_dir, conflict_resolution=ConflictResolution.REPLACE
        )

        # Should have replaced the file
        assert conflict_file.read_text() == "archive content"


class TestInteractiveConflictCallback:
    """Test interactive conflict callback functionality."""

    @patch("builtins.input")
    def test_interactive_callback_replace(self, mock_input, temp_dir):
        """Test interactive callback with replace choice."""
        mock_input.return_value = "r"
        file_path = temp_dir / "test.txt"

        result = _interactive_conflict_callback(file_path)
        assert result == ConflictResolution.REPLACE

    @patch("builtins.input")
    def test_interactive_callback_skip(self, mock_input, temp_dir):
        """Test interactive callback with skip choice."""
        mock_input.return_value = "n"
        file_path = temp_dir / "test.txt"

        result = _interactive_conflict_callback(file_path)
        assert result == ConflictResolution.SKIP

    @patch("builtins.input")
    def test_interactive_callback_exit(self, mock_input, temp_dir):
        """Test interactive callback with exit choice."""
        mock_input.return_value = "x"
        file_path = temp_dir / "test.txt"

        result = _interactive_conflict_callback(file_path)
        assert result == ConflictResolution.EXIT

    @patch("builtins.input")
    def test_interactive_callback_invalid_then_valid(self, mock_input, temp_dir):
        """Test interactive callback with invalid then valid choice."""
        mock_input.side_effect = ["invalid", "r"]
        file_path = temp_dir / "test.txt"

        result = _interactive_conflict_callback(file_path)
        assert result == ConflictResolution.REPLACE
        assert mock_input.call_count == 2

    @patch("builtins.input")
    def test_interactive_callback_keyboard_interrupt(self, mock_input, temp_dir):
        """Test interactive callback with KeyboardInterrupt."""
        mock_input.side_effect = KeyboardInterrupt()
        file_path = temp_dir / "test.txt"

        result = _interactive_conflict_callback(file_path)
        assert result == ConflictResolution.EXIT

    @patch("builtins.input")
    def test_interactive_callback_eof_error(self, mock_input, temp_dir):
        """Test interactive callback with EOFError."""
        mock_input.side_effect = EOFError()
        file_path = temp_dir / "test.txt"

        result = _interactive_conflict_callback(file_path)
        assert result == ConflictResolution.EXIT
