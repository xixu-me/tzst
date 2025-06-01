"""Tests for TzstArchive class core functionality."""

from tzst import TzstArchive


class TestBasicImportAndCreation:
    """Test basic import and creation functionality."""

    def test_simple_import(self):
        """Test that we can import TzstArchive."""
        assert TzstArchive is not None

    def test_simple_creation(self):
        """Test simple TzstArchive creation."""
        archive = TzstArchive("test.tzst")
        assert archive.filename.name == "test.tzst"
        assert archive.mode == "r"


class TestTzstArchiveBasics:
    """Test basic TzstArchive class functionality."""

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


class TestTzstArchiveStreamingMode:
    """Test streaming mode functionality."""

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
