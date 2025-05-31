"""Tests for security features and extraction filters."""

from unittest.mock import patch

from tzst import TzstArchive, extract_archive


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

    def test_none_filter_with_warning(self, sample_files, temp_dir, capsys):
        """Test None filter shows deprecation warning."""
        archive_path = temp_dir / "test_none_filter.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive
        with TzstArchive(archive_path, "w") as archive:
            for file_path in file_paths:
                relative_path = file_path.relative_to(sample_files[0].parent)
                archive.add(file_path, arcname=str(relative_path))

        # Test extraction with None filter
        extract_dir = temp_dir / "extracted_none"

        with patch("tarfile.TarFile.extractall") as mock_extractall:
            with TzstArchive(archive_path, "r") as archive:
                archive.extract(path=extract_dir, filter=None)

            mock_extractall.assert_called_once()
            call_args = mock_extractall.call_args
            assert call_args[1]["filter"] is None

    def test_custom_filter_function(self, sample_files, temp_dir):
        """Test custom filter function."""
        archive_path = temp_dir / "test_custom_filter.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive
        with TzstArchive(archive_path, "w") as archive:
            for file_path in file_paths:
                relative_path = file_path.relative_to(sample_files[0].parent)
                archive.add(file_path, arcname=str(relative_path))

        # Define custom filter function
        def custom_filter(member, path):
            """Custom filter that only allows regular files."""
            if member.isfile():
                return member
            return None

        # Test extraction with custom filter
        extract_dir = temp_dir / "extracted_custom"

        with patch("tarfile.TarFile.extractall") as mock_extractall:
            with TzstArchive(archive_path, "r") as archive:
                archive.extract(path=extract_dir, filter=custom_filter)

            mock_extractall.assert_called_once()
            call_args = mock_extractall.call_args
            assert call_args[1]["filter"] == custom_filter

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
    """Test security-related documentation and warnings."""

    def test_extract_method_has_security_warning(self):
        """Test that extract method has proper security warning in docstring."""
        docstring = TzstArchive.extract.__doc__
        assert docstring is not None
        assert "Never extract archives from untrusted sources" in docstring
        assert "filter" in docstring
        assert "data" in docstring

    def test_extract_archive_has_security_warning(self):
        """Test that extract_archive function has proper security warning."""
        docstring = extract_archive.__doc__
        assert docstring is not None
        assert "Never extract archives from untrusted sources" in docstring
        assert "path traversal attacks" in docstring
        assert "data" in docstring


class TestSecurityEdgeCases:
    """Test edge cases and error conditions for security features."""

    def test_streaming_mode_filter_compatibility(self, sample_files, temp_dir):
        """Test that filters work correctly with streaming mode."""
        archive_path = temp_dir / "test_streaming_filter.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive
        with TzstArchive(archive_path, "w") as archive:
            for file_path in file_paths:
                relative_path = file_path.relative_to(sample_files[0].parent)
                archive.add(file_path, arcname=str(relative_path))

        # Test extraction in streaming mode with filter
        extract_dir = temp_dir / "extracted_streaming"

        # This should work without errors
        with TzstArchive(archive_path, "r", streaming=True) as archive:
            archive.extract(path=extract_dir, filter="data")

        # Verify files were extracted
        assert extract_dir.exists()
        extracted_files = list(extract_dir.rglob("*"))
        assert len([f for f in extracted_files if f.is_file()]) > 0

    def test_filter_with_specific_member_extraction(self, sample_files, temp_dir):
        """Test filter when extracting specific members."""
        archive_path = temp_dir / "test_member_filter.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive
        with TzstArchive(archive_path, "w") as archive:
            for file_path in file_paths:
                relative_path = file_path.relative_to(sample_files[0].parent)
                archive.add(file_path, arcname=str(relative_path))

        # Test extracting specific member with filter
        extract_dir = temp_dir / "extracted_member"

        if file_paths:
            with TzstArchive(archive_path, "r") as archive:
                members = archive.getnames()
                if members:
                    # Extract first member with data filter
                    archive.extract(member=members[0], path=extract_dir, filter="data")
                    # Verify file was extracted
                    assert extract_dir.exists()
                    extracted_file = extract_dir / members[0]
                    assert extracted_file.exists()
