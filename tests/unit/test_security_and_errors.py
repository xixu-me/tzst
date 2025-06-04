"""Tests for security features and error handling."""

from unittest.mock import patch

import pytest

from tzst import TzstArchive, create_archive, extract_archive
from tzst import test_archive as tzst_test_archive


@pytest.mark.unit
class TestErrorHandling:
    """Test error handling."""

    def test_invalid_archive_mode(self, sample_archive_path):
        """Test invalid archive mode."""
        with pytest.raises(ValueError):
            TzstArchive(sample_archive_path, "invalid")

    def test_append_mode_not_supported(self, sample_archive_path):
        """Test that append mode raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            TzstArchive(sample_archive_path, "a")

    def test_archive_not_open(self, sample_archive_path):
        """Test operations on non-open archive."""
        archive = TzstArchive(sample_archive_path, "r")

        with pytest.raises(RuntimeError):
            archive.getnames()

    def test_file_not_found(self, temp_dir):
        """Test handling of non-existent files."""
        archive_path = temp_dir / "test.tzst"
        fake_file = temp_dir / "fake.txt"

        with pytest.raises(FileNotFoundError):
            create_archive(archive_path, [fake_file])


@pytest.mark.unit
class TestSecurityFiltering:
    """Test security filtering mechanisms."""

    def test_tar_filter_extraction(self, sample_files, temp_dir):
        """Test extraction with TAR security filter."""
        file_paths = [f for f in sample_files if f.is_file()]
        archive_path = temp_dir / "tar_filter_test.tzst"

        # Create archive
        create_archive(archive_path, file_paths)

        # Extract with tar filter
        extract_dir = temp_dir / "tar_filtered"
        with patch("tzst.core.TzstArchive.extractall") as mock_extractall:
            extract_archive(archive_path, extract_dir, filter="tar")

            # Verify filter was passed
            call_args = mock_extractall.call_args
            assert call_args[1]["filter"] == "tar"

    def test_data_filter_extraction(self, sample_files, temp_dir):
        """Test extraction with data security filter."""
        file_paths = [f for f in sample_files if f.is_file()]
        archive_path = temp_dir / "data_filter_test.tzst"

        # Create archive
        create_archive(archive_path, file_paths)

        # Extract with data filter (default for security)
        extract_dir = temp_dir / "data_filtered"
        with patch("tzst.core.TzstArchive.extractall") as mock_extractall:
            extract_archive(archive_path, extract_dir, filter="data")

            # Verify filter was passed
            call_args = mock_extractall.call_args
            assert call_args[1]["filter"] == "data"

    def test_invalid_filter_raises_error(self, sample_files, temp_dir):
        """Test that invalid filters raise appropriate errors."""
        file_paths = [f for f in sample_files if f.is_file()]
        archive_path = temp_dir / "invalid_filter_test.tzst"

        # Create archive
        create_archive(archive_path, file_paths)

        # Try to extract with invalid filter
        extract_dir = temp_dir / "invalid_filtered"
        with pytest.raises(ValueError):
            extract_archive(archive_path, extract_dir, filter="invalid")


class TestCompressionValidation:
    """Test compression level validation."""

    def test_compression_level_boundary_values(self, sample_files, temp_dir):
        """Test boundary compression level values."""
        file_paths = [f for f in sample_files if f.is_file()]

        # Test level 1 (minimum valid)
        archive_path_min = temp_dir / "min_compression.tzst"
        create_archive(archive_path_min, file_paths, compression_level=1)
        assert archive_path_min.exists()
        assert tzst_test_archive(archive_path_min) is True

        # Test level 22 (maximum valid)
        archive_path_max = temp_dir / "max_compression.tzst"
        create_archive(archive_path_max, file_paths, compression_level=22)
        assert archive_path_max.exists()
        assert tzst_test_archive(archive_path_max) is True

    def test_invalid_compression_levels_raise_error(self, sample_files, temp_dir):
        """Test that invalid compression levels raise appropriate errors."""
        file_paths = [f for f in sample_files if f.is_file()]
        archive_path = temp_dir / "invalid_compression.tzst"

        # Test invalid levels that should raise ValueError
        for invalid_level in [0, 23, -1, 100]:
            with pytest.raises(ValueError):
                create_archive(
                    archive_path, file_paths, compression_level=invalid_level
                )

    def test_specific_compression_level_validation(self, temp_dir):
        """Test specific compression level validation to cover missing lines."""
        import tempfile
        from pathlib import Path

        with tempfile.NamedTemporaryFile(suffix=".tzst", delete=False) as f:
            archive_path = Path(f.name)

        try:
            # Test compression level too low (line 60)
            with pytest.raises(ValueError, match="Invalid compression level '0'"):
                TzstArchive(archive_path, mode="w", compression_level=0)

            # Test compression level too high (line 66)
            with pytest.raises(ValueError, match="Invalid compression level '23'"):
                TzstArchive(archive_path, mode="w", compression_level=23)

        finally:
            archive_path.unlink(missing_ok=True)

    def test_invalid_mode_validation(self, temp_dir):
        """Test invalid mode validation to cover missing lines."""
        import tempfile
        from pathlib import Path

        with tempfile.NamedTemporaryFile(suffix=".tzst", delete=False) as f:
            archive_path = Path(f.name)

        try:
            # Test invalid mode (line 54)
            with pytest.raises(ValueError, match="Invalid mode 'x'"):
                TzstArchive(archive_path, mode="x")

            # Test invalid mode with additional characters
            with pytest.raises(ValueError, match="Invalid mode 'rb'"):
                TzstArchive(archive_path, mode="rb")

        finally:
            archive_path.unlink(missing_ok=True)

    def test_runtime_errors_for_wrong_mode_operations(self, temp_dir):
        """Test RuntimeError for operations on wrong mode archives."""
        import tempfile
        from pathlib import Path

        with tempfile.NamedTemporaryFile(suffix=".tzst", delete=False) as f:
            archive_path = Path(f.name)

        try:
            # Create empty archive first
            with TzstArchive(archive_path, mode="w") as archive:
                pass

            # Test read operations on write mode
            with TzstArchive(archive_path, mode="w") as archive:
                with pytest.raises(RuntimeError, match="Archive not open for reading"):
                    archive.getmembers()

                with pytest.raises(RuntimeError, match="Archive not open for reading"):
                    archive.getnames()

                with pytest.raises(RuntimeError, match="Archive not open for reading"):
                    archive.extractfile("test")

        finally:
            archive_path.unlink(missing_ok=True)

    def test_operations_on_closed_archive(self, temp_dir):
        """Test operations on closed archive to cover missing lines."""
        import tempfile
        from pathlib import Path

        with tempfile.NamedTemporaryFile(suffix=".tzst", delete=False) as f:
            archive_path = Path(f.name)

        try:
            # Create and close archive
            archive = TzstArchive(archive_path, mode="w")
            archive.close()

            # Test operations on closed archive
            with pytest.raises(RuntimeError, match="Archive not open"):
                archive.getmembers()

            with pytest.raises(RuntimeError, match="Archive not open"):
                archive.getnames()

            with pytest.raises(RuntimeError, match="Archive not open"):
                archive.extractfile("test")

        finally:
            archive_path.unlink(missing_ok=True)

    def test_close_error_handling(self, temp_dir):
        """Test error handling in close method."""
        from pathlib import Path
        from unittest.mock import MagicMock

        # Create a mock archive that will raise exceptions during close
        archive = TzstArchive.__new__(TzstArchive)
        archive.path = Path("test.tzst")
        archive.mode = "w"
        archive.compression_level = 3

        # Create mock objects that raise exceptions when closed
        mock_tarfile = MagicMock()
        mock_tarfile.close.side_effect = Exception("Mock tarfile close error")

        mock_stream = MagicMock()
        mock_stream.close.side_effect = Exception("Mock stream close error")

        mock_fileobj = MagicMock()
        mock_fileobj.close.side_effect = Exception("Mock fileobj close error")

        archive._tarfile = mock_tarfile
        archive._compressed_stream = mock_stream
        archive._fileobj = mock_fileobj

        # This should not raise an exception despite the mock exceptions
        archive.close()

        # Verify all close methods were called
        mock_tarfile.close.assert_called_once()
        mock_stream.close.assert_called_once()
        mock_fileobj.close.assert_called_once()


class TestSpecialFileTypes:
    """Test handling of special file types and edge cases."""

    def test_empty_files(self, temp_dir):
        """Test archiving and extracting empty files."""
        empty_file = temp_dir / "empty.txt"
        empty_file.touch()

        archive_path = temp_dir / "empty_file.tzst"
        create_archive(archive_path, [empty_file])

        assert archive_path.exists()
        assert tzst_test_archive(archive_path) is True

        # Test extraction
        extract_dir = temp_dir / "empty_extracted"
        extract_archive(archive_path, extract_dir)

        extracted_file = extract_dir / "empty.txt"
        assert extracted_file.exists()
        assert extracted_file.stat().st_size == 0

    def test_binary_files(self, temp_dir):
        """Test archiving binary files."""
        binary_file = temp_dir / "binary.bin"
        binary_content = bytes(range(256)) * 100  # 25.6KB of binary data
        binary_file.write_bytes(binary_content)

        archive_path = temp_dir / "binary_file.tzst"
        create_archive(archive_path, [binary_file])

        assert archive_path.exists()
        assert tzst_test_archive(archive_path) is True

        # Test extraction
        extract_dir = temp_dir / "binary_extracted"
        extract_archive(archive_path, extract_dir)

        extracted_file = extract_dir / "binary.bin"
        assert extracted_file.exists()
        extracted_content = extracted_file.read_bytes()
        assert extracted_content == binary_content

    def test_files_with_special_characters(self, temp_dir):
        """Test files with special characters in names."""
        special_chars_file = temp_dir / "file!@#$%^&()_+{}[]-',.txt"
        special_chars_file.write_text("Special characters content")

        archive_path = temp_dir / "special_chars.tzst"
        create_archive(archive_path, [special_chars_file])

        assert archive_path.exists()
        assert tzst_test_archive(archive_path) is True


class TestAppendModeDocumentation:
    """Test that append mode provides helpful error messages."""

    def test_append_mode_error_message(self, temp_dir):
        """Test that append mode raises informative error."""
        archive_path = temp_dir / "append_test.tzst"

        with pytest.raises(NotImplementedError) as exc_info:
            TzstArchive(archive_path, "a")

        error_msg = str(exc_info.value)
        assert "append mode" in error_msg.lower()
        assert "alternatives" in error_msg.lower() or "alternative" in error_msg.lower()
        assert "decompressing" in error_msg.lower()
        assert "recompressing" in error_msg.lower()

    def test_append_mode_error_in_open(self, temp_dir):
        """Test append mode error when opening existing archive."""
        archive_path = temp_dir / "append_open_test.tzst"

        # Create an archive first
        with TzstArchive(archive_path, "w"):
            pass

        # Try to open in append mode
        with pytest.raises(NotImplementedError) as exc_info:
            TzstArchive(archive_path, "a")

        error_msg = str(exc_info.value)
        assert (
            "multiple archives" in error_msg.lower() or "recreate" in error_msg.lower()
        )


class TestSpecificMissingLineCoverage:
    """Test specific missing lines from coverage report."""

    def test_invalid_mode_validation_specific(self, temp_dir):
        """Test specific invalid mode validation to cover missing lines."""
        import tempfile
        from pathlib import Path

        with tempfile.NamedTemporaryFile(suffix=".tzst", delete=False) as f:
            archive_path = Path(f.name)

        try:
            # Test invalid mode (line 54)
            with pytest.raises(ValueError, match="Invalid mode 'x'"):
                TzstArchive(archive_path, mode="x")

            # Test invalid mode with additional characters
            with pytest.raises(ValueError, match="Invalid mode 'rb'"):
                TzstArchive(archive_path, mode="rb")

        finally:
            archive_path.unlink(missing_ok=True)

    def test_compression_level_validation_specific(self, temp_dir):
        """Test specific compression level validation to cover missing lines."""
        import tempfile
        from pathlib import Path

        with tempfile.NamedTemporaryFile(suffix=".tzst", delete=False) as f:
            archive_path = Path(f.name)

        try:
            # Test compression level too low (line 60)
            with pytest.raises(ValueError, match="Invalid compression level '0'"):
                TzstArchive(archive_path, mode="w", compression_level=0)

            # Test compression level too high (line 66)
            with pytest.raises(ValueError, match="Invalid compression level '23'"):
                TzstArchive(archive_path, mode="w", compression_level=23)

        finally:
            archive_path.unlink(missing_ok=True)

    def test_runtime_errors_for_wrong_mode_operations(self, temp_dir):
        """Test RuntimeError for operations on wrong mode archives."""
        import tempfile
        from pathlib import Path

        with tempfile.NamedTemporaryFile(suffix=".tzst", delete=False) as f:
            archive_path = Path(f.name)

        try:
            # Create empty archive first
            with TzstArchive(archive_path, mode="w") as archive:
                pass

            # Test read operations on write mode
            with TzstArchive(archive_path, mode="w") as archive:
                with pytest.raises(RuntimeError, match="Archive not open for reading"):
                    archive.getmembers()

                with pytest.raises(RuntimeError, match="Archive not open for reading"):
                    archive.getnames()

                with pytest.raises(RuntimeError, match="Archive not open for reading"):
                    archive.extractfile("test")

        finally:
            archive_path.unlink(missing_ok=True)

    def test_operations_on_closed_archive_specific(self, temp_dir):
        """Test operations on closed archive to cover missing lines."""
        import tempfile
        from pathlib import Path

        with tempfile.NamedTemporaryFile(suffix=".tzst", delete=False) as f:
            archive_path = Path(f.name)

        try:
            # Create and close archive
            archive = TzstArchive(archive_path, mode="w")
            archive.close()

            # Test operations on closed archive
            with pytest.raises(RuntimeError, match="Archive not open"):
                archive.getmembers()

            with pytest.raises(RuntimeError, match="Archive not open"):
                archive.getnames()

            with pytest.raises(RuntimeError, match="Archive not open"):
                archive.extractfile("test")

        finally:
            archive_path.unlink(missing_ok=True)
