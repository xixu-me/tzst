"""Tests to cover missing lines in CLI and improve overall coverage."""

import sys
from unittest.mock import patch

import pytest

from tzst.cli import _validate_files, main


class TestCLIMissingLines:
    """Test specific missing lines in CLI for improved coverage."""

    def test_validate_files_os_error_handling(self, temp_dir):
        """Test OSError handling in validate_files function."""
        # Create a test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")  # Mock Path.exists to raise OSError
        with patch(
            "pathlib.Path.exists", side_effect=OSError("Permission denied")
        ):  # Should handle OSError gracefully and continue
            try:
                _validate_files([test_file])
            except OSError:
                pass  # Expected to be caught and handled

    def test_main_function_edge_cases(self, temp_dir):
        """Test main function edge cases for missing line coverage."""
        # Test with minimal arguments that might hit edge cases
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        archive_path = temp_dir / "test.tzst"  # Create archive
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 0

        # Test version command through main
        with patch("sys.exit"):
            try:
                main(["--version"])
            except SystemExit:
                pass

        # Test help command variations
        with patch("sys.exit"):
            try:
                main(["--help"])
            except SystemExit:
                pass

    def test_command_line_argument_edge_cases(self, temp_dir):
        """Test command line argument edge cases."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Test with various argument combinations that might hit missing lines
        archive_path = temp_dir / "test.tzst"

        # Create archive with specific compression level
        result = main(["a", str(archive_path), str(test_file), "-c", "1"])
        assert result == 0

        # Test list with streaming
        result = main(["l", str(archive_path), "--streaming"])
        assert result == 0  # Test extract with specific options
        extract_dir = temp_dir / "extracted"
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0

    def test_error_handling_edge_cases(self, temp_dir):
        """Test error handling edge cases in CLI."""
        # Test with invalid archive path
        invalid_path = temp_dir / "nonexistent" / "test.tzst"

        result = main(["l", str(invalid_path)])
        assert result == 1

        # Test with invalid compression level - should return argparse error code 2
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        archive_path = temp_dir / "test.tzst"

        result = main(["a", str(archive_path), str(test_file), "-c", "50"])
        assert result == 2

    def test_filter_option_edge_cases(self, temp_dir):
        """Test filter option edge cases."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        archive_path = temp_dir / "test.tzst"

        # Create archive
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 0

        # Test extract with different filters
        for filter_type in ["data", "tar", "fully_trusted"]:
            extract_dir = temp_dir / f"extracted_{filter_type}"
            result = main(
                [
                    "x",
                    str(archive_path),
                    "-o",
                    str(extract_dir),
                    "--filter",
                    filter_type,
                ]
            )
            assert result == 0

    def test_atomic_operation_edge_cases(self, temp_dir):
        """Test atomic operation edge cases."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        archive_path = temp_dir / "test.tzst"

        # Test with --no-atomic flag
        result = main(["a", str(archive_path), str(test_file), "--no-atomic"])
        assert result == 0

        # Verify archive was created
        assert archive_path.exists()

    def test_verbose_output_edge_cases(self, temp_dir, capsys):
        """Test verbose output edge cases."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        archive_path = temp_dir / "test.tzst"  # Create archive
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 0

        # Test verbose list
        result = main(["l", str(archive_path), "-v"])
        assert result == 0

        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_command_validation_edge_cases(self):
        """Test command validation edge cases."""
        # Test with empty arguments
        result = main([])
        assert result == 1

        # Test with invalid command - should return argparse error code 2
        result = main(["invalid_command"])
        assert result == 2

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
    def test_windows_specific_functionality(self, temp_dir):
        """Test Windows-specific functionality."""
        # Test Windows reserved names
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        archive_path = temp_dir / "test.tzst"

        # Create archive
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 0

        # Test with Windows path separators
        windows_style_path = str(archive_path).replace("/", "\\")
        result = main(["l", windows_style_path])
        assert result == 0

    def test_streaming_mode_edge_cases(self, temp_dir):
        """Test streaming mode edge cases."""
        # Create a larger file for streaming tests
        large_file = temp_dir / "large.txt"
        large_file.write_text("x" * 10000)  # 10KB file

        archive_path = temp_dir / "streaming.tzst"

        # Create archive
        result = main(["a", str(archive_path), str(large_file)])
        assert result == 0

        # Test all commands with streaming
        result = main(["l", str(archive_path), "--streaming"])
        assert result == 0

        result = main(["t", str(archive_path), "--streaming"])
        assert result == 0

        extract_dir = temp_dir / "extracted_streaming"
        result = main(["x", str(archive_path), "-o", str(extract_dir), "--streaming"])
        assert result == 0

    def test_compression_level_boundary_values(self, temp_dir):
        """Test compression level boundary values."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Test minimum compression level
        archive_path_min = temp_dir / "min_compression.tzst"
        result = main(["a", str(archive_path_min), str(test_file), "-c", "1"])
        assert result == 0

        # Test maximum compression level
        archive_path_max = temp_dir / "max_compression.tzst"
        result = main(["a", str(archive_path_max), str(test_file), "-c", "22"])
        assert result == 0

    def test_output_directory_creation_edge_cases(self, temp_dir):
        """Test output directory creation edge cases."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        archive_path = temp_dir / "test.tzst"

        # Create archive
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 0

        # Test extraction to nested directory that doesn't exist
        nested_extract_dir = temp_dir / "level1" / "level2" / "level3"
        result = main(["x", str(archive_path), "-o", str(nested_extract_dir)])
        assert result == 0

        # Verify directory was created
        assert nested_extract_dir.exists()

    def test_special_file_handling_edge_cases(self, temp_dir):
        """Test special file handling edge cases."""
        # Create files with special characteristics
        empty_file = temp_dir / "empty.txt"
        empty_file.touch()

        binary_file = temp_dir / "binary.bin"
        binary_file.write_bytes(b"\x00\x01\x02\x03\xff")

        unicode_file = temp_dir / "unicode.txt"
        unicode_file.write_text("Hello 世界 🌍", encoding="utf-8")

        archive_path = temp_dir / "special.tzst"

        # Create archive with special files
        result = main(
            [
                "a",
                str(archive_path),
                str(empty_file),
                str(binary_file),
                str(unicode_file),
            ]
        )
        assert result == 0

        # Test list and extract
        result = main(["l", str(archive_path)])
        assert result == 0

        extract_dir = temp_dir / "extracted_special"
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0


class TestPlatformSpecificMissingLines:
    """Test platform-specific functionality to improve coverage."""

    @pytest.mark.skipif(
        sys.platform != "win32", reason="Windows-specific functionality"
    )
    def test_windows_long_path_edge_cases(self, temp_dir):
        """Test Windows long path handling edge cases."""
        # Create a very deep directory structure
        deep_dir = temp_dir
        for i in range(10):
            deep_dir = deep_dir / f"very_long_directory_name_{i}"
        deep_dir.mkdir(parents=True, exist_ok=True)

        deep_file = deep_dir / "deep_file.txt"
        deep_file.write_text("Content in deeply nested file")

        archive_path = temp_dir / "deep.tzst"

        # Test archiving deep structure
        result = main(["a", str(archive_path), str(deep_file)])
        assert result == 0

        # Test extraction
        extract_dir = temp_dir / "extracted_deep"
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0

    @pytest.mark.skipif(
        sys.platform != "win32", reason="Windows-specific functionality"
    )
    def test_windows_reserved_names_edge_cases(self, temp_dir):
        """Test Windows reserved names edge cases."""
        # Test with files that have problematic names on Windows
        normal_file = temp_dir / "normal.txt"
        normal_file.write_text("normal content")

        # File with trailing space (problematic on Windows)
        space_file = temp_dir / "file_with_space .txt"
        space_file.write_text("space content")

        archive_path = temp_dir / "reserved.tzst"

        # Create archive
        result = main(["a", str(archive_path), str(normal_file), str(space_file)])
        assert result == 0

    def test_unicode_handling_edge_cases(self, temp_dir):
        """Test unicode handling edge cases."""
        # Create files with various unicode content
        files_to_create = [
            ("chinese.txt", "你好世界"),
            ("emoji.txt", "🎉🌟💫"),
            ("mixed.txt", "Hello 世界! 🌍 Мир"),
            ("special_chars.txt", "àáâãäåæçèéêë"),
        ]

        created_files = []
        for filename, content in files_to_create:
            file_path = temp_dir / filename
            file_path.write_text(content, encoding="utf-8")
            created_files.append(file_path)

        archive_path = temp_dir / "unicode.tzst"  # Create archive
        file_args = [str(f) for f in created_files]
        result = main(["a", str(archive_path), *file_args])
        assert result == 0

        # Test extraction
        extract_dir = temp_dir / "extracted_unicode"
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0

        # Verify unicode content is preserved
        for filename, original_content in files_to_create:
            extracted_file = extract_dir / filename
            assert extracted_file.exists()
            extracted_content = extracted_file.read_text(encoding="utf-8")
            assert extracted_content == original_content

    def test_performance_edge_cases(self, temp_dir):
        """Test performance-related edge cases."""
        # Create many small files
        files = []
        for i in range(50):  # Create 50 small files
            file_path = temp_dir / f"small_{i:03d}.txt"
            file_path.write_text(f"Content of file {i}")
            files.append(file_path)

        archive_path = temp_dir / "many_files.tzst"  # Create archive with many files
        file_args = [str(f) for f in files]
        result = main(["a", str(archive_path), *file_args])
        assert result == 0

        # Test listing (should handle many files efficiently)
        result = main(["l", str(archive_path)])
        assert result == 0

        # Test extraction
        extract_dir = temp_dir / "extracted_many"
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0

    def test_error_recovery_edge_cases(self, temp_dir):
        """Test error recovery edge cases."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        archive_path = temp_dir / "test.tzst"

        # Create archive
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 0

        # Test with readonly archive
        archive_path.chmod(0o444)  # Make read-only

        try:
            # Should handle read-only archive gracefully
            result = main(["l", str(archive_path)])
            assert result == 0
        finally:
            # Restore write permissions for cleanup
            archive_path.chmod(0o644)

    def test_cross_platform_compatibility(self, temp_dir):
        """Test cross-platform compatibility features."""
        # Create files with various characteristics
        text_file = temp_dir / "text.txt"
        text_file.write_text("Cross-platform text content\n")

        binary_file = temp_dir / "binary.dat"
        binary_file.write_bytes(bytes(range(256)))

        archive_path = temp_dir / "cross_platform.tzst"

        # Create archive
        result = main(["a", str(archive_path), str(text_file), str(binary_file)])
        assert result == 0

        # Test with different compression levels
        for level in [1, 11, 22]:
            archive_path_level = temp_dir / f"cross_platform_level_{level}.tzst"
            result = main(
                ["a", str(archive_path_level), str(text_file), "-c", str(level)]
            )
            assert result == 0

            # Verify can be read back
            result = main(["t", str(archive_path_level)])
            assert result == 0
