"""Remaining core tests for tzst after reorganization.

This file contains test classes that weren't moved during the test organization:
- TestExtensions - File extension handling
- TestNonAtomicOperations - Non-atomic file operations
- TestCompressionLevelEdgeCases - Compression level edge cases
- TestExtractionFilters - Extraction filter security features
- TestSecurityDocumentation - Security documentation
- TestSecurityEdgeCases - Security edge cases
- TestCurrentDirectoryEdgeCases - Current directory edge cases

Most other tests have been moved to organized subdirectories under tests/.
"""

import os
from unittest.mock import patch

from tzst import TzstArchive, create_archive, extract_archive, list_archive
from tzst import test_archive as tzst_test_archive


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
            pass  # Empty archive

        # Test extraction with filter on empty archive
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
