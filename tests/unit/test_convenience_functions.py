"""Tests for tzst convenience functions."""

import pytest

from tzst import create_archive, extract_archive, list_archive
from tzst import test_archive as tzst_test_archive


class TestConvenienceFunctions:
    """Test the convenience functions."""

    def test_create_archive_function(self, sample_files, sample_archive_path):
        """Test create_archive function."""
        file_paths = [f for f in sample_files if f.is_file()]
        create_archive(sample_archive_path, file_paths)

        assert sample_archive_path.exists()

        # Verify contents
        contents = list_archive(sample_archive_path)
        assert len(contents) > 0

    def test_extract_archive_function(
        self, sample_files, sample_archive_path, temp_dir
    ):
        """Test extract_archive function."""
        # Create archive first
        file_paths = [f for f in sample_files if f.is_file()]
        create_archive(sample_archive_path, file_paths)

        # Extract
        extract_dir = temp_dir / "extracted"
        extract_archive(sample_archive_path, extract_dir)

        # Verify extraction
        assert extract_dir.exists()
        extracted_files = list(extract_dir.rglob("*"))
        assert len(extracted_files) > 0

    def test_extract_archive_flat(self, sample_files, sample_archive_path, temp_dir):
        """Test flat extraction."""
        # Create archive first
        file_paths = [f for f in sample_files if f.is_file()]
        create_archive(sample_archive_path, file_paths)

        # Extract flat
        extract_dir = temp_dir / "extracted_flat"
        extract_archive(sample_archive_path, extract_dir, flatten=True)

        # Verify flat extraction (no subdirectories)
        assert extract_dir.exists()
        extracted_files = [f for f in extract_dir.iterdir() if f.is_file()]
        extracted_dirs = [d for d in extract_dir.iterdir() if d.is_dir()]

        assert len(extracted_files) > 0
        assert len(extracted_dirs) == 0  # Should be flat

    def test_list_archive_function(self, sample_files, sample_archive_path):
        """Test list_archive function."""
        # Create archive first
        file_paths = [f for f in sample_files if f.is_file()]
        create_archive(sample_archive_path, file_paths)

        # List contents
        contents = list_archive(sample_archive_path)
        assert len(contents) > 0

        # Test verbose listing
        verbose_contents = list_archive(sample_archive_path, verbose=True)
        assert len(verbose_contents) == len(contents)
        assert "mode" in verbose_contents[0]

    def test_test_archive_function(self, sample_files, sample_archive_path):
        """Test test_archive function."""
        # Create archive first
        file_paths = [f for f in sample_files if f.is_file()]
        create_archive(sample_archive_path, file_paths)

        # Test archive
        assert tzst_test_archive(sample_archive_path) is True

        # Test non-existent archive
        fake_archive = sample_archive_path.parent / "fake.tzst"
        assert tzst_test_archive(fake_archive) is False

    def test_streaming_convenience_functions(
        self, sample_files, sample_archive_path, temp_dir
    ):
        """Test convenience functions with streaming parameter."""
        # Create archive first
        file_paths = [f for f in sample_files if f.is_file()]
        create_archive(sample_archive_path, file_paths)

        # Test list_archive with streaming
        contents_normal = list_archive(sample_archive_path, streaming=False)
        contents_streaming = list_archive(sample_archive_path, streaming=True)
        assert len(contents_normal) == len(contents_streaming)

        # Test test_archive with streaming
        assert tzst_test_archive(sample_archive_path, streaming=False) is True
        assert tzst_test_archive(sample_archive_path, streaming=True) is True

        # Test extract_archive with streaming
        extract_dir_normal = temp_dir / "extract_normal"
        extract_dir_streaming = temp_dir / "extract_streaming"

        extract_archive(sample_archive_path, extract_dir_normal, streaming=False)
        extract_archive(sample_archive_path, extract_dir_streaming, streaming=True)

        assert extract_dir_normal.exists()
        assert extract_dir_streaming.exists()


class TestAtomicOperations:
    """Test atomic file operations."""

    def test_atomic_file_operations(self, sample_files, temp_dir):
        """Test atomic file operations."""
        archive_path = temp_dir / "atomic_test.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Test with atomic operations enabled
        create_archive(archive_path, file_paths, use_temp_file=True)
        assert archive_path.exists()

        # Verify archive is valid
        assert tzst_test_archive(archive_path) is True

    def test_non_atomic_file_creation(self, sample_files, temp_dir):
        """Test that non-atomic creation also works."""
        archive_path = temp_dir / "non_atomic_test.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Test with atomic operations disabled
        create_archive(archive_path, file_paths, use_temp_file=False)
        assert archive_path.exists()

        # Verify archive is valid
        assert tzst_test_archive(archive_path) is True

    def test_atomic_cleanup_on_error(self, temp_dir):
        """Test that temporary files are cleaned up on errors."""
        archive_path = temp_dir / "cleanup_test.tzst"

        # Try to create archive with non-existent files
        with pytest.raises(FileNotFoundError):
            create_archive(archive_path, ["non_existent_file.txt"], use_temp_file=True)

        # Archive should not exist
        assert not archive_path.exists()

        # No temporary files should be left behind
        temp_files = list(temp_dir.glob(".cleanup_test.tzst.*"))
        assert len(temp_files) == 0


class TestCompressionLevels:
    """Test compression level validation and functionality."""

    def test_compression_level_validation(self, sample_files, temp_dir):
        """Test compression level validation."""
        file_paths = [f for f in sample_files if f.is_file()]

        # Test valid compression levels
        for level in [1, 3, 10, 22]:
            archive_path = temp_dir / f"level_{level}.tzst"
            create_archive(archive_path, file_paths, compression_level=level)
            assert archive_path.exists()
            assert tzst_test_archive(archive_path) is True

        # Test invalid compression levels
        for invalid_level in [0, 23, -1, 100]:
            archive_path = temp_dir / f"invalid_{invalid_level}.tzst"
            with pytest.raises(ValueError) as exc_info:
                create_archive(
                    archive_path, file_paths, compression_level=invalid_level
                )

            assert "compression level" in str(exc_info.value).lower()
            assert "1" in str(exc_info.value) and "22" in str(exc_info.value)


class TestEdgeCaseCoverage:
    """Test edge cases to improve coverage."""

    def test_empty_files_list(self, temp_dir):
        """Test create_archive with empty files list."""
        archive_path = temp_dir / "empty.tzst"

        # Should create an empty archive
        create_archive(archive_path, [])

        assert archive_path.exists()
        contents = list_archive(archive_path)
        assert len(contents) == 0

    def test_create_archive_with_use_temp_file_false(self, temp_dir):
        """Test creating archive with use_temp_file=False."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        archive_path = temp_dir / "test.tzst"

        # Test non-atomic mode
        create_archive(archive_path, [str(test_file)], use_temp_file=False)

        assert archive_path.exists()
        contents = list_archive(archive_path)
        assert len(contents) == 1

    def test_extract_archive_to_specific_path(self, temp_dir):
        """Test extracting archive to specific path."""
        # Create test archive
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        archive_path = temp_dir / "test.tzst"
        create_archive(archive_path, [str(test_file)])

        # Extract to specific directory
        extract_dir = temp_dir / "extracted"
        extract_archive(archive_path, extract_dir)

        assert extract_dir.exists()
        assert (extract_dir / "test.txt").exists()
        assert (extract_dir / "test.txt").read_text() == "test content"

    def test_list_archive_with_streaming(self, temp_dir):
        """Test listing archive with streaming mode."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        archive_path = temp_dir / "test.tzst"
        create_archive(archive_path, [str(test_file)])

        # Test with streaming=True
        contents = list_archive(archive_path, streaming=True)
        assert len(contents) == 1
        assert contents[0]["name"] == "test.txt"

    def test_test_archive_success(self, temp_dir):
        """Test testing a valid archive."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        archive_path = temp_dir / "test.tzst"
        create_archive(archive_path, [str(test_file)])

        # Test archive - should return True for valid archive
        result = tzst_test_archive(archive_path)
        assert result is True

    def test_test_archive_failure(self, temp_dir):
        """Test testing an invalid archive."""
        # Create a file that's not a valid archive
        invalid_archive = temp_dir / "invalid.tzst"
        invalid_archive.write_text("This is not a valid archive")

        # Test archive - should return False for invalid archive
        result = tzst_test_archive(invalid_archive)
        assert result is False
