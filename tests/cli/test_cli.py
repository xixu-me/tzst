"""Comprehensive tests for tzst CLI interface.

This file consolidates all CLI-related tests to eliminate duplication
and provide a single source of truth for CLI testing.
"""

import argparse

import pytest

from tzst.cli import (
    create_parser,
    format_size,
    main,
    print_banner,
    validate_compression_level,
)


class TestUtilityFunctions:
    """Test CLI utility functions."""

    def test_format_size_bytes(self):
        """Test format_size with byte values."""
        assert format_size(0) == "   0.0 B"
        assert format_size(1) == "   1.0 B"
        assert format_size(999) == " 999.0 B"

    def test_format_size_kilobytes(self):
        """Test format_size with kilobyte values."""
        assert format_size(1024) == "   1.0 KB"
        assert format_size(1536) == "   1.5 KB"
        assert format_size(2048) == "   2.0 KB"

    def test_format_size_megabytes(self):
        """Test format_size with megabyte values."""
        assert format_size(1024 * 1024) == "   1.0 MB"
        mb_1_5 = int(1.5 * 1024 * 1024)
        assert format_size(mb_1_5) == "   1.5 MB"

    def test_format_size_gigabytes(self):
        """Test format_size with gigabyte values."""
        assert format_size(1024 * 1024 * 1024) == "   1.0 GB"
        gb_2_5 = int(2.5 * 1024 * 1024 * 1024)
        assert format_size(gb_2_5) == "   2.5 GB"

    def test_format_size_terabytes(self):
        """Test format_size with terabyte values."""
        tb_size = 1024 * 1024 * 1024 * 1024
        assert format_size(tb_size) == "   1.0 TB"

    def test_format_size_petabytes(self):
        """Test format_size with very large values (petabytes)."""
        huge_size = 1024 * 1024 * 1024 * 1024 * 1024 * 2
        result = format_size(huge_size)
        assert result.endswith(" PB")
        assert "2.0" in result

    def test_print_banner_output(self, capsys):
        """Test print_banner function output."""
        print_banner()
        captured = capsys.readouterr()

        # Should print empty line, version line, empty line
        lines = captured.out.split("\n")
        assert len(lines) >= 3
        assert lines[0] == ""  # Empty line
        assert "tzst" in lines[1]
        assert "Copyright" in lines[1]
        assert lines[2] == ""  # Empty line

    def test_validate_compression_level_valid(self):
        """Test validate_compression_level with valid levels."""
        assert validate_compression_level("1") == 1
        assert validate_compression_level("11") == 11
        assert validate_compression_level("22") == 22

    def test_validate_compression_level_invalid_range(self):
        """Test validate_compression_level with out-of-range values."""
        with pytest.raises(
            argparse.ArgumentTypeError, match="Invalid compression level: 0"
        ):
            validate_compression_level("0")

        with pytest.raises(
            argparse.ArgumentTypeError, match="Invalid compression level: 23"
        ):
            validate_compression_level("23")

    def test_validate_compression_level_invalid_format(self):
        """Test validate_compression_level with non-numeric values."""
        with pytest.raises(
            argparse.ArgumentTypeError, match="Invalid compression level: 'abc'"
        ):
            validate_compression_level("abc")

        with pytest.raises(
            argparse.ArgumentTypeError, match="Invalid compression level: '1.5'"
        ):
            validate_compression_level("1.5")


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
        result = main(["a", str(archive_path), *file_paths])

        assert result == 0
        assert archive_path.exists()

    def test_list_command(self, sample_files, temp_dir):
        """Test list command functionality."""
        archive_path = temp_dir / "test.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]

        # Create archive first
        main(["a", str(archive_path), *file_paths])

        # Run list command
        result = main(["l", str(archive_path)])

        assert result == 0

    def test_extract_command(self, sample_files, temp_dir):
        """Test extract command functionality."""
        archive_path = temp_dir / "test.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]
        extract_dir = temp_dir / "extracted"

        # Create archive first
        main(["a", str(archive_path), *file_paths])

        # Run extract command
        result = main(["x", str(archive_path), "-o", str(extract_dir)])

        assert result == 0
        assert extract_dir.exists()

    def test_test_command(self, sample_files, temp_dir):
        """Test test command functionality."""
        archive_path = temp_dir / "test.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]

        # Create archive first
        main(["a", str(archive_path), *file_paths])

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

    def test_keyboard_interrupt_handling(self, temp_dir):
        """Test that KeyboardInterrupt is handled properly."""
        # This test is more conceptual since we can't easily simulate KeyboardInterrupt
        # in a unit test, but we can verify the error handling structure exists
        from tzst.cli import cmd_add

        # Create a mock args object
        class MockArgs:
            def __init__(self):
                self.archive = str(temp_dir / "interrupt_test.tzst")
                self.files = ["non_existent_file.txt"]
                self.compression_level = 3

        # Test that the function handles FileNotFoundError properly
        result = cmd_add(MockArgs())
        assert result == 1  # Should return error code for missing files


class TestCLIAliases:
    """Test CLI command aliases."""

    def test_add_aliases(self, sample_files, temp_dir):
        """Test add command aliases."""
        archive_path = temp_dir / "test.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]

        # Test 'add' alias
        result = main(["add", str(archive_path), *file_paths])
        assert result == 0

        # Test 'create' alias
        archive_path2 = temp_dir / "test2.tzst"
        result = main(["create", str(archive_path2), *file_paths])
        assert result == 0

    def test_extract_aliases(self, sample_files, temp_dir):
        """Test extract command aliases."""
        archive_path = temp_dir / "test.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]
        extract_dir = temp_dir / "extracted"

        # Create archive first
        main(["a", str(archive_path), *file_paths])

        # Test 'extract' alias
        result = main(["extract", str(archive_path), "-o", str(extract_dir)])
        assert result == 0

    def test_list_aliases(self, sample_files, temp_dir):
        """Test list command aliases."""
        archive_path = temp_dir / "test.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]

        # Create archive first
        main(["a", str(archive_path), *file_paths])

        # Test 'list' alias
        result = main(["list", str(archive_path)])
        assert result == 0


class TestCLIHelp:
    """Test CLI help and documentation."""

    def test_help_command(self):
        """Test help command execution."""
        # Test main help
        result = main(["--help"])  # Help should exit successfully
        assert result == 0

    def test_help_contains_security_info(self, capsys):
        """Test that help output contains security information."""
        try:
            main(["--help"])
        except SystemExit:
            pass  # Help exits with SystemExit

        captured = capsys.readouterr()
        help_output = captured.out + captured.err

        # Should mention security filters
        assert "filter" in help_output.lower() or "security" in help_output.lower()

    def test_command_specific_help(self):
        """Test command-specific help if available."""
        # Some CLI implementations support command-specific help
        # This test can be extended based on actual implementation
        pass


@pytest.mark.integration
class TestCLIIntegration:
    """Integration tests for CLI."""

    def test_full_workflow(self, sample_files, temp_dir):
        """Test complete workflow: create, list, test, extract."""
        archive_path = temp_dir / "workflow.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()]
        extract_dir = temp_dir / "workflow_extracted"

        # Create archive
        result = main(["a", str(archive_path), *file_paths])
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


class TestCLIStreamingOptions:
    """Test CLI streaming options."""

    def test_extract_streaming_flag(self, sample_files, temp_dir):
        """Test extract command with streaming flag."""
        archive_path = temp_dir / "cli_streaming_test.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive first
        from tzst import create_archive

        create_archive(archive_path, file_paths)

        # Test extract with streaming
        parser = create_parser()
        args = parser.parse_args(
            ["x", str(archive_path), "--streaming", "-o", str(temp_dir / "extracted")]
        )

        assert args.command == "x"
        assert hasattr(args, "streaming")
        assert args.streaming is True

    def test_list_streaming_flag(self, sample_files, temp_dir):
        """Test list command with streaming flag."""
        archive_path = temp_dir / "cli_list_streaming.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive first
        from tzst import create_archive

        create_archive(archive_path, file_paths)

        # Test list with streaming
        parser = create_parser()
        args = parser.parse_args(["l", str(archive_path), "--streaming"])

        assert args.command == "l"
        assert hasattr(args, "streaming")
        assert args.streaming is True

    def test_test_streaming_flag(self, sample_files, temp_dir):
        """Test test command with streaming flag."""
        archive_path = temp_dir / "cli_test_streaming.tzst"
        file_paths = [f for f in sample_files if f.is_file()]

        # Create archive first
        from tzst import create_archive

        create_archive(archive_path, file_paths)

        # Test test command with streaming
        parser = create_parser()
        args = parser.parse_args(["t", str(archive_path), "--streaming"])

        assert args.command == "t"
        assert hasattr(args, "streaming")
        assert args.streaming is True


class TestCLICompressionLevels:
    """Test CLI compression level handling."""

    def test_valid_compression_levels(self, sample_files, temp_dir):
        """Test various valid compression levels."""
        file_paths = [str(f) for f in sample_files if f.is_file()]

        # Test compression levels 1, 3, 10, 22
        for level in [1, 3, 10, 22]:
            archive_path = temp_dir / f"level_{level}.tzst"
            result = main(["a", str(archive_path), *file_paths, "-l", str(level)])
            assert result == 0
            assert archive_path.exists()


class TestCLIAtomicOperations:
    """Test CLI atomic and non-atomic operations."""

    def test_no_atomic_flag(self, sample_files, temp_dir):
        """Test --no-atomic flag functionality."""
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "no_atomic.tzst"

        # Test --no-atomic flag
        result = main(["a", str(archive_path), *file_paths, "--no-atomic"])
        assert result == 0
        assert archive_path.exists()

        # Verify archive integrity
        result = main(["t", str(archive_path)])
        assert result == 0

    def test_atomic_vs_no_atomic_results(self, sample_files, temp_dir):
        """Test that atomic and non-atomic modes produce equivalent archives."""
        file_paths = [str(f) for f in sample_files if f.is_file()]

        # Create archive with atomic mode (default)
        atomic_archive = temp_dir / "atomic.tzst"
        result = main(["a", str(atomic_archive), *file_paths])
        assert result == 0

        # Create archive with non-atomic mode
        non_atomic_archive = temp_dir / "non_atomic.tzst"
        result = main(["a", str(non_atomic_archive), *file_paths, "--no-atomic"])
        assert result == 0

        # Both archives should be valid and contain same files
        result_atomic = main(["t", str(atomic_archive)])
        result_non_atomic = main(["t", str(non_atomic_archive)])
        assert result_atomic == 0
        assert result_non_atomic == 0


class TestCLISecurityFilters:
    """Test CLI security filtering options."""

    def test_tar_filter(self, sample_files, temp_dir):
        """Test --filter tar option."""
        # First create an archive
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "filter_test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Test extraction with tar filter
        extract_dir = temp_dir / "tar_filtered"
        result = main(
            ["x", str(archive_path), "-o", str(extract_dir), "--filter", "tar"]
        )
        assert result == 0
        assert extract_dir.exists()

    def test_data_filter(self, sample_files, temp_dir):
        """Test --filter data option."""
        # First create an archive
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "filter_test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Test extraction with data filter
        extract_dir = temp_dir / "data_filtered"
        result = main(
            ["x", str(archive_path), "-o", str(extract_dir), "--filter", "data"]
        )
        assert result == 0
        assert extract_dir.exists()

    def test_invalid_filter(self, sample_files, temp_dir):
        """Test invalid filter option returns error."""
        # First create an archive
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "filter_test.tzst"
        main(
            ["a", str(archive_path), *file_paths]
        )  # Test extraction with invalid filter
        extract_dir = temp_dir / "invalid_filtered"
        result = main(
            ["x", str(archive_path), "-o", str(extract_dir), "--filter", "invalid"]
        )
        assert result == 2  # Should fail with argparse error code


class TestCLIStreamingOperations:
    """Test CLI streaming operations."""

    def test_list_streaming(self, sample_files, temp_dir):
        """Test list command with --streaming flag."""
        # First create an archive
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "streaming_test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Test list with streaming
        result = main(["l", str(archive_path), "--streaming"])
        assert result == 0

    def test_test_streaming(self, sample_files, temp_dir):
        """Test test command with --streaming flag."""
        # First create an archive
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "streaming_test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Test archive integrity with streaming
        result = main(["t", str(archive_path), "--streaming"])
        assert result == 0

    def test_extract_streaming(self, sample_files, temp_dir):
        """Test extract command with --streaming flag."""
        # First create an archive
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "streaming_test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Test extraction with streaming
        extract_dir = temp_dir / "streaming_extracted"
        result = main(["x", str(archive_path), "-o", str(extract_dir), "--streaming"])
        assert result == 0
        assert extract_dir.exists()


class TestCLISpecialFiles:
    """Test CLI with special file types and names."""

    def test_empty_files(self, temp_dir):
        """Test archiving empty files."""
        # Create empty file
        empty_file = temp_dir / "empty.txt"
        empty_file.touch()

        archive_path = temp_dir / "empty_test.tzst"
        result = main(["a", str(archive_path), str(empty_file)])
        assert result == 0
        assert archive_path.exists()

    def test_files_with_spaces_and_special_chars(self, temp_dir):
        """Test files with spaces and special characters."""
        # Create file with special characters
        special_file = temp_dir / "file with spaces & special chars!@#$%.txt"
        special_file.write_text("Special file content")

        archive_path = temp_dir / "special_chars.tzst"
        result = main(["a", str(archive_path), str(special_file)])
        assert result == 0

    def test_very_long_filenames(self, temp_dir):
        """Test files with very long names."""
        # Create file with very long name
        long_name = "long_" + "x" * 200 + ".txt"
        long_file = temp_dir / long_name
        long_file.write_text("Long filename content")

        archive_path = temp_dir / "long_filename.tzst"
        result = main(["a", str(archive_path), str(long_file)])
        assert result == 0

    def test_files_with_dots(self, temp_dir):
        """Test files with multiple dots in name."""
        # Create file with multiple dots
        dotted_file = temp_dir / "multiple.dots.in.name.txt"
        dotted_file.write_text("Dotted file content")

        archive_path = temp_dir / "dotted.tzst"
        result = main(["a", str(archive_path), str(dotted_file)])
        assert result == 0


class TestCLILargeFiles:
    """Test CLI with large files."""

    def test_large_text_file(self, temp_dir):
        """Test archiving large text files."""
        # Create large text file (1MB+)
        large_file = temp_dir / "large.txt"
        content = "This is a large file content.\n" * 50000
        large_file.write_text(content)

        archive_path = temp_dir / "large_file.tzst"
        result = main(["a", str(archive_path), str(large_file), "-l", "22"])
        assert result == 0
        assert archive_path.exists()

    def test_binary_file(self, temp_dir):
        """Test archiving binary files."""
        # Create binary file
        binary_file = temp_dir / "binary.bin"
        binary_content = bytes(range(256)) * 1000  # 256KB of binary data
        binary_file.write_bytes(binary_content)

        archive_path = temp_dir / "binary.tzst"
        result = main(["a", str(archive_path), str(binary_file)])
        assert result == 0


class TestCLIUnicodeHandling:
    """Test CLI with Unicode and international characters."""

    def test_unicode_filenames(self, temp_dir):
        """Test files with Unicode characters in names."""
        # Create file with Unicode characters (may fail on some platforms)
        try:
            unicode_file = temp_dir / "测试文件_🌟.txt"
            unicode_file.write_text("Unicode content", encoding="utf-8")

            archive_path = temp_dir / "unicode.tzst"
            result = main(["a", str(archive_path), str(unicode_file)])
            # Result may be 0 (success) or 1 (failure) depending on platform
            assert result in [0, 1]
        except (OSError, UnicodeError):
            # Skip if platform doesn't support Unicode filenames
            pytest.skip("Platform doesn't support Unicode filenames")

    def test_unicode_content(self, temp_dir):
        """Test files with Unicode content."""
        # Create file with Unicode content
        unicode_content_file = temp_dir / "unicode_content.txt"
        unicode_content = "Hello 世界! 🌍 Здравствуй мир!"
        unicode_content_file.write_text(unicode_content, encoding="utf-8")

        archive_path = temp_dir / "unicode_content.tzst"
        result = main(["a", str(archive_path), str(unicode_content_file)])
        assert result == 0

        # Test extraction and content verification
        extract_dir = temp_dir / "unicode_extracted"
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0

        extracted_file = extract_dir / "unicode_content.txt"
        assert extracted_file.exists()
        extracted_content = extracted_file.read_text(encoding="utf-8")
        assert extracted_content == unicode_content


class TestCLIExitCodes:
    """Test CLI exit codes for proper script integration."""

    def test_successful_operations_return_zero(self, sample_files, temp_dir):
        """Test that successful operations return exit code 0."""
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "success.tzst"

        # Create archive
        result = main(["a", str(archive_path), *file_paths])
        assert result == 0

        # List archive
        result = main(["l", str(archive_path)])
        assert result == 0

        # Test archive
        result = main(["t", str(archive_path)])
        assert result == 0

        # Extract archive
        extract_dir = temp_dir / "extracted"
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0

    def test_error_conditions_return_nonzero(self, temp_dir):
        """Test that error conditions return non-zero exit codes."""
        # Non-existent archive
        result = main(["l", str(temp_dir / "nonexistent.tzst")])
        assert result != 0

        # Non-existent file to archive
        result = main(["a", str(temp_dir / "test.tzst"), "nonexistent.txt"])
        assert result != 0

        # Invalid compression level
        result = main(["a", str(temp_dir / "test.tzst"), __file__, "-l", "0"])
        assert result != 0

        # Invalid filter
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), __file__])  # Create valid archive first
        result = main(["x", str(archive_path), "--filter", "invalid"])
        assert result != 0

    def test_help_and_version_return_proper_codes(self):
        """Test help and version commands return appropriate codes."""
        # Help should return non-zero (standard for help)
        result = main([])
        assert result == 1

        # Version should return zero
        result = main(["--version"])
        assert result == 0


class TestCLIPerformance:
    """Test CLI performance with various scenarios."""

    def test_large_number_of_small_files(self, temp_dir):
        """Test archiving many small files."""
        # Create multiple small files
        files = []
        for i in range(50):
            small_file = temp_dir / f"small_{i:03d}.txt"
            small_file.write_text(f"Small file {i} content")
            files.append(str(small_file))

        archive_path = temp_dir / "many_files.tzst"
        result = main(["a", str(archive_path), *files])
        assert result == 0
        assert archive_path.exists()

    def test_nested_directory_structure(self, temp_dir):
        """Test archiving nested directory structures."""
        # Create nested structure
        for i in range(5):
            nested_dir = temp_dir / f"level_{i}"
            for j in range(i + 1):
                nested_dir = nested_dir / f"sub_{j}"
            nested_dir.mkdir(parents=True, exist_ok=True)

            nested_file = nested_dir / f"file_{i}.txt"
            nested_file.write_text(f"Nested file at level {i}")

        archive_path = temp_dir / "nested.tzst"
        result = main(["a", str(archive_path), str(temp_dir / "level_0")])
        assert result == 0


class TestCLIRealWorldScenarios:
    """Test scenarios discovered during comprehensive real-world testing."""

    def test_no_atomic_flag_with_path_resolution(self, temp_dir):
        """Test --no-atomic flag with various path scenarios.

        This tests the critical bug fix where --no-atomic failed due to
        path resolution issues when changing working directory.
        """
        # Create test file
        test_file = temp_dir / "test_no_atomic.txt"
        test_file.write_text("No atomic test content")

        # Test no-atomic in current directory
        archive_path = temp_dir / "no_atomic_test.tzst"
        result = main(["a", str(archive_path), str(test_file), "--no-atomic"])
        assert result == 0
        assert archive_path.exists()

        # Verify archive integrity
        result = main(["t", str(archive_path)])
        assert result == 0  # Test extraction works
        extract_dir = temp_dir / "no_atomic_extracted"
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0
        extracted_file = extract_dir / "test_no_atomic.txt"
        assert extracted_file.exists()

    def test_no_atomic_flag_in_subdirectory(self, temp_dir):
        """Test --no-atomic flag when archive is in subdirectory."""
        # Create subdirectory and test file
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        test_file = temp_dir / "test_sub.txt"
        test_file.write_text("Subdirectory test content")

        # Create archive in subdirectory with --no-atomic
        archive_path = subdir / "sub_no_atomic.tzst"
        result = main(["a", str(archive_path), str(test_file), "--no-atomic"])
        assert result == 0
        assert archive_path.exists()

    def test_compression_level_clamping(self, temp_dir):
        """Test that extreme compression levels are handled properly."""
        test_file = temp_dir / "clamp_test.txt"
        test_file.write_text("Compression clamping test")

        # Test compression level higher than maximum
        archive_path = temp_dir / "extreme_compression.tzst"
        result = main(["a", str(archive_path), str(test_file), "-l", "50"])
        assert result == 2  # argparse error

        # Test negative compression level
        result = main(["a", str(archive_path), str(test_file), "-l", "-1"])
        assert result == 2  # argparse error

    def test_whitespace_only_file(self, temp_dir):
        """Test archiving files with only whitespace content."""
        whitespace_file = temp_dir / "whitespace.txt"
        whitespace_file.write_text("   \n\t\n   \n")

        archive_path = temp_dir / "whitespace.tzst"
        result = main(["a", str(archive_path), str(whitespace_file)])
        assert result == 0

        # Extract and verify content preserved
        extract_dir = temp_dir / "whitespace_extracted"
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0

        extracted_file = extract_dir / "whitespace.txt"
        assert extracted_file.exists()
        assert extracted_file.read_text() == "   \n\t\n   \n"

    def test_null_bytes_binary_file(self, temp_dir):
        """Test archiving binary files with null bytes."""
        null_file = temp_dir / "null_bytes.bin"
        null_content = b"\x00\x00\x00\x01\x00\x02\x00\x00\x03"
        null_file.write_bytes(null_content)

        archive_path = temp_dir / "null_bytes.tzst"
        result = main(["a", str(archive_path), str(null_file)])
        assert result == 0

        # Extract and verify binary content preserved
        extract_dir = temp_dir / "null_extracted"
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0

        extracted_file = extract_dir / "null_bytes.bin"
        assert extracted_file.exists()
        assert extracted_file.read_bytes() == null_content

    def test_streaming_with_filters_combination(self, temp_dir):
        """Test streaming flag combined with security filters."""
        # Create test archive
        test_file = temp_dir / "stream_filter.txt"
        test_file.write_text("Streaming with filter test")

        archive_path = temp_dir / "stream_filter.tzst"
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 0

        # Test list with streaming
        result = main(["l", str(archive_path), "--streaming"])
        assert result == 0

        # Test extract with streaming and filter
        extract_dir = temp_dir / "stream_filter_extracted"
        result = main(
            [
                "x",
                str(archive_path),
                "-o",
                str(extract_dir),
                "--streaming",
                "--filter",
                "data",
            ]
        )
        assert result == 0

    def test_exit_code_propagation_fix(self, temp_dir):
        """Test that exit codes are properly propagated (fixed issue)."""
        # Test successful operation returns 0
        test_file = temp_dir / "exit_test.txt"
        test_file.write_text("Exit code test")

        archive_path = temp_dir / "exit_test.tzst"
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 0  # Success should return 0

        # Test error operation returns non-zero
        result = main(["l", "nonexistent_archive.tzst"])
        assert result != 0  # Error should return non-zero


class TestCLISecurityFilterParsing:
    """Test CLI security filter argument parsing."""

    def test_extract_filter_argument_parsing(self):
        """Test that --filter argument is parsed correctly for extract commands."""
        parser = create_parser()

        # Test x/extract command with filter
        args = parser.parse_args(["x", "test.tzst", "--filter", "data"])
        assert args.command == "x"
        assert args.filter == "data"

        args = parser.parse_args(["extract", "test.tzst", "--filter", "tar"])
        assert args.command == "extract"
        assert args.filter == "tar"

        # Test e/extract-flat command with filter
        args = parser.parse_args(["e", "test.tzst", "--filter", "data"])
        assert args.command == "e"
        assert args.filter == "data"

    def test_filter_default_value(self):
        """Test that filter defaults to 'data'."""
        parser = create_parser()

        # Test default for x command
        args = parser.parse_args(["x", "test.tzst"])
        assert args.filter == "data"

        # Test default for e command
        args = parser.parse_args(["e", "test.tzst"])
        assert args.filter == "data"

    def test_filter_invalid_choices(self):
        """Test that invalid filter choices are rejected."""
        parser = create_parser()

        # Invalid filter should raise SystemExit (argparse error)
        with pytest.raises(SystemExit):
            parser.parse_args(["x", "test.tzst", "--filter", "invalid"])

    def test_extract_with_filter(self, sample_files, temp_dir):
        """Test extract command with security filters."""
        archive_path = temp_dir / "cli_extract_filter.tzst"
        file_paths = [str(f) for f in sample_files if f.is_file()][:1]

        # Create archive first
        result = main(["a", str(archive_path), *file_paths])
        assert result == 0

        # Test extraction with different filters
        for filter_type in ["data", "tar", "fully_trusted"]:
            output_dir = temp_dir / f"extracted_{filter_type}"
            result = main(
                ["x", str(archive_path), "--filter", filter_type, "-o", str(output_dir)]
            )
            assert result == 0

    def test_filter_with_other_options(self):
        """Test filter option combined with other options."""
        parser = create_parser()

        # Test with streaming and output directory
        args = parser.parse_args(
            [
                "x",
                "test.tzst",
                "file1.txt",
                "file2.txt",
                "--filter",
                "tar",
                "--streaming",
                "-o",
                "output_dir",
            ]
        )
        assert args.filter == "tar"
        assert args.streaming is True
        assert args.output == "output_dir"
        assert args.files == ["file1.txt", "file2.txt"]

    def test_filter_not_available_for_non_extract_commands(self):
        """Test that --filter is only available for extract commands."""
        parser = create_parser()

        # Should work for extract commands
        parser.parse_args(["x", "test.tzst", "--filter", "data"])
        parser.parse_args(["e", "test.tzst", "--filter", "tar"])

        # Should fail for non-extract commands
        with pytest.raises(SystemExit):
            parser.parse_args(["a", "test.tzst", "file.txt", "--filter", "data"])

        with pytest.raises(SystemExit):
            parser.parse_args(["l", "test.tzst", "--filter", "data"])

        with pytest.raises(SystemExit):
            parser.parse_args(["t", "test.tzst", "--filter", "data"])


class TestCLIBoundaryConditions:
    """Test boundary conditions and edge cases."""

    def test_compression_level_boundaries(self, temp_dir):
        """Test exact boundary values for compression levels."""
        test_file = temp_dir / "boundary_test.txt"
        test_file.write_text("Boundary compression test")

        # Test minimum valid level (1)
        archive_min = temp_dir / "min_compression.tzst"
        result = main(["a", str(archive_min), str(test_file), "-l", "1"])
        assert result == 0

        # Test maximum valid level (22)
        archive_max = temp_dir / "max_compression.tzst"
        result = main(["a", str(archive_max), str(test_file), "-l", "22"])
        assert result == 0

        # Test just below minimum (should fail with argparse error)
        result = main(["a", "temp.tzst", str(test_file), "-l", "0"])
        assert result == 2  # argparse error for invalid choice

        # Test just above maximum (should fail or clamp)
        result = main(["a", "temp.tzst", str(test_file), "-l", "23"])
        assert result in [0, 1, 2]  # May clamp or error

    def test_edge_case_scenarios(self, temp_dir):
        """Test edge cases and boundary conditions."""
        # Test with special characters in paths
        special_file = temp_dir / "file with spaces.txt"
        special_file.write_text("content")
        special_archive = temp_dir / "special archive.tzst"

        result = main(["a", str(special_archive), str(special_file)])
        # Should handle special characters gracefully

        if result == 0:
            # If creation succeeded, test other operations
            result = main(["l", str(special_archive)])
            assert result == 0

            result = main(["t", str(special_archive)])
            assert result == 0

    def test_maximum_filename_length(self, temp_dir):
        """Test files with maximum allowable filename length."""
        # Create file with very long name (close to filesystem limit)
        long_name = "a" * 200 + ".txt"
        try:
            long_file = temp_dir / long_name
            long_file.write_text("Long filename test")

            archive_path = temp_dir / "long_filename.tzst"
            result = main(["a", str(archive_path), str(long_file)])
            # Should succeed or fail gracefully
            assert result in [0, 1]
        except OSError:
            # Skip if filesystem doesn't support such long names
            pytest.skip("Filesystem doesn't support long filenames")


class TestCompressionLevelValidation:
    """Test compression level validation in CLI."""

    def test_valid_compression_levels(self, temp_dir):
        """Test that valid compression levels (1-22) work correctly."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Test content")

        # Test boundary values and some middle values
        valid_levels = [1, 2, 10, 22]

        for level in valid_levels:
            archive_path = temp_dir / f"test_level_{level}.tzst"
            result = main(["a", str(archive_path), str(test_file), "-l", str(level)])
            assert result == 0, f"Compression level {level} should be valid"

    def test_invalid_compression_levels(self, temp_dir):
        """Test that invalid compression levels return proper error codes."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Test content")
        archive_path = temp_dir / "test.tzst"

        # Test invalid levels that should return exit code 2 (argparse error)
        invalid_levels = [0, 23, 50, 100, -1, -10]

        for level in invalid_levels:
            result = main(["a", str(archive_path), str(test_file), "-l", str(level)])
            assert result == 2, (
                f"Invalid compression level {level} should return exit code 2"
            )

    def test_non_numeric_compression_levels(self, temp_dir):
        """Test that non-numeric compression levels return proper error codes."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Test content")
        archive_path = temp_dir / "test.tzst"

        # Test non-numeric values
        invalid_values = ["abc", "1.5", "high", "max", ""]

        for value in invalid_values:
            result = main(["a", str(archive_path), str(test_file), "-l", value])
            assert result == 2, (
                f"Non-numeric compression level '{value}' should return exit code 2"
            )

    def test_compression_level_extremes(self, temp_dir):
        """Test compression level validation with extreme values."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Test content")
        archive_path = temp_dir / "test.tzst"

        # Test level 50 - should return argparse error code 2
        result = main(["a", str(archive_path), str(test_file), "-l", "50"])
        assert result == 2, "Compression level 50 should return exit code 2"


class TestCLIVersionCommand:
    """Test version command functionality."""

    def test_version_command_direct(self):
        """Test version command handler directly."""
        from tzst.cli import cmd_version

        class MockArgs:
            pass

        args = MockArgs()
        result = cmd_version(args)
        assert result == 0

    def test_version_command_via_main(self):
        """Test version command via main function."""
        result = main(["--version"])
        assert result == 0

    def test_version_flag_parsing(self):
        """Test that version flag is properly parsed."""
        parser = create_parser()
        args = parser.parse_args(["--version"])
        assert hasattr(args, "version")
        assert args.version is True


class TestCLIValidationFunctions:
    """Test internal CLI validation functions."""

    def test_validate_compression_level_in_argv_valid(self):
        """Test compression level validation with valid levels."""
        from tzst.cli import _validate_compression_level_in_argv

        # Test valid levels
        assert not _validate_compression_level_in_argv(["a", "test.tzst", "-l", "3"])
        assert not _validate_compression_level_in_argv(
            ["a", "test.tzst", "--level", "22"]
        )
        assert not _validate_compression_level_in_argv(
            ["a", "test.tzst", "--level", "1"]
        )

    def test_validate_compression_level_in_argv_invalid_range(self, capsys):
        """Test compression level validation with invalid range."""
        from tzst.cli import _validate_compression_level_in_argv

        # Test invalid range
        assert _validate_compression_level_in_argv(["a", "test.tzst", "-l", "0"])
        captured = capsys.readouterr()
        assert "Invalid compression level: 0" in captured.err
        assert "Must be between 1 and 22" in captured.err

        assert _validate_compression_level_in_argv(["a", "test.tzst", "--level", "23"])
        captured = capsys.readouterr()
        assert "Invalid compression level: 23" in captured.err

    def test_validate_compression_level_in_argv_invalid_format(self, capsys):
        """Test compression level validation with invalid format."""
        from tzst.cli import _validate_compression_level_in_argv

        # Test invalid format
        assert _validate_compression_level_in_argv(["a", "test.tzst", "-l", "abc"])
        captured = capsys.readouterr()
        assert "Invalid compression level: 'abc'" in captured.err
        assert "Must be an integer" in captured.err

    def test_validate_compression_level_in_argv_no_level(self):
        """Test compression level validation when no level specified."""
        from tzst.cli import _validate_compression_level_in_argv

        # Test no level specified
        assert not _validate_compression_level_in_argv(["a", "test.tzst", "file.txt"])

    def test_validate_filter_in_argv_valid(self):
        """Test filter validation with valid filters."""
        from tzst.cli import _validate_filter_in_argv

        # Test valid filters
        assert not _validate_filter_in_argv(["x", "test.tzst", "--filter", "data"])
        assert not _validate_filter_in_argv(["x", "test.tzst", "--filter", "tar"])
        assert not _validate_filter_in_argv(
            ["x", "test.tzst", "--filter", "fully_trusted"]
        )

    def test_validate_filter_in_argv_invalid(self, capsys):
        """Test filter validation with invalid filter."""
        from tzst.cli import _validate_filter_in_argv

        # Test invalid filter
        assert _validate_filter_in_argv(["x", "test.tzst", "--filter", "invalid"])
        captured = capsys.readouterr()
        assert "Invalid filter specified: invalid" in captured.err
        assert "Must be one of: data, tar, fully_trusted" in captured.err

    def test_validate_filter_in_argv_no_filter(self):
        """Test filter validation when no filter specified."""
        from tzst.cli import _validate_filter_in_argv

        # Test no filter specified
        assert not _validate_filter_in_argv(["x", "test.tzst"])


class TestCLIErrorHandlingInternal:
    def test_handle_parsing_errors_help_requested(self):
        """Test error handling when help is requested."""
        from tzst.cli import (
            _handle_parsing_errors,  # Simulate help request (exit code 0)
        )

        e = SystemExit(0)
        result = _handle_parsing_errors(e, ["--help"])
        assert result == 0

    def test_handle_parsing_errors_invalid_filter(self, capsys):
        """Test error handling for invalid filter."""
        from tzst.cli import _handle_parsing_errors

        # Simulate parsing error (exit code 2) with invalid filter
        e = SystemExit(2)
        argv = ["x", "test.tzst", "--filter", "invalid"]
        result = _handle_parsing_errors(e, argv)
        assert result == 2  # Should maintain argparse exit code 2
        # Note: _handle_parsing_errors doesn't print error messages,
        # error messages are printed by argparse before SystemExit is raised

    def test_handle_parsing_errors_other_errors(self):
        """Test error handling for other parsing errors."""
        from tzst.cli import _handle_parsing_errors

        # Test with exit code 2 but no special validation errors
        e = SystemExit(2)
        result = _handle_parsing_errors(e, ["invalid", "command"])
        assert result == 2

        # Test with None exit code
        e = SystemExit(None)
        result = _handle_parsing_errors(e, [])
        assert result == 1

    def test_parse_arguments_success(self):
        """Test successful argument parsing."""
        from tzst.cli import _parse_arguments

        parser = create_parser()
        args, error_code = _parse_arguments(parser, ["a", "test.tzst", "file.txt"])
        assert args is not None
        assert error_code is None
        assert args.command == "a"

    def test_parse_arguments_error(self):
        """Test argument parsing with errors."""
        from tzst.cli import _parse_arguments

        parser = create_parser()
        args, error_code = _parse_arguments(parser, ["invalid"])
        assert args is None
        assert error_code == 2

    def test_execute_command_no_func(self, capsys):
        """Test command execution when no function is set."""
        from tzst.cli import _execute_command

        class MockArgs:
            pass

        args = MockArgs()
        parser = create_parser()
        result = _execute_command(args, parser)
        assert result == 1
        # Should print help when no function is available

    def test_execute_command_version_flag(self):
        """Test command execution with version flag."""
        from tzst.cli import _execute_command

        class MockArgs:
            version = True

        args = MockArgs()
        parser = create_parser()
        result = _execute_command(args, parser)
        assert result == 0

    def test_invalid_arguments_main(self):
        """Test main function with invalid arguments."""
        result = main(["invalid-command"])
        assert result == 2  # Argument parsing error


class TestCLIStreamingAndAdvancedOptions:
    """Test CLI streaming and advanced options."""

    def test_streaming_option_parsing(self):
        """Test that streaming options are properly parsed."""
        parser = create_parser()

        # Test list command with streaming
        args = parser.parse_args(["l", "test.tzst", "--streaming"])
        assert hasattr(args, "streaming")
        assert args.streaming is True

        # Test test command with streaming
        args = parser.parse_args(["t", "test.tzst", "--streaming"])
        assert hasattr(args, "streaming")
        assert args.streaming is True

    def test_atomic_options_parsing(self):
        """Test atomic operation options."""
        parser = create_parser()

        # Test with atomic (default)
        args = parser.parse_args(["a", "test.tzst", "file.txt"])
        assert not hasattr(args, "no_atomic") or not args.no_atomic

        # Test with no-atomic
        args = parser.parse_args(["a", "test.tzst", "file.txt", "--no-atomic"])
        assert hasattr(args, "no_atomic")
        assert args.no_atomic is True

    def test_verbose_options_parsing(self):
        """Test verbose option parsing."""
        parser = create_parser()

        # Test list command with verbose
        args = parser.parse_args(["l", "test.tzst", "-v"])
        assert hasattr(args, "verbose")
        assert args.verbose is True  # Test list command with --verbose
        args = parser.parse_args(["l", "test.tzst", "--verbose"])
        assert hasattr(args, "verbose")
        assert args.verbose is True


class TestCLIEdgeCases:
    """Test CLI edge cases and boundary conditions."""

    def test_empty_arguments(self):
        """Test main function with no arguments."""
        result = main([])
        # Should show help and exit with error code
        assert result in [1, 2]

    def test_help_with_subcommands(self):
        """Test help display for specific subcommands."""
        # Test that help can be requested for specific commands
        result = main(["a", "--help"])
        assert result == 0

        result = main(["x", "--help"])
        assert result == 0

    def test_compression_level_edge_values(self):
        """Test compression level with edge values."""
        parser = create_parser()

        # Test minimum valid level
        args = parser.parse_args(["a", "test.tzst", "file.txt", "-l", "1"])
        assert args.compression_level == 1

        # Test maximum valid level
        args = parser.parse_args(["a", "test.tzst", "file.txt", "--level", "22"])
        assert args.compression_level == 22

    def test_filter_options_all_values(self):
        """Test all valid filter option values."""
        parser = create_parser()

        for filter_val in ["data", "tar", "fully_trusted"]:
            args = parser.parse_args(["x", "test.tzst", "--filter", filter_val])
            assert args.filter == filter_val

    def test_output_directory_parsing(self):
        """Test output directory parsing for extract commands."""
        parser = create_parser()

        # Test extract with output directory
        args = parser.parse_args(["x", "test.tzst", "-o", "/tmp/output"])
        assert args.output == "/tmp/output"

        # Test extract-flat with output directory
        args = parser.parse_args(["e", "test.tzst", "--output", "/tmp/output"])
        assert args.output == "/tmp/output"


class TestCLIFileOperations:
    """Test CLI file operation error scenarios."""

    def test_test_command_missing_file(self, temp_dir):
        """Test test command with missing archive file."""
        missing_archive = temp_dir / "missing.tzst"
        result = main(["t", str(missing_archive)])
        assert result == 1

    def test_list_command_missing_file(self, temp_dir):
        """Test list command with missing archive file."""
        missing_archive = temp_dir / "missing.tzst"
        result = main(["l", str(missing_archive)])
        assert result == 1

    def test_extract_command_missing_file(self, temp_dir):
        """Test extract command with missing archive file."""
        missing_archive = temp_dir / "missing.tzst"
        result = main(["x", str(missing_archive)])
        assert result == 1


class TestCLIExceptionHandling:
    """Test CLI exception handling for comprehensive coverage."""

    def test_oserror_in_validate_files(self, temp_dir, monkeypatch):
        """Test OSError exception handling in _validate_files function."""
        from pathlib import Path

        from tzst.cli import _validate_files

        # Create a path that will trigger OSError when checking existence
        invalid_path = Path(temp_dir / "invalid")

        # Mock Path.exists to raise OSError at the class level
        def mock_exists(self):
            if str(self).endswith("invalid"):
                raise OSError("Invalid path")
            return True

        monkeypatch.setattr(Path, "exists", mock_exists)

        with pytest.raises(OSError):
            _validate_files([invalid_path])

    def test_file_not_found_error_in_extract(self, temp_dir):
        """Test FileNotFoundError handling in extract command."""
        missing_archive = temp_dir / "missing.tzst"
        result = main(["x", str(missing_archive)])
        assert result == 1

    def test_file_not_found_error_in_extract_flat(self, temp_dir):
        """Test FileNotFoundError handling in extract-flat command."""
        missing_archive = temp_dir / "missing.tzst"
        result = main(["e", str(missing_archive)])
        assert result == 1

    def test_file_not_found_error_in_list(self, temp_dir):
        """Test FileNotFoundError handling in list command."""
        missing_archive = temp_dir / "missing.tzst"
        result = main(["l", str(missing_archive)])
        assert result == 1

    def test_file_not_found_error_in_test(self, temp_dir):
        """Test FileNotFoundError handling in test command."""
        missing_archive = temp_dir / "missing.tzst"
        result = main(["t", str(missing_archive)])
        assert result == 1

    def test_tzst_archive_error_in_add(self, temp_dir, monkeypatch):
        """Test TzstArchiveError handling in add command."""
        from tzst.exceptions import TzstArchiveError

        # Create a file to add
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Mock create_archive to raise TzstArchiveError
        def mock_create_archive(*args, **kwargs):
            raise TzstArchiveError("Mock archive error")

        monkeypatch.setattr("tzst.cli.create_archive", mock_create_archive)

        archive_path = temp_dir / "test.tzst"
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 1

    def test_tzst_archive_error_in_extract(self, sample_files, temp_dir, monkeypatch):
        """Test TzstArchiveError handling in extract command."""
        from tzst.exceptions import TzstArchiveError

        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock extract_archive to raise TzstArchiveError
        def mock_extract_archive(*args, **kwargs):
            raise TzstArchiveError("Mock extraction error")

        monkeypatch.setattr("tzst.cli.extract_archive", mock_extract_archive)

        result = main(["x", str(archive_path)])
        assert result == 1

    def test_tzst_archive_error_in_list(self, sample_files, temp_dir, monkeypatch):
        """Test TzstArchiveError handling in list command."""
        from tzst.exceptions import TzstArchiveError

        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock list_archive to raise TzstArchiveError
        def mock_list_archive(*args, **kwargs):
            raise TzstArchiveError("Mock list error")

        monkeypatch.setattr("tzst.cli.list_archive", mock_list_archive)

        result = main(["l", str(archive_path)])
        assert result == 1

    def test_tzst_archive_error_in_test(self, sample_files, temp_dir, monkeypatch):
        """Test TzstArchiveError handling in test command."""
        from tzst.exceptions import TzstArchiveError

        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock test_archive to raise TzstArchiveError
        def mock_test_archive(*args, **kwargs):
            raise TzstArchiveError("Mock test error")

        monkeypatch.setattr("tzst.cli.test_archive", mock_test_archive)

        result = main(["t", str(archive_path)])
        assert result == 1

    def test_value_error_in_add(self, temp_dir, monkeypatch):
        """Test ValueError handling in add command."""

        # Create a file to add
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Mock create_archive to raise ValueError
        def mock_create_archive(*args, **kwargs):
            raise ValueError("Invalid compression level")

        monkeypatch.setattr("tzst.cli.create_archive", mock_create_archive)

        archive_path = temp_dir / "test.tzst"
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 1

    def test_oserror_in_add(self, temp_dir, monkeypatch):
        """Test OSError handling in add command."""

        # Create a file to add
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Mock create_archive to raise OSError
        def mock_create_archive(*args, **kwargs):
            raise OSError("Permission denied")

        monkeypatch.setattr("tzst.cli.create_archive", mock_create_archive)

        archive_path = temp_dir / "test.tzst"
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 1

    def test_keyboard_interrupt_in_add(self, temp_dir, monkeypatch):
        """Test KeyboardInterrupt handling in add command."""

        # Create a file to add
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Mock create_archive to raise KeyboardInterrupt
        def mock_create_archive(*args, **kwargs):
            raise KeyboardInterrupt()

        monkeypatch.setattr("tzst.cli.create_archive", mock_create_archive)

        archive_path = temp_dir / "test.tzst"
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 130  # SIGINT exit code

    def test_generic_exception_in_add(self, temp_dir, monkeypatch):
        """Test generic Exception handling in add command."""

        # Create a file to add
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Mock create_archive to raise generic Exception
        def mock_create_archive(*args, **kwargs):
            raise Exception("Unexpected error")

        monkeypatch.setattr("tzst.cli.create_archive", mock_create_archive)

        archive_path = temp_dir / "test.tzst"
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 1

    def test_generic_exception_in_extract(self, sample_files, temp_dir, monkeypatch):
        """Test generic Exception handling in extract command."""

        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock extract_archive to raise generic Exception
        def mock_extract_archive(*args, **kwargs):
            raise Exception("Unexpected extraction error")

        monkeypatch.setattr("tzst.cli.extract_archive", mock_extract_archive)

        result = main(["x", str(archive_path)])
        assert result == 1

    def test_generic_exception_in_list(self, sample_files, temp_dir, monkeypatch):
        """Test generic Exception handling in list command."""

        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock list_archive to raise generic Exception
        def mock_list_archive(*args, **kwargs):
            raise Exception("Unexpected list error")

        monkeypatch.setattr("tzst.cli.list_archive", mock_list_archive)

        result = main(["l", str(archive_path)])
        assert result == 1

    def test_generic_exception_in_test(self, sample_files, temp_dir, monkeypatch):
        """Test generic Exception handling in test command."""

        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock test_archive to raise generic Exception
        def mock_test_archive(*args, **kwargs):
            raise Exception("Unexpected test error")

        monkeypatch.setattr("tzst.cli.test_archive", mock_test_archive)

        result = main(["t", str(archive_path)])
        assert result == 1

    def test_test_archive_failure(self, sample_files, temp_dir, monkeypatch):
        """Test archive test failure detection."""

        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock test_archive to return False (test failed)
        def mock_test_archive(*args, **kwargs):
            return False

        monkeypatch.setattr("tzst.cli.test_archive", mock_test_archive)

        result = main(["t", str(archive_path)])
        assert result == 1


class TestCLIArgumentParsingEdgeCases:
    """Test advanced argument parsing edge cases."""

    def test_validation_functions_edge_cases(self):
        """Test validation functions with edge cases."""
        from tzst.cli import (
            _validate_compression_level_in_argv,
            _validate_filter_in_argv,
        )

        # Test compression level validation with edge cases
        assert (
            _validate_compression_level_in_argv(["x", "test.tzst", "-l", "1"]) is False
        )  # Valid level returns False
        assert (
            _validate_compression_level_in_argv(["x", "test.tzst", "-l", "22"]) is False
        )  # Valid level returns False
        assert (
            _validate_compression_level_in_argv(["x", "test.tzst", "-l", "0"]) is True
        )  # Invalid level returns True
        assert (
            _validate_compression_level_in_argv(["x", "test.tzst", "-l", "23"]) is True
        )  # Invalid level returns True
        assert (
            _validate_compression_level_in_argv(["x", "test.tzst", "-l", "abc"]) is True
        )  # Invalid level returns True
        assert (
            _validate_compression_level_in_argv(["x", "test.tzst"]) is False
        )  # No compression level returns False

        # Test filter validation with edge cases
        assert (
            _validate_filter_in_argv(["x", "test.tzst", "--filter", "data"]) is False
        )  # Valid filter returns False
        assert (
            _validate_filter_in_argv(["x", "test.tzst", "--filter", "tar"]) is False
        )  # Valid filter returns False
        assert (
            _validate_filter_in_argv(["x", "test.tzst", "--filter", "invalid"]) is True
        )  # Invalid filter returns True
        assert (
            _validate_filter_in_argv(["x", "test.tzst"]) is False
        )  # No filter returns False

    def test_handle_parsing_errors_edge_cases(self):
        """Test _handle_parsing_errors with various edge cases."""
        from tzst.cli import _handle_parsing_errors

        # Test with different exit codes
        e = SystemExit(0)
        result = _handle_parsing_errors(e, ["--help"])
        assert result == 0

        e = SystemExit(1)
        result = _handle_parsing_errors(e, ["some", "args"])
        assert result == 1

        e = SystemExit(None)
        result = _handle_parsing_errors(e, [])
        assert result == 1  # Test with compression level error
        e = SystemExit(2)
        result = _handle_parsing_errors(e, ["a", "test.tzst", "file.txt", "-l", "1000"])
        assert result == 2

        # Test with filter error
        e = SystemExit(2)
        result = _handle_parsing_errors(e, ["x", "test.tzst", "--filter", "badfilter"])
        assert result == 2

    def test_parse_arguments_edge_cases(self):
        """Test _parse_arguments with edge cases."""
        from tzst.cli import _parse_arguments, create_parser

        parser = create_parser()

        # Test successful parsing
        args, error_code = _parse_arguments(parser, ["a", "test.tzst", "file.txt"])
        assert args is not None
        assert error_code is None

        # Test parsing error
        args, error_code = _parse_arguments(parser, ["invalid"])
        assert args is None
        assert error_code == 2

    def test_execute_command_edge_cases(self):
        """Test _execute_command with edge cases."""
        from tzst.cli import _execute_command, create_parser

        parser = create_parser()

        # Test with version flag
        class MockArgsVersion:
            version = True

        args = MockArgsVersion()
        result = _execute_command(args, parser)
        assert result == 0

        # Test with no function attribute
        class MockArgsNoFunc:
            version = False

        args = MockArgsNoFunc()
        result = _execute_command(args, parser)
        assert result == 1


class TestCLIVerboseListingCoverage:
    """Test verbose listing functionality for coverage."""

    def test_verbose_listing_with_mixed_content(self, sample_files, temp_dir, capsys):
        """Test verbose listing functionality with files and directories."""
        # Create archive with mixed content
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Test verbose listing
        result = main(["l", str(archive_path), "-v"])
        assert result == 0

        # Check that verbose output is displayed
        captured = capsys.readouterr()
        assert "Mode" in captured.out
        assert "Size" in captured.out
        assert "Modified" in captured.out
        assert "Name" in captured.out
        assert "-" * 60 in captured.out

    def test_verbose_listing_with_mode_information(self, temp_dir, capsys):
        """Test verbose listing with specific mode information."""
        # Create a test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Create archive
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), str(test_file)])

        # Test verbose listing
        result = main(["l", str(archive_path), "-v"])
        assert result == 0

        # Check that mode information is displayed
        captured = capsys.readouterr()
        assert "test.txt" in captured.out
        # Should have mode information displayed

    def test_verbose_listing_directory_entries(self, temp_dir, capsys):
        """Test verbose listing with directory entries."""
        # Create test directory structure
        test_dir = temp_dir / "test_dir"
        test_dir.mkdir()
        test_file = test_dir / "nested.txt"
        test_file.write_text("nested content")

        # Create archive with directory
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), str(test_dir)])

        # Test verbose listing
        result = main(["l", str(archive_path), "-v"])
        assert result == 0

        # Check directory is shown as <DIR>
        captured = capsys.readouterr()
        assert "<DIR>" in captured.out or "test_dir" in captured.out


class TestCLISimpleListingCoverage:
    """Test simple listing functionality for coverage."""

    def test_simple_listing_with_summary(self, sample_files, temp_dir, capsys):
        """Test simple listing with file and directory summary."""  # Create test files and directories
        file_paths = [str(f) for f in sample_files if f.is_file()]

        # Create archive
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Test simple listing
        result = main(["l", str(archive_path)])
        assert result == 0

        # Check that summary is displayed
        captured = capsys.readouterr()
        assert "Total:" in captured.out
        assert "files" in captured.out

    def test_simple_listing_with_directories(self, temp_dir, capsys):
        """Test simple listing counting directories."""
        # Create test structure with directories
        test_dir1 = temp_dir / "dir1"
        test_dir1.mkdir()
        test_file1 = test_dir1 / "file1.txt"
        test_file1.write_text("content1")

        test_dir2 = temp_dir / "dir2"
        test_dir2.mkdir()
        test_file2 = test_dir2 / "file2.txt"
        test_file2.write_text("content2")

        # Create archive
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), str(test_dir1), str(test_dir2)])

        # Test simple listing
        result = main(["l", str(archive_path)])
        assert result == 0

        # Check directory counting in summary
        captured = capsys.readouterr()
        assert "directories" in captured.out
        assert "Total:" in captured.out

    def test_simple_listing_size_calculation(self, temp_dir, capsys):
        """Test simple listing size calculation."""
        # Create test files with known content
        test_file1 = temp_dir / "file1.txt"
        test_file1.write_text("A" * 100)  # 100 bytes
        test_file2 = temp_dir / "file2.txt"
        test_file2.write_text("B" * 200)  # 200 bytes

        # Create archive
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), str(test_file1), str(test_file2)])

        # Test simple listing
        result = main(["l", str(archive_path)])
        assert result == 0

        # Check total size is calculated
        captured = capsys.readouterr()
        assert "Total:" in captured.out
        # Should show total size of files


class TestCLIExtractFlatExceptionHandling:
    """Test extract-flat command exception handling for coverage."""

    def test_extract_flat_file_not_found_error(self, temp_dir):
        """Test extract-flat command with missing archive file."""
        missing_archive = temp_dir / "missing.tzst"
        result = main(["e", str(missing_archive)])
        assert result == 1

    def test_extract_flat_tzst_decompression_error(
        self, sample_files, temp_dir, monkeypatch
    ):
        """Test extract-flat command with TzstDecompressionError."""
        from tzst.exceptions import TzstDecompressionError

        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock extract_archive to raise TzstDecompressionError
        def mock_extract_archive(*args, **kwargs):
            raise TzstDecompressionError("Mock decompression error")

        monkeypatch.setattr("tzst.cli.extract_archive", mock_extract_archive)

        result = main(["e", str(archive_path)])
        assert result == 1

    def test_extract_flat_tzst_archive_error(self, sample_files, temp_dir, monkeypatch):
        """Test extract-flat command with TzstArchiveError."""
        from tzst.exceptions import TzstArchiveError

        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock extract_archive to raise TzstArchiveError
        def mock_extract_archive(*args, **kwargs):
            raise TzstArchiveError("Mock archive error")

        monkeypatch.setattr("tzst.cli.extract_archive", mock_extract_archive)

        result = main(["e", str(archive_path)])
        assert result == 1

    def test_extract_flat_generic_exception(self, sample_files, temp_dir, monkeypatch):
        """Test extract-flat command with generic Exception."""
        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock extract_archive to raise generic Exception
        def mock_extract_archive(*args, **kwargs):
            raise Exception("Mock generic error")

        monkeypatch.setattr("tzst.cli.extract_archive", mock_extract_archive)

        result = main(["e", str(archive_path)])
        assert result == 1

    def test_extract_flat_with_filter_option(self, sample_files, temp_dir, capsys):
        """Test extract-flat command with non-default filter."""
        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Extract with tar filter
        output_dir = temp_dir / "extracted"
        result = main(
            ["e", str(archive_path), "-o", str(output_dir), "--filter", "tar"]
        )
        assert result == 0

        # Check that filter is mentioned in output
        captured = capsys.readouterr()
        assert "Using security filter: tar" in captured.out


class TestCLIKeyboardInterruptHandling:
    """Test KeyboardInterrupt handling in CLI commands for coverage."""

    def test_keyboard_interrupt_in_extract_full(
        self, sample_files, temp_dir, monkeypatch
    ):
        """Test KeyboardInterrupt handling in extract command."""
        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock extract_archive to raise KeyboardInterrupt
        def mock_extract_archive(*args, **kwargs):
            raise KeyboardInterrupt()

        monkeypatch.setattr("tzst.cli.extract_archive", mock_extract_archive)

        result = main(["x", str(archive_path)])
        assert result == 130  # SIGINT exit code

    def test_keyboard_interrupt_in_list(self, sample_files, temp_dir, monkeypatch):
        """Test KeyboardInterrupt handling in list command."""
        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock list_archive to raise KeyboardInterrupt
        def mock_list_archive(*args, **kwargs):
            raise KeyboardInterrupt()

        monkeypatch.setattr("tzst.cli.list_archive", mock_list_archive)

        result = main(["l", str(archive_path)])
        assert result == 130

    def test_keyboard_interrupt_in_test(self, sample_files, temp_dir, monkeypatch):
        """Test KeyboardInterrupt handling in test command."""
        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock test_archive to raise KeyboardInterrupt
        def mock_test_archive(*args, **kwargs):
            raise KeyboardInterrupt()

        monkeypatch.setattr("tzst.cli.test_archive", mock_test_archive)

        result = main(["t", str(archive_path)])
        assert result == 130


class TestCLITzstDecompressionErrorHandling:
    """Test TzstDecompressionError handling in CLI commands for coverage."""

    def test_tzst_decompression_error_in_extract_full(
        self, sample_files, temp_dir, monkeypatch
    ):
        """Test TzstDecompressionError handling in extract command."""
        from tzst.exceptions import TzstDecompressionError

        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock extract_archive to raise TzstDecompressionError
        def mock_extract_archive(*args, **kwargs):
            raise TzstDecompressionError("Mock decompression error")

        monkeypatch.setattr("tzst.cli.extract_archive", mock_extract_archive)

        result = main(["x", str(archive_path)])
        assert result == 1

    def test_tzst_decompression_error_in_list(
        self, sample_files, temp_dir, monkeypatch
    ):
        """Test TzstDecompressionError handling in list command."""
        from tzst.exceptions import TzstDecompressionError

        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock list_archive to raise TzstDecompressionError
        def mock_list_archive(*args, **kwargs):
            raise TzstDecompressionError("Mock decompression error")

        monkeypatch.setattr("tzst.cli.list_archive", mock_list_archive)

        result = main(["l", str(archive_path)])
        assert result == 1

    def test_tzst_decompression_error_in_test(
        self, sample_files, temp_dir, monkeypatch
    ):
        """Test TzstDecompressionError handling in test command."""
        from tzst.exceptions import TzstDecompressionError

        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock test_archive to raise TzstDecompressionError
        def mock_test_archive(*args, **kwargs):
            raise TzstDecompressionError("Mock decompression error")

        monkeypatch.setattr("tzst.cli.test_archive", mock_test_archive)

        result = main(["t", str(archive_path)])
        assert result == 1


class TestCLIAdvancedExceptionScenarios:
    """Test additional exception scenarios for comprehensive coverage."""

    def test_generic_exception_in_test_command(
        self, sample_files, temp_dir, monkeypatch
    ):
        """Test generic Exception handling in test command."""
        # Create a valid archive first
        file_paths = [str(f) for f in sample_files if f.is_file()]
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), *file_paths])

        # Mock test_archive to raise generic Exception
        def mock_test_archive(*args, **kwargs):
            raise Exception("Unexpected test error")

        monkeypatch.setattr("tzst.cli.test_archive", mock_test_archive)

        result = main(["t", str(archive_path)])
        assert result == 1

    def test_list_command_archive_not_found_path_check(self, temp_dir):
        """Test list command path existence check."""
        missing_archive = temp_dir / "definitely_missing.tzst"
        # Ensure the file definitely doesn't exist
        assert not missing_archive.exists()

        result = main(["l", str(missing_archive)])
        assert result == 1

    def test_test_command_archive_not_found_path_check(self, temp_dir):
        """Test test command path existence check."""
        missing_archive = temp_dir / "definitely_missing.tzst"
        # Ensure the file definitely doesn't exist
        assert not missing_archive.exists()

        result = main(["t", str(missing_archive)])
        assert result == 1

    def test_extract_full_archive_not_found_path_check(self, temp_dir):
        """Test extract command path existence check."""
        missing_archive = temp_dir / "definitely_missing.tzst"
        # Ensure the file definitely doesn't exist
        assert not missing_archive.exists()

        result = main(["x", str(missing_archive)])
        assert result == 1

    def test_extract_flat_archive_not_found_path_check(self, temp_dir):
        """Test extract-flat command path existence check."""
        missing_archive = temp_dir / "definitely_missing.tzst"
        # Ensure the file definitely doesn't exist
        assert not missing_archive.exists()

        result = main(["e", str(missing_archive)])
        assert result == 1


class TestCLIListingFunctionsCoverage:
    """Test edge cases in listing functions for coverage."""

    def test_verbose_listing_with_missing_mode(self, temp_dir, capsys, monkeypatch):
        """Test verbose listing when mode information is missing."""
        # Create a test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Create archive
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), str(test_file)])

        # Mock list_archive to return items without mode
        def mock_list_archive(*args, **kwargs):
            return [
                {
                    "name": "test.txt",
                    "size": 12,
                    "is_file": True,
                    "is_dir": False,
                    # Missing mode field
                }
            ]

        monkeypatch.setattr("tzst.cli.list_archive", mock_list_archive)

        # Test verbose listing
        result = main(["l", str(archive_path), "-v"])
        assert result == 0

        # Check that missing mode is handled (shows "----")
        captured = capsys.readouterr()
        assert "----" in captured.out

    def test_verbose_listing_with_missing_mtime(self, temp_dir, capsys, monkeypatch):
        """Test verbose listing when mtime information is missing."""
        # Create a test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Create archive
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), str(test_file)])

        # Mock list_archive to return items without mtime_str
        def mock_list_archive(*args, **kwargs):
            return [
                {
                    "name": "test.txt",
                    "size": 12,
                    "is_file": True,
                    "is_dir": False,
                    "mode": 0o644,
                    # Missing mtime_str field
                }
            ]

        monkeypatch.setattr("tzst.cli.list_archive", mock_list_archive)

        # Test verbose listing
        result = main(["l", str(archive_path), "-v"])
        assert result == 0

        # Check that listing works without mtime
        captured = capsys.readouterr()
        assert "test.txt" in captured.out

    def test_simple_listing_mixed_file_types(self, temp_dir, capsys, monkeypatch):
        """Test simple listing with mixed file types for directory counting."""
        # Create a test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Create archive
        archive_path = temp_dir / "test.tzst"
        main(["a", str(archive_path), str(test_file)])

        # Mock list_archive to return mixed content
        def mock_list_archive(*args, **kwargs):
            return [
                {
                    "name": "file1.txt",
                    "size": 100,
                    "is_file": True,
                    "is_dir": False,
                },
                {
                    "name": "dir1/",
                    "size": 0,
                    "is_file": False,
                    "is_dir": True,
                },
                {
                    "name": "file2.txt",
                    "size": 200,
                    "is_file": True,
                    "is_dir": False,
                },
                {
                    "name": "dir2/",
                    "size": 0,
                    "is_file": False,
                    "is_dir": True,
                },
            ]

        monkeypatch.setattr("tzst.cli.list_archive", mock_list_archive)

        # Test simple listing
        result = main(["l", str(archive_path)])
        assert result == 0

        # Check that counts are correct
        captured = capsys.readouterr()
        assert "2 files" in captured.out
        assert "2 directories" in captured.out
        assert "300.0 B" in captured.out  # Total size of files
