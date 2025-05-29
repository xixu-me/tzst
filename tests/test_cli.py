"""Tests for the CLI interface."""

import pytest

from tzst.cli import create_parser, main


class TestCLIParser:
    """Test CLI argument parsing."""

    def test_parser_creation(self):
        """Test that parser can be created."""
        parser = create_parser()
        assert parser is not None

    def test_add_command_parsing(self):
        """Test parsing of add command."""
        parser = create_parser()
        args = parser.parse_args(["a", "test.tzst", "file1.txt", "file2.txt"])

        assert args.command == "a"
        assert args.archive == "test.tzst"
        assert args.files == ["file1.txt", "file2.txt"]
        assert args.compression_level == 3  # default

    def test_extract_command_parsing(self):
        """Test parsing of extract command."""
        parser = create_parser()
        args = parser.parse_args(["x", "test.tzst", "-o", "output"])

        assert args.command == "x"
        assert args.archive == "test.tzst"
        assert args.output == "output"

    def test_list_command_parsing(self):
        """Test parsing of list command."""
        parser = create_parser()
        args = parser.parse_args(["l", "test.tzst", "-v"])

        assert args.command == "l"
        assert args.archive == "test.tzst"
        assert args.verbose is True

    def test_test_command_parsing(self):
        """Test parsing of test command."""
        parser = create_parser()
        args = parser.parse_args(["t", "test.tzst"])

        assert args.command == "t"
        assert args.archive == "test.tzst"


class TestCLICommands:
    """Test CLI command execution."""

    def test_add_command(self, sample_files, temp_dir):
        """Test add command functionality."""
        archive_path = temp_dir / "test.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]

        # Run add command
        result = main(["a", str(archive_path)] + file_paths)

        assert result == 0
        assert archive_path.exists()

    def test_list_command(self, sample_files, temp_dir):
        """Test list command functionality."""
        archive_path = temp_dir / "test.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]

        # Create archive first
        main(["a", str(archive_path)] + file_paths)

        # Run list command
        result = main(["l", str(archive_path)])

        assert result == 0

    def test_extract_command(self, sample_files, temp_dir):
        """Test extract command functionality."""
        archive_path = temp_dir / "test.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]
        extract_dir = temp_dir / "extracted"

        # Create archive first
        main(["a", str(archive_path)] + file_paths)

        # Run extract command
        result = main(["x", str(archive_path), "-o", str(extract_dir)])

        assert result == 0
        assert extract_dir.exists()

    def test_test_command(self, sample_files, temp_dir):
        """Test test command functionality."""
        archive_path = temp_dir / "test.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]

        # Create archive first
        main(["a", str(archive_path)] + file_paths)

        # Run test command
        result = main(["t", str(archive_path)])

        assert result == 0


class TestCLIErrorHandling:
    """Test CLI error handling."""

    def test_missing_archive(self, temp_dir):
        """Test handling of missing archive file."""
        fake_archive = temp_dir / "fake.tzst"

        result = main(["l", str(fake_archive)])
        assert result == 1

    def test_missing_files_to_add(self, temp_dir):
        """Test handling of missing files to add."""
        archive_path = temp_dir / "test.tzst"
        fake_file = temp_dir / "fake.txt"

        result = main(["a", str(archive_path), str(fake_file)])
        assert result == 1

    def test_no_command(self):
        """Test handling of no command provided."""
        result = main([])
        assert result == 1


class TestCLIAliases:
    """Test CLI command aliases."""

    def test_add_aliases(self, sample_files, temp_dir):
        """Test add command aliases."""
        archive_path = temp_dir / "test.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]

        # Test 'add' alias
        result = main(["add", str(archive_path)] + file_paths)
        assert result == 0

        # Test 'create' alias
        archive_path2 = temp_dir / "test2.tzst"
        result = main(["create", str(archive_path2)] + file_paths)
        assert result == 0

    def test_extract_aliases(self, sample_files, temp_dir):
        """Test extract command aliases."""
        archive_path = temp_dir / "test.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]
        extract_dir = temp_dir / "extracted"

        # Create archive first
        main(["a", str(archive_path)] + file_paths)

        # Test 'extract' alias
        result = main(["extract", str(archive_path), "-o", str(extract_dir)])
        assert result == 0

    def test_list_aliases(self, sample_files, temp_dir):
        """Test list command aliases."""
        archive_path = temp_dir / "test.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]

        # Create archive first
        main(["a", str(archive_path)] + file_paths)

        # Test 'list' alias
        result = main(["list", str(archive_path)])
        assert result == 0


@pytest.mark.integration
class TestCLIIntegration:
    """Integration tests for CLI."""

    def test_full_workflow(self, sample_files, temp_dir):
        """Test complete workflow: create, list, test, extract."""
        archive_path = temp_dir / "workflow.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]
        extract_dir = temp_dir / "workflow_extracted"

        # Create archive
        result = main(["a", str(archive_path)] + file_paths)
        assert result == 0
        assert archive_path.exists()

        # List contents
        result = main(["l", str(archive_path)])
        assert result == 0

        # Test integrity
        result = main(["t", str(archive_path)])
        assert result == 0

        # Extract
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0
        assert extract_dir.exists()

        # Verify extracted files exist and have correct content
        for file_path in sample_files:
            if file_path.is_file():
                relative_path = file_path.relative_to(sample_files[0].parent)
                extracted_file = extract_dir / relative_path
                assert extracted_file.exists()

                # Compare content
                original_content = file_path.read_bytes()
                extracted_content = extracted_file.read_bytes()
                assert original_content == extracted_content
