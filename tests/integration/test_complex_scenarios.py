"""Integration tests for tzst complex scenarios."""

import os

import pytest

from tzst import create_archive, extract_archive, list_archive
from tzst import test_archive as tzst_test_archive


class TestCurrentDirectoryArchiving:
    """Test current directory archiving bug fixes."""

    def test_current_directory_dot_contents_without_wrapper(self, temp_dir):
        """Test that archiving '.' includes directory contents without wrapper folder."""
        # Create test structure
        work_dir = temp_dir / "work_space"
        work_dir.mkdir()

        # Create test files
        file1 = work_dir / "file1.txt"
        file1.write_text("Content 1")
        file2 = work_dir / "file2.txt"
        file2.write_text("Content 2")

        # Create subdirectory with file
        subdir = work_dir / "subdir"
        subdir.mkdir()
        file3 = subdir / "file3.txt"
        file3.write_text("Content 3")

        # Change to work directory and create archive
        original_cwd = os.getcwd()
        try:
            os.chdir(work_dir)
            archive_path = work_dir / "test.tzst"

            # Create archive with current directory
            create_archive(archive_path, ["."])

            # List archive contents
            contents = list_archive(archive_path)
            content_names = [item["name"] for item in contents]

            # Should NOT contain a wrapper directory, just file contents
            assert "file1.txt" in content_names
            assert "file2.txt" in content_names
            assert "subdir/file3.txt" in content_names

            # Should NOT contain the work directory name itself
            assert work_dir.name not in content_names

            # Extract and verify structure
            extract_dir = temp_dir / "extracted"
            extract_archive(archive_path, extract_dir)

            # Verify content
            assert (extract_dir / "file1.txt").read_text() == "Content 1"
            assert (extract_dir / "file2.txt").read_text() == "Content 2"
            assert (extract_dir / "subdir" / "file3.txt").read_text() == "Content 3"

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


@pytest.mark.integration
class TestLargeFileOperations:
    """Integration tests for large file operations."""

    def test_large_archive_creation_and_extraction(self, temp_dir):
        """Test creating and extracting archives with multiple large files."""
        # Create multiple large files
        large_files = []
        for i in range(3):
            large_file = temp_dir / f"large_{i}.txt"
            content = f"Large file {i} content line.\n" * 50000  # ~1.2MB each
            large_file.write_text(content)
            large_files.append(large_file)

        # Create archive with high compression
        archive_path = temp_dir / "large_files.tzst"
        create_archive(archive_path, large_files, compression_level=22)

        assert archive_path.exists()
        assert tzst_test_archive(archive_path) is True

        # Extract and verify
        extract_dir = temp_dir / "large_extracted"
        extract_archive(archive_path, extract_dir)

        for i, original_file in enumerate(large_files):
            extracted_file = extract_dir / f"large_{i}.txt"
            assert extracted_file.exists()
            assert extracted_file.read_text() == original_file.read_text()


@pytest.mark.integration
class TestComplexDirectoryStructures:
    """Integration tests for complex directory structures."""

    def test_deeply_nested_directories(self, temp_dir):
        """Test archiving deeply nested directory structures."""
        # Create deep nested structure
        current_dir = temp_dir / "deep"
        current_dir.mkdir()

        for level in range(10):  # 10 levels deep
            current_dir = current_dir / f"level_{level}"
            current_dir.mkdir()

            # Add a file at each level
            test_file = current_dir / f"file_at_level_{level}.txt"
            test_file.write_text(f"Content at level {level}")

        # Archive the entire structure
        archive_path = temp_dir / "deep_structure.tzst"
        create_archive(archive_path, [temp_dir / "deep"])

        assert archive_path.exists()
        assert tzst_test_archive(archive_path) is True

        # Extract and verify structure is preserved
        extract_dir = temp_dir / "deep_extracted"
        extract_archive(archive_path, extract_dir)

        # Verify deep structure
        test_deep_file = extract_dir / "deep"
        for level in range(10):
            test_deep_file = test_deep_file / f"level_{level}"
            file_at_level = test_deep_file / f"file_at_level_{level}.txt"
            assert file_at_level.exists()
            assert file_at_level.read_text() == f"Content at level {level}"
