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
