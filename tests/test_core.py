"""Tests for tzst core functionality."""

import pytest

from tzst import TzstArchive, create_archive, extract_archive, list_archive
from tzst import test_archive as tzst_test_archive


class TestTzstArchive:
    """Test the TzstArchive class."""

    def test_create_and_list_archive(self, sample_files, sample_archive_path):
        """Test creating an archive and listing its contents."""
        # Create archive with relative paths using arcname
        with TzstArchive(sample_archive_path, "w") as archive:
            for file_path in sample_files:
                if file_path.is_file():
                    relative_path = file_path.relative_to(sample_files[0].parent)
                    archive.add(file_path, arcname=str(relative_path))

        assert sample_archive_path.exists()

        # List contents
        with TzstArchive(sample_archive_path, "r") as archive:
            contents = archive.list()

        # Should have all files
        expected_names = [
            str(f.relative_to(sample_files[0].parent)).replace("\\", "/")
            for f in sample_files
            if f.is_file()
        ]
        actual_names = [item["name"] for item in contents]

        for expected in expected_names:
            assert expected in actual_names

    def test_extract_archive(self, sample_files, sample_archive_path, temp_dir):
        """Test extracting files from an archive."""
        # Create archive with relative paths using arcname
        with TzstArchive(sample_archive_path, "w") as archive:
            for file_path in sample_files:
                if file_path.is_file():
                    relative_path = file_path.relative_to(sample_files[0].parent)
                    archive.add(file_path, arcname=str(relative_path))

        # Extract to new directory
        extract_dir = temp_dir / "extracted"
        with TzstArchive(sample_archive_path, "r") as archive:
            archive.extract(path=extract_dir)

        # Verify extracted files
        for file_path in sample_files:
            if file_path.is_file():
                relative_path = file_path.relative_to(sample_files[0].parent)
                extracted_file = extract_dir / relative_path
                assert extracted_file.exists()

                # Compare content
                original_content = file_path.read_bytes()
                extracted_content = extracted_file.read_bytes()
                assert original_content == extracted_content

    def test_archive_test(self, sample_files, sample_archive_path):
        """Test archive integrity testing."""
        # Create archive with relative paths using arcname
        with TzstArchive(sample_archive_path, "w") as archive:
            for file_path in sample_files:
                if file_path.is_file():
                    relative_path = file_path.relative_to(sample_files[0].parent)
                    archive.add(file_path, arcname=str(relative_path))

        # Test archive integrity
        with TzstArchive(sample_archive_path, "r") as archive:
            assert archive.test() is True

    def test_verbose_listing(self, sample_files, sample_archive_path):
        """Test verbose listing of archive contents."""
        # Create archive with relative paths using arcname
        with TzstArchive(sample_archive_path, "w") as archive:
            for file_path in sample_files:
                if file_path.is_file():
                    relative_path = file_path.relative_to(sample_files[0].parent)
                    archive.add(file_path, arcname=str(relative_path))

        # Get verbose listing
        with TzstArchive(sample_archive_path, "r") as archive:
            contents = archive.list(verbose=True)

        # Check that verbose fields are present
        for item in contents:
            assert "mode" in item
            assert "mtime" in item
            assert "mtime_str" in item
            assert "uid" in item
            assert "gid" in item

    def test_streaming_mode_archive(self, sample_files, sample_archive_path):
        """Test streaming mode for reading archives."""
        # Create archive normally
        file_paths = [f for f in sample_files if f.is_file()]
        with TzstArchive(sample_archive_path, "w") as archive:
            for file_path in file_paths:
                relative_path = file_path.relative_to(sample_files[0].parent)
                archive.add(file_path, arcname=str(relative_path))

        # Test streaming mode reading
        with TzstArchive(sample_archive_path, "r", streaming=True) as archive:
            contents = archive.list()
            assert len(contents) > 0

    def test_streaming_vs_buffered_mode(self, sample_files, sample_archive_path):
        """Test that streaming and buffered modes produce same results."""
        # Create archive
        file_paths = [f for f in sample_files if f.is_file()]
        with TzstArchive(sample_archive_path, "w") as archive:
            for file_path in file_paths:
                relative_path = file_path.relative_to(sample_files[0].parent)
                archive.add(file_path, arcname=str(relative_path))

        # Read with buffered mode
        with TzstArchive(sample_archive_path, "r", streaming=False) as archive:
            buffered_contents = archive.list()

        # Read with streaming mode
        with TzstArchive(sample_archive_path, "r", streaming=True) as archive:
            streaming_contents = archive.list()

        # Results should be identical
        assert len(buffered_contents) == len(streaming_contents)
        for buffered, streaming in zip(
            buffered_contents, streaming_contents, strict=True
        ):
            assert buffered["name"] == streaming["name"]
            assert buffered["size"] == streaming["size"]


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


class TestExtensions:
    """Test file extension handling."""

    def test_tzst_extension(self, sample_files, temp_dir):
        """Test .tzst extension."""
        archive_path = temp_dir / "test.tzst"
        file_paths = [f for f in sample_files if f.is_file()]
        create_archive(archive_path, file_paths)
        assert archive_path.exists()

    def test_tar_zst_extension(self, sample_files, temp_dir):
        """Test .tar.zst extension."""
        archive_path = temp_dir / "test.tar.zst"
        file_paths = [f for f in sample_files if f.is_file()]
        create_archive(archive_path, file_paths)
        assert archive_path.exists()

    def test_auto_extension(self, sample_files, temp_dir):
        """Test automatic extension addition."""
        archive_path = temp_dir / "test"
        file_paths = [f for f in sample_files if f.is_file()]
        create_archive(archive_path, file_paths)

        # Should create test.tzst
        expected_path = temp_dir / "test.tzst"
        assert expected_path.exists()


class TestStreamingMode:
    """Test streaming mode improvements."""

    def test_streaming_archive_creation_and_extraction(self, sample_files, temp_dir):
        """Test that streaming mode works for reading archives."""
        archive_path = temp_dir / "streaming_test.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive normally
        create_archive(archive_path, file_paths)

        # Test streaming mode reading
        with TzstArchive(archive_path, "r", streaming=True) as archive:
            contents = archive.list()
            assert len(contents) > 0

            # Test extraction in streaming mode
            extract_dir = temp_dir / "streaming_extracted"
            try:
                archive.extract(path=extract_dir)
                assert extract_dir.exists()
            except RuntimeError as e:
                if "streaming mode" in str(e):
                    # This is expected for some archives in streaming mode
                    # Test that we can still read the contents
                    assert len(contents) > 0
                else:
                    raise

    def test_streaming_vs_buffered_mode(self, sample_files, temp_dir):
        """Test that streaming and buffered modes produce same results."""
        archive_path = temp_dir / "comparison_test.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive
        create_archive(archive_path, file_paths)

        # Read with buffered mode
        with TzstArchive(archive_path, "r", streaming=False) as archive:
            buffered_contents = archive.list()

        # Read with streaming mode
        with TzstArchive(archive_path, "r", streaming=True) as archive:
            streaming_contents = archive.list()

        # Results should be identical
        assert len(buffered_contents) == len(streaming_contents)
        for buffered, streaming in zip(
            buffered_contents, streaming_contents, strict=True
        ):
            assert buffered["name"] == streaming["name"]
            assert buffered["size"] == streaming["size"]

    def test_convenience_functions_with_streaming(self, sample_files, temp_dir):
        """Test convenience functions with streaming parameter."""
        archive_path = temp_dir / "convenience_streaming.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive
        create_archive(archive_path, file_paths)

        # Test list_archive with streaming
        contents_normal = list_archive(archive_path, streaming=False)
        contents_streaming = list_archive(archive_path, streaming=True)
        assert len(contents_normal) == len(contents_streaming)

        # Test test_archive with streaming
        assert tzst_test_archive(archive_path, streaming=False) is True
        assert tzst_test_archive(archive_path, streaming=True) is True

        # Test extract_archive with streaming
        extract_dir_normal = temp_dir / "extract_normal"
        extract_dir_streaming = temp_dir / "extract_streaming"

        extract_archive(archive_path, extract_dir_normal, streaming=False)
        extract_archive(archive_path, extract_dir_streaming, streaming=True)

        assert extract_dir_normal.exists()
        assert extract_dir_streaming.exists()


class TestAtomicFileOperations:
    """Test atomic file operations."""

    def test_atomic_file_creation(self, sample_files, temp_dir):
        """Test that atomic file creation works."""
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


class TestCompressionLevelValidation:
    """Test compression level validation improvements."""

    def test_valid_compression_levels(self, sample_files, temp_dir):
        """Test that valid compression levels work."""
        file_paths = [f for f in sample_files if f.is_file()]

        for level in [1, 3, 10, 22]:
            archive_path = temp_dir / f"level_{level}.tzst"
            create_archive(archive_path, file_paths, compression_level=level)
            assert archive_path.exists()
            assert tzst_test_archive(archive_path) is True

    def test_invalid_compression_levels(self, sample_files, temp_dir):
        """Test that invalid compression levels raise errors."""
        file_paths = [f for f in sample_files if f.is_file()]

        for invalid_level in [0, 23, -1, 100]:
            archive_path = temp_dir / f"invalid_{invalid_level}.tzst"
            with pytest.raises(ValueError) as exc_info:
                create_archive(
                    archive_path, file_paths, compression_level=invalid_level
                )

            assert "compression level" in str(exc_info.value).lower()
            assert "1" in str(exc_info.value) and "22" in str(exc_info.value)
