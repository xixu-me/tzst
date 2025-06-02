"""Tests to exercise conftest.py fixtures and improve coverage."""

from tzst import create_archive, extract_archive, list_archive
from tzst.core import TzstArchive


class TestConftestFixtures:
    """Test all conftest.py fixtures to improve coverage."""

    def test_comprehensive_test_files_fixture(self, comprehensive_test_files, temp_dir):
        """Test the comprehensive_test_files fixture."""
        # Ensure we have the expected file types
        assert len(comprehensive_test_files) >= 9

        file_names = [f.name for f in comprehensive_test_files]

        # Check for specific files that should be created
        assert "empty_file.txt" in file_names
        assert "whitespace_only.txt" in file_names
        assert "newlines_only.txt" in file_names
        assert "null_bytes.bin" in file_names
        assert "large_file.txt" in file_names
        assert "binary_data.bin" in file_names
        assert "file with spaces.txt" in file_names
        assert "unicode_content.txt" in file_names
        assert "deepest_file.txt" in file_names

        # Create archive with these comprehensive test files
        archive_path = temp_dir / "comprehensive.tzst"
        file_paths = [str(f) for f in comprehensive_test_files if f.is_file()]
        create_archive(archive_path, file_paths)

        # Verify archive was created and contains expected files
        assert archive_path.exists()
        contents = list_archive(archive_path)
        assert len(contents) >= 9

    def test_platform_specific_files_fixture(self, platform_specific_files, temp_dir):
        """Test the platform_specific_files fixture."""
        # This fixture may return empty list on Windows, non-empty on Unix
        # Just ensure it doesn't crash and returns a list
        assert isinstance(platform_specific_files, list)

        if platform_specific_files:
            # If we have platform-specific files, create an archive with them
            archive_path = temp_dir / "platform_specific.tzst"
            file_paths = [str(f) for f in platform_specific_files if f.is_file()]
            if file_paths:
                create_archive(archive_path, file_paths)
                assert archive_path.exists()

    def test_compression_test_files_fixture(self, compression_test_files, temp_dir):
        """Test the compression_test_files fixture."""
        assert len(compression_test_files) == 2

        file_names = [f.name for f in compression_test_files]
        assert "highly_compressible.txt" in file_names
        assert "poorly_compressible.bin" in file_names

        # Test different compression levels with these files
        for level in [1, 11, 22]:
            archive_path = temp_dir / f"compression_level_{level}.tzst"
            with TzstArchive(
                archive_path, mode="w", compression_level=level
            ) as archive:
                for file_path in compression_test_files:
                    if file_path.is_file():
                        archive.add(str(file_path), arcname=file_path.name)

            assert archive_path.exists()
            contents = list_archive(archive_path)
            assert len(contents) == 2

    def test_combined_fixtures_workflow(
        self, comprehensive_test_files, compression_test_files, temp_dir
    ):
        """Test using multiple fixtures together."""
        all_files = comprehensive_test_files + compression_test_files
        file_paths = [str(f) for f in all_files if f.is_file()]

        # Create archive with all files
        archive_path = temp_dir / "combined.tzst"
        create_archive(archive_path, file_paths)

        # Extract and verify
        extract_dir = temp_dir / "extracted"
        extract_archive(archive_path, extract_dir)
        # Verify archive was created and extracted directory exists
        assert archive_path.exists()
        assert extract_dir.exists()

        # Count files instead of checking exact names (due to nested structure)
        extracted_files = list(extract_dir.rglob("*"))
        extracted_file_count = len([f for f in extracted_files if f.is_file()])
        original_file_count = len([f for f in all_files if f.is_file()])

        # Should have extracted at least some files
        assert extracted_file_count > 0
        assert extracted_file_count <= original_file_count

    def test_unicode_content_file_handling(self, comprehensive_test_files, temp_dir):
        """Test handling of unicode content specifically."""
        unicode_files = [f for f in comprehensive_test_files if "unicode" in f.name]
        assert len(unicode_files) >= 1

        unicode_file = unicode_files[0]
        content = unicode_file.read_text(encoding="utf-8")
        assert "世界" in content
        assert "🌍" in content

        # Create archive and verify unicode handling
        archive_path = temp_dir / "unicode.tzst"
        create_archive(archive_path, [str(unicode_file)])

        # Extract and verify content is preserved
        extract_dir = temp_dir / "extracted_unicode"
        extract_archive(archive_path, extract_dir)

        extracted_file = extract_dir / unicode_file.name
        extracted_content = extracted_file.read_text(encoding="utf-8")
        assert extracted_content == content

    def test_special_character_filenames(self, comprehensive_test_files, temp_dir):
        """Test files with special characters in names."""
        special_files = [f for f in comprehensive_test_files if " " in f.name]
        assert len(special_files) >= 1

        archive_path = temp_dir / "special_chars.tzst"
        file_paths = [str(f) for f in special_files if f.is_file()]
        create_archive(archive_path, file_paths)

        contents = list_archive(archive_path)
        assert any(" " in item["name"] for item in contents)

    def test_deeply_nested_structure(self, comprehensive_test_files, temp_dir):
        """Test deeply nested directory structure."""
        nested_files = [f for f in comprehensive_test_files if "deepest" in f.name]
        assert len(nested_files) >= 1

        nested_file = nested_files[0]
        assert "nested" in str(nested_file.parent)

        # Create archive maintaining directory structure
        archive_path = temp_dir / "nested.tzst"
        with TzstArchive(archive_path, mode="w") as archive:
            archive.add(
                str(nested_file), arcname=str(nested_file.relative_to(temp_dir))
            )

        contents = list_archive(archive_path)
        assert any("nested" in item["name"] for item in contents)

    def test_empty_and_whitespace_files(self, comprehensive_test_files, temp_dir):
        """Test empty and whitespace-only files."""
        empty_files = [
            f
            for f in comprehensive_test_files
            if "empty" in f.name or "whitespace" in f.name or "newlines" in f.name
        ]
        assert len(empty_files) >= 3

        archive_path = temp_dir / "empty_whitespace.tzst"
        file_paths = [str(f) for f in empty_files if f.is_file()]
        create_archive(archive_path, file_paths)

        # Extract and verify these special cases are handled
        extract_dir = temp_dir / "extracted_empty"
        extract_archive(archive_path, extract_dir)

        for file_path in empty_files:
            if file_path.is_file():
                extracted_file = extract_dir / file_path.name
                assert extracted_file.exists()

    def test_binary_data_handling(self, comprehensive_test_files, temp_dir):
        """Test binary files with null bytes and binary data."""
        binary_files = [f for f in comprehensive_test_files if f.suffix == ".bin"]
        assert len(binary_files) >= 2

        archive_path = temp_dir / "binary.tzst"
        file_paths = [str(f) for f in binary_files if f.is_file()]
        create_archive(archive_path, file_paths)

        # Extract and verify binary content is preserved
        extract_dir = temp_dir / "extracted_binary"
        extract_archive(archive_path, extract_dir)

        for file_path in binary_files:
            if file_path.is_file():
                extracted_file = extract_dir / file_path.name
                assert extracted_file.exists()
                # Verify binary content is identical
                original_content = file_path.read_bytes()
                extracted_content = extracted_file.read_bytes()
                assert original_content == extracted_content

    def test_large_file_handling(self, comprehensive_test_files, temp_dir):
        """Test large file handling."""
        large_files = [f for f in comprehensive_test_files if "large" in f.name]
        assert len(large_files) >= 1

        large_file = large_files[0]
        # Verify it's actually large
        assert large_file.stat().st_size > 100000  # Should be > 100KB

        archive_path = temp_dir / "large.tzst"
        create_archive(archive_path, [str(large_file)])

        # Test with streaming mode
        archive_path_streaming = temp_dir / "large_streaming.tzst"
        with TzstArchive(archive_path_streaming, mode="w", streaming=True) as archive:
            archive.add(str(large_file), arcname=large_file.name)

        # Both archives should exist
        assert archive_path.exists()
        assert archive_path_streaming.exists()
