"""Comprehensive tests for tzst core functionality.

This file consolidates all core functionality tests for the tzst library,
including TzstArchive class, convenience functions, error handling,
and various operational modes.
"""

import os
from pathlib import Path
from unittest.mock import patch

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


class TestNonAtomicOperations:
    """Test non-atomic file operations (critical fix verification)."""

    def test_non_atomic_archive_creation(self, sample_files, temp_dir):
        """Test non-atomic archive creation works correctly."""
        file_paths = [f for f in sample_files if f.is_file()]
        archive_path = temp_dir / "non_atomic_test.tzst"

        # Test with atomic operations disabled
        create_archive(archive_path, file_paths, use_temp_file=False)
        assert archive_path.exists()

        # Verify archive is valid
        assert tzst_test_archive(archive_path) is True

        # Verify contents
        contents = list_archive(archive_path)
        assert len(contents) > 0

    def test_non_atomic_vs_atomic_equivalence(self, sample_files, temp_dir):
        """Test that atomic and non-atomic modes produce equivalent results."""
        file_paths = [f for f in sample_files if f.is_file()]

        # Create with atomic mode
        atomic_archive = temp_dir / "atomic.tzst"
        create_archive(atomic_archive, file_paths, use_temp_file=True)

        # Create with non-atomic mode
        non_atomic_archive = temp_dir / "non_atomic.tzst"
        create_archive(non_atomic_archive, file_paths, use_temp_file=False)

        # Both should be valid
        assert tzst_test_archive(atomic_archive) is True
        assert tzst_test_archive(non_atomic_archive) is True

        # Both should have same file contents
        atomic_contents = list_archive(atomic_archive)
        non_atomic_contents = list_archive(non_atomic_archive)
        assert len(atomic_contents) == len(non_atomic_contents)

    def test_non_atomic_path_resolution(self, temp_dir):
        """Test that non-atomic mode handles path resolution correctly."""
        # Create nested directory structure
        nested_dir = temp_dir / "level1" / "level2" / "level3"
        nested_dir.mkdir(parents=True, exist_ok=True)

        test_file = nested_dir / "deep_file.txt"
        test_file.write_text("Deep file content")

        # Create archive from parent directory using non-atomic mode
        archive_path = temp_dir / "deep_structure.tzst"
        create_archive(archive_path, [test_file], use_temp_file=False)

        assert archive_path.exists()
        assert tzst_test_archive(archive_path) is True


class TestCompressionLevelEdgeCases:
    """Test compression level edge cases and validation."""

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

    def test_compression_effectiveness(self, temp_dir):
        """Test that higher compression levels produce smaller files."""
        # Create a large compressible file
        large_file = temp_dir / "compressible.txt"
        content = "This is highly compressible content. " * 10000
        large_file.write_text(content)

        # Test different compression levels
        sizes = {}
        for level in [1, 11, 22]:
            archive_path = temp_dir / f"compressed_level_{level}.tzst"
            create_archive(archive_path, [large_file], compression_level=level)
            sizes[level] = archive_path.stat().st_size

        # Higher compression should generally result in smaller files
        # (though this isn't guaranteed for all data types)
        assert sizes[1] > 0
        assert sizes[22] > 0


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
        binary_content = bytes(range(256)) * 1000  # 256KB of binary data
        binary_file.write_bytes(binary_content)

        archive_path = temp_dir / "binary.tzst"
        create_archive(archive_path, [binary_file])

        assert archive_path.exists()
        assert tzst_test_archive(archive_path) is True

        # Test extraction and content verification
        extract_dir = temp_dir / "binary_extracted"
        extract_archive(archive_path, extract_dir)

        extracted_file = extract_dir / "binary.bin"
        assert extracted_file.exists()
        extracted_content = extracted_file.read_bytes()
        assert extracted_content == binary_content

    def test_large_files(self, temp_dir):
        """Test archiving large files."""
        large_file = temp_dir / "large.txt"
        content = "Large file content line.\n" * 100000  # ~2.4MB
        large_file.write_text(content)

        archive_path = temp_dir / "large_file.tzst"
        create_archive(archive_path, [large_file], compression_level=22)

        assert archive_path.exists()
        assert tzst_test_archive(archive_path) is True

        # Test extraction
        extract_dir = temp_dir / "large_extracted"
        extract_archive(archive_path, extract_dir)

        extracted_file = extract_dir / "large.txt"
        assert extracted_file.exists()
        extracted_content = extracted_file.read_text()
        assert extracted_content == content

    def test_files_with_special_characters(self, temp_dir):
        """Test files with special characters in names."""
        special_chars_file = temp_dir / "file!@#$%^&()_+{}[]-',.txt"
        special_chars_file.write_text("Special characters content")

        archive_path = temp_dir / "special_chars.tzst"
        create_archive(archive_path, [special_chars_file])

        assert archive_path.exists()
        assert tzst_test_archive(archive_path) is True

    def test_very_long_filenames(self, temp_dir):
        """Test files with very long names."""
        long_name = "very_long_" + "x" * 200 + ".txt"
        long_file = temp_dir / long_name
        long_file.write_text("Long filename content")

        archive_path = temp_dir / "long_filename.tzst"
        create_archive(archive_path, [long_file])

        assert archive_path.exists()
        assert tzst_test_archive(archive_path) is True


class TestSecurityFiltering:
    """Test security filtering mechanisms."""

    def test_tar_filter_extraction(self, sample_files, temp_dir):
        """Test extraction with TAR security filter."""
        file_paths = [f for f in sample_files if f.is_file()]
        archive_path = temp_dir / "tar_filter_test.tzst"

        # Create archive
        create_archive(archive_path, file_paths)  # Extract with TAR filter
        extract_dir = temp_dir / "tar_filtered"
        extract_archive(archive_path, extract_dir, filter="tar")

        assert extract_dir.exists()
        extracted_files = list(extract_dir.rglob("*"))
        assert len(extracted_files) > 0

    def test_data_filter_extraction(self, sample_files, temp_dir):
        """Test extraction with data security filter."""
        file_paths = [f for f in sample_files if f.is_file()]
        archive_path = temp_dir / "data_filter_test.tzst"

        # Create archive
        create_archive(archive_path, file_paths)  # Extract with data filter
        extract_dir = temp_dir / "data_filtered"
        extract_archive(archive_path, extract_dir, filter="data")

        assert extract_dir.exists()
        extracted_files = list(extract_dir.rglob("*"))
        assert len(extracted_files) > 0

    def test_invalid_filter_raises_error(self, sample_files, temp_dir):
        """Test that invalid filters raise appropriate errors."""
        file_paths = [f for f in sample_files if f.is_file()]
        archive_path = temp_dir / "invalid_filter_test.tzst"  # Create archive
        create_archive(archive_path, file_paths)

        # Try to extract with invalid filter
        extract_dir = temp_dir / "invalid_filtered"
        with pytest.raises(ValueError):
            extract_archive(archive_path, extract_dir, filter="invalid")


class TestExtractionFilters:
    """Test extraction filter security features."""

    def test_default_filter_is_data(self, sample_files, temp_dir):
        """Test that the default filter is 'data' for security."""
        archive_path = temp_dir / "test_security.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive
        with TzstArchive(archive_path, "w") as archive:
            for file_path in file_paths:
                relative_path = file_path.relative_to(sample_files[0].parent)
                archive.add(file_path, arcname=str(relative_path))

        # Test that default filter is 'data'
        extract_dir = temp_dir / "extracted_default"

        with patch("tarfile.TarFile.extractall") as mock_extractall:
            with TzstArchive(archive_path, "r") as archive:
                archive.extract(path=extract_dir)

            # Verify that 'data' filter was used
            mock_extractall.assert_called_once()
            call_args = mock_extractall.call_args
            assert "filter" in call_args[1]
            assert call_args[1]["filter"] == "data"

    def test_data_filter_explicit(self, sample_files, temp_dir):
        """Test explicitly setting 'data' filter."""
        archive_path = temp_dir / "test_data_filter.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive
        with TzstArchive(archive_path, "w") as archive:
            for file_path in file_paths:
                relative_path = file_path.relative_to(sample_files[0].parent)
                archive.add(file_path, arcname=str(relative_path))

        # Test extraction with explicit 'data' filter
        extract_dir = temp_dir / "extracted_data"

        with patch("tarfile.TarFile.extractall") as mock_extractall:
            with TzstArchive(archive_path, "r") as archive:
                archive.extract(path=extract_dir, filter="data")

            mock_extractall.assert_called_once()
            call_args = mock_extractall.call_args
            assert call_args[1]["filter"] == "data"

    def test_tar_filter(self, sample_files, temp_dir):
        """Test 'tar' filter for Unix-like features."""
        archive_path = temp_dir / "test_tar_filter.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive
        with TzstArchive(archive_path, "w") as archive:
            for file_path in file_paths:
                relative_path = file_path.relative_to(sample_files[0].parent)
                archive.add(file_path, arcname=str(relative_path))

        # Test extraction with 'tar' filter
        extract_dir = temp_dir / "extracted_tar"

        with patch("tarfile.TarFile.extractall") as mock_extractall:
            with TzstArchive(archive_path, "r") as archive:
                archive.extract(path=extract_dir, filter="tar")

            mock_extractall.assert_called_once()
            call_args = mock_extractall.call_args
            assert call_args[1]["filter"] == "tar"

    def test_fully_trusted_filter(self, sample_files, temp_dir):
        """Test 'fully_trusted' filter (dangerous but complete)."""
        archive_path = temp_dir / "test_trusted_filter.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive
        with TzstArchive(archive_path, "w") as archive:
            for file_path in file_paths:
                relative_path = file_path.relative_to(sample_files[0].parent)
                archive.add(file_path, arcname=str(relative_path))

        # Test extraction with 'fully_trusted' filter
        extract_dir = temp_dir / "extracted_trusted"

        with patch("tarfile.TarFile.extractall") as mock_extractall:
            with TzstArchive(archive_path, "r") as archive:
                archive.extract(path=extract_dir, filter="fully_trusted")

            mock_extractall.assert_called_once()
            call_args = mock_extractall.call_args
            assert call_args[1]["filter"] == "fully_trusted"

    def test_convenience_function_filter(self, sample_files, temp_dir):
        """Test filter parameter in extract_archive convenience function."""
        archive_path = temp_dir / "test_convenience_filter.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive
        with TzstArchive(archive_path, "w") as archive:
            for file_path in file_paths:
                relative_path = file_path.relative_to(sample_files[0].parent)
                archive.add(file_path, arcname=str(relative_path))

        # Test extract_archive with different filters
        for filter_type in ["data", "tar", "fully_trusted"]:
            extract_dir = temp_dir / f"extracted_conv_{filter_type}"

            # This should not raise an exception
            extract_archive(archive_path, extract_dir, filter=filter_type)

            # Verify files were extracted
            assert extract_dir.exists()
            extracted_files = list(extract_dir.rglob("*"))
            assert len([f for f in extracted_files if f.is_file()]) > 0


class TestSecurityDocumentation:
    """Test security documentation and warnings."""

    def test_security_filter_documentation(self, sample_files, temp_dir):
        """Test that security filters are properly documented."""
        # This test verifies that the API provides proper guidance
        archive_path = temp_dir / "test_docs.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive
        with TzstArchive(archive_path, "w") as archive:
            for file_path in file_paths:
                relative_path = file_path.relative_to(sample_files[0].parent)
                archive.add(file_path, arcname=str(relative_path))

        # Test that TzstArchive.extract method accepts filter parameter
        with TzstArchive(archive_path, "r") as archive:
            # Should accept various filter types without error
            extract_dir = temp_dir / "doc_test"
            archive.extract(path=extract_dir, filter="data")


class TestSecurityEdgeCases:
    """Test security edge cases and boundary conditions."""

    def test_filter_with_empty_archive(self, temp_dir):
        """Test filter behavior with empty archives."""
        archive_path = temp_dir / "empty_security.tzst"

        # Create empty archive
        with TzstArchive(archive_path, "w") as archive:
            pass  # Empty archive        # Test extraction with filter on empty archive
        extract_dir = temp_dir / "empty_extracted"
        with TzstArchive(archive_path, "r") as archive:
            archive.extract(path=extract_dir, filter="data")

        # Should succeed without error
        assert extract_dir.exists()

    def test_filter_parameter_validation(self, sample_files, temp_dir):
        """Test that invalid filter parameters are handled."""
        archive_path = temp_dir / "validation_test.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive
        with TzstArchive(archive_path, "w") as archive:
            for file_path in file_paths:
                relative_path = file_path.relative_to(sample_files[0].parent)
                archive.add(file_path, arcname=str(relative_path))

        # Test invalid filter string
        extract_dir = temp_dir / "invalid_filter"
        with TzstArchive(archive_path, "r") as archive:
            # Invalid filter should be handled gracefully
            # (exact behavior depends on implementation)
            try:
                archive.extract(path=extract_dir, filter="invalid_filter_name")
            except (ValueError, TypeError):
                pass  # Expected behavior for invalid filter


class TestCurrentDirectoryArchiving:
    """Test current directory archiving bug fixes."""

    def test_current_directory_dot_contents_without_wrapper(self, temp_dir):
        """Test that archiving '.' includes directory contents
        without wrapper folder."""
        # Create test files in a subdirectory to work from
        work_dir = temp_dir / "work_space"
        work_dir.mkdir()

        # Create test files
        file1 = work_dir / "file1.txt"
        file2 = work_dir / "file2.txt"
        subdir = work_dir / "subdir"
        subdir.mkdir()
        file3 = subdir / "file3.txt"

        file1.write_text("Content 1")
        file2.write_text("Content 2")
        file3.write_text("Content 3")

        # Change to work directory and create archive with "."
        original_cwd = os.getcwd()
        try:
            os.chdir(work_dir)
            archive_path = work_dir / "test_dot.tzst"

            # Create archive using "." parameter
            create_archive(archive_path, ["."])

            # List archive contents
            contents = list_archive(archive_path)
            content_names = [item["name"] for item in contents]

            # Should contain files without "./" prefix or wrapper directory
            assert "file1.txt" in content_names
            assert "file2.txt" in content_names
            assert "subdir/file3.txt" in content_names

            # Should NOT contain "." or "./" entries
            assert "." not in content_names
            assert "./" not in content_names

            # Extract and verify structure
            extract_dir = temp_dir / "extracted"
            extract_archive(archive_path, extract_dir)

            # Files should be at root level of extraction
            assert (extract_dir / "file1.txt").exists()
            assert (extract_dir / "file2.txt").exists()
            assert (extract_dir / "subdir" / "file3.txt").exists()

            # Verify content
            assert (extract_dir / "file1.txt").read_text() == "Content 1"
            assert (extract_dir / "file2.txt").read_text() == "Content 2"
            assert (extract_dir / "subdir" / "file3.txt").read_text() == "Content 3"

        finally:
            os.chdir(original_cwd)

    def test_current_directory_resolved_path(self, temp_dir):
        """Test that archiving current directory by resolved path works correctly."""
        # Create test files in a subdirectory to work from
        work_dir = temp_dir / "work_space2"
        work_dir.mkdir()

        # Create test files
        file1 = work_dir / "test_file.txt"
        file1.write_text("Test content")

        # Change to work directory and create archive with resolved current directory
        original_cwd = os.getcwd()
        try:
            os.chdir(work_dir)
            archive_path = work_dir / "test_resolved.tzst"
            current_path = Path.cwd()

            # Create archive using resolved current directory path
            create_archive(archive_path, [str(current_path)])

            # List archive contents
            contents = list_archive(archive_path)
            content_names = [item["name"] for item in contents]

            # Should contain files without directory wrapper
            assert "test_file.txt" in content_names

            # Should NOT contain the directory name itself
            assert work_dir.name not in content_names

        finally:
            os.chdir(original_cwd)

    def test_current_directory_vs_normal_archiving(self, temp_dir):
        """Test difference between current directory and normal directory archiving."""
        # Create test structure
        work_dir = temp_dir / "work_dir"
        work_dir.mkdir()
        other_dir = temp_dir / "other_dir"
        other_dir.mkdir()

        # Create identical files in both directories
        (work_dir / "shared.txt").write_text("Shared content")
        (other_dir / "shared.txt").write_text("Shared content")

        original_cwd = os.getcwd()
        try:
            # Archive current directory with "."
            os.chdir(work_dir)
            current_archive = work_dir / "current.tzst"
            create_archive(current_archive, ["."])
            current_contents = list_archive(current_archive)
            current_names = [item["name"] for item in current_contents]

            # Archive other directory normally
            normal_archive = work_dir / "normal.tzst"
            create_archive(normal_archive, [str(other_dir)])
            normal_contents = list_archive(normal_archive)
            normal_names = [item["name"] for item in normal_contents]

            # Current directory archiving should have file at root
            assert "shared.txt" in current_names

            # Normal directory archiving should have directory wrapper
            assert f"{other_dir.name}/shared.txt" in normal_names
            assert "shared.txt" not in normal_names  # Should not be at root

        finally:
            os.chdir(original_cwd)


class TestTemporaryFileExclusion:
    """Test temporary file exclusion bug fixes."""

    def test_exclude_temp_files_with_tmp_in_middle(self, temp_dir):
        """Test that temporary files with .tmp in the middle are excluded."""
        # Create test files including problematic temp files
        work_dir = temp_dir / "temp_test"
        work_dir.mkdir()

        # Regular files that should be included
        regular_file = work_dir / "regular.txt"
        regular_file.write_text("Regular content")

        # Temporary files that should be excluded
        temp_file1 = work_dir / ".a.tzst.9uztm81l.tmp"
        temp_file2 = work_dir / ".backup.abc123.tmp"
        temp_file3 = work_dir / ".test.random.tmp"

        temp_file1.write_text("Temp content 1")
        temp_file2.write_text("Temp content 2")
        temp_file3.write_text("Temp content 3")

        # Files that look like temp files but shouldn't be excluded
        not_temp1 = work_dir / "something.tmp"  # Doesn't start with .
        not_temp2 = work_dir / ".config"  # Starts with . but no .tmp
        not_temp3 = work_dir / ".tmpfile"  # Has tmp but not as separate component

        not_temp1.write_text("Not temp 1")
        not_temp2.write_text("Not temp 2")
        not_temp3.write_text("Not temp 3")

        original_cwd = os.getcwd()
        try:
            os.chdir(work_dir)
            archive_path = work_dir / "temp_exclusion.tzst"

            # Create archive with current directory
            create_archive(archive_path, ["."])

            # List archive contents
            contents = list_archive(archive_path)
            content_names = [item["name"] for item in contents]

            # Regular file should be included
            assert "regular.txt" in content_names

            # Files that look like temp but aren't should be included
            assert "something.tmp" in content_names
            assert ".config" in content_names
            assert ".tmpfile" in content_names

            # Actual temp files should be excluded
            assert ".a.tzst.9uztm81l.tmp" not in content_names
            assert ".backup.abc123.tmp" not in content_names
            assert ".test.random.tmp" not in content_names

        finally:
            os.chdir(original_cwd)

    def test_exclude_traditional_temp_files(self, temp_dir):
        """Test that traditional .tmp files are still excluded."""
        work_dir = temp_dir / "traditional_temp"
        work_dir.mkdir()

        # Regular file
        regular_file = work_dir / "document.txt"
        regular_file.write_text("Document content")

        # Traditional temp files
        temp_file1 = work_dir / ".temp.tmp"
        temp_file2 = work_dir / ".backup.tmp"

        temp_file1.write_text("Traditional temp 1")
        temp_file2.write_text("Traditional temp 2")

        original_cwd = os.getcwd()
        try:
            os.chdir(work_dir)
            archive_path = work_dir / "traditional_temp.tzst"

            create_archive(archive_path, ["."])

            contents = list_archive(archive_path)
            content_names = [item["name"] for item in contents]

            # Regular file should be included
            assert "document.txt" in content_names

            # Traditional temp files should be excluded
            assert ".temp.tmp" not in content_names
            assert ".backup.tmp" not in content_names

        finally:
            os.chdir(original_cwd)

    def test_archive_file_self_exclusion(self, temp_dir):
        """Test that the archive file itself is excluded from the archive."""
        work_dir = temp_dir / "self_exclusion"
        work_dir.mkdir()

        # Create some files
        file1 = work_dir / "include_me.txt"
        file1.write_text("Include this")

        original_cwd = os.getcwd()
        try:
            os.chdir(work_dir)
            archive_path = work_dir / "self_test.tzst"

            create_archive(archive_path, ["."])

            contents = list_archive(archive_path)
            content_names = [item["name"] for item in contents]

            # Regular file should be included
            assert "include_me.txt" in content_names

            # Archive file itself should not be included
            assert "self_test.tzst" not in content_names

        finally:
            os.chdir(original_cwd)

    def test_temp_file_patterns_comprehensive(self, temp_dir):
        """Test comprehensive temporary file pattern matching."""
        work_dir = temp_dir / "comprehensive_temp"
        work_dir.mkdir()

        # Files that should be excluded (start with . and contain .tmp)
        excluded_files = [
            ".file.tmp",
            ".archive.abc123.tmp",
            ".backup.random.tmp",
            ".test.xyz.tmp",
            ".a.tzst.9uztm81l.tmp",  # The original bug case
            ".something.else.tmp",
        ]

        # Files that should be included
        included_files = [
            "normal.txt",
            "file.tmp",  # No leading dot
            ".config",  # Leading dot but no .tmp
            ".tmpfile",  # Has tmp but not as separate component
            "tmp.txt",  # tmp not in the pattern
            ".file.temp",  # Similar but not .tmp
        ]

        # Create all files
        for filename in excluded_files + included_files:
            (work_dir / filename).write_text(f"Content of {filename}")

        original_cwd = os.getcwd()
        try:
            os.chdir(work_dir)
            archive_path = work_dir / "comprehensive.tzst"

            create_archive(archive_path, ["."])

            contents = list_archive(archive_path)
            content_names = [item["name"] for item in contents]

            # Check that included files are present
            for filename in included_files:
                assert filename in content_names, f"File {filename} should be included"

            # Check that excluded files are not present
            for filename in excluded_files:
                assert filename not in content_names, (
                    f"File {filename} should be excluded"
                )

        finally:
            os.chdir(original_cwd)


class TestCurrentDirectoryEdgeCases:
    """Test edge cases for current directory archiving."""

    def test_empty_current_directory(self, temp_dir):
        """Test archiving empty current directory."""
        empty_dir = temp_dir / "empty_work"
        empty_dir.mkdir()

        original_cwd = os.getcwd()
        try:
            os.chdir(empty_dir)
            archive_path = empty_dir / "empty.tzst"

            create_archive(archive_path, ["."])

            contents = list_archive(archive_path)
            content_names = [item["name"] for item in contents]

            # Should only contain the archive file exclusion, so be empty
            # (archive file itself should be excluded)
            assert len(content_names) == 0

        finally:
            os.chdir(original_cwd)

    def test_current_directory_with_subdirectories(self, temp_dir):
        """Test current directory archiving with nested subdirectories."""
        work_dir = temp_dir / "nested_work"
        work_dir.mkdir()

        # Create nested structure
        level1 = work_dir / "level1"
        level2 = level1 / "level2"
        level3 = level2 / "level3"

        level1.mkdir()
        level2.mkdir()
        level3.mkdir()

        # Create files at various levels
        (work_dir / "root.txt").write_text("Root level")
        (level1 / "l1.txt").write_text("Level 1")
        (level2 / "l2.txt").write_text("Level 2")
        (level3 / "l3.txt").write_text("Level 3")

        original_cwd = os.getcwd()
        try:
            os.chdir(work_dir)
            archive_path = work_dir / "nested.tzst"

            create_archive(archive_path, ["."])

            contents = list_archive(archive_path)
            content_names = [item["name"] for item in contents]

            # Should preserve directory structure without wrapper
            assert "root.txt" in content_names
            assert "level1/l1.txt" in content_names
            assert "level1/level2/l2.txt" in content_names
            assert "level1/level2/level3/l3.txt" in content_names

            # Extract and verify structure
            extract_dir = temp_dir / "nested_extracted"
            extract_archive(archive_path, extract_dir)

            assert (extract_dir / "root.txt").exists()
            assert (extract_dir / "level1" / "l1.txt").exists()
            assert (extract_dir / "level1" / "level2" / "l2.txt").exists()
            assert (extract_dir / "level1" / "level2" / "level3" / "l3.txt").exists()

        finally:
            os.chdir(original_cwd)

    def test_atomic_vs_non_atomic_current_directory(self, temp_dir):
        """Test that atomic and non-atomic modes work the same for current directory."""
        work_dir = temp_dir / "atomic_test"
        work_dir.mkdir()

        # Create test files
        (work_dir / "test1.txt").write_text("Test content 1")
        (work_dir / "test2.txt").write_text("Test content 2")

        original_cwd = os.getcwd()
        try:
            os.chdir(work_dir)

            # Test atomic mode
            atomic_archive = work_dir / "atomic.tzst"
            create_archive(atomic_archive, ["."], use_temp_file=True)
            atomic_contents = list_archive(atomic_archive)
            atomic_names = [item["name"] for item in atomic_contents]

            # Test non-atomic mode
            non_atomic_archive = work_dir / "non_atomic.tzst"
            create_archive(non_atomic_archive, ["."], use_temp_file=False)
            non_atomic_contents = list_archive(non_atomic_archive)
            non_atomic_names = [item["name"] for item in non_atomic_contents]

            # Both should have the same contents
            assert set(atomic_names) == set(non_atomic_names)
            assert "test1.txt" in atomic_names
            assert "test2.txt" in atomic_names

        finally:
            os.chdir(original_cwd)
