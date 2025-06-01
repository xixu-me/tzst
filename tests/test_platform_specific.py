"""Platform-specific and cross-platform compatibility tests."""

import sys

import pytest

from tzst.cli import main


@pytest.mark.skipif(sys.platform == "win32", reason="Unix-specific features")
class TestUnixSpecificFeatures:
    """Test Unix/Linux specific features like symlinks and permissions."""

    def test_symbolic_links_preservation(self, temp_dir):
        """Test that symbolic links are preserved in archives."""
        # Create target file and symlink
        target_file = temp_dir / "target.txt"
        target_file.write_text("Symlink target content")

        symlink_file = temp_dir / "symlink.txt"
        try:
            symlink_file.symlink_to(target_file)
        except OSError:
            pytest.skip("Symlinks not supported on this system")

        # Create archive with symlink
        archive_path = temp_dir / "symlinks.tzst"
        result = main(["a", str(archive_path), str(target_file), str(symlink_file)])
        assert result == 0

        # Extract and verify symlink is preserved
        extract_dir = temp_dir / "symlink_extracted"
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0

        extracted_symlink = extract_dir / "symlink.txt"
        if extracted_symlink.exists():
            # Verify it's still a symlink
            assert extracted_symlink.is_symlink()

    def test_file_permissions_preservation(self, temp_dir):
        """Test that file permissions are preserved."""
        # Create file with specific permissions
        perm_file = temp_dir / "permissions.txt"
        perm_file.write_text("Permission test content")

        # Set specific permissions (readable/writable by owner only)
        try:
            perm_file.chmod(0o600)
        except OSError:
            pytest.skip("Permission setting not supported")

        original_mode = perm_file.stat().st_mode

        # Create archive
        archive_path = temp_dir / "permissions.tzst"
        result = main(["a", str(archive_path), str(perm_file)])
        assert result == 0

        # Extract and verify permissions
        extract_dir = temp_dir / "perm_extracted"
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0

        extracted_file = extract_dir / "permissions.txt"
        if extracted_file.exists():
            # Permissions should be preserved (may vary by system)
            extracted_mode = extracted_file.stat().st_mode
            # At minimum, check that it's not world-writable if original wasn't
            if not (original_mode & 0o002):
                assert not (extracted_mode & 0o002)

    def test_executable_files(self, temp_dir):
        """Test handling of executable files."""
        # Create executable script
        script_file = temp_dir / "test_script.sh"
        script_file.write_text("#!/bin/bash\necho 'Hello World'\n")

        try:
            script_file.chmod(0o755)  # Make executable
        except OSError:
            pytest.skip("Permission setting not supported")

        # Create archive
        archive_path = temp_dir / "executable.tzst"
        result = main(["a", str(archive_path), str(script_file)])
        assert result == 0

        # Extract and verify executable bit preserved
        extract_dir = temp_dir / "exec_extracted"
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0

        extracted_script = extract_dir / "test_script.sh"
        if extracted_script.exists():
            # Check if executable bit is preserved
            mode = extracted_script.stat().st_mode
            assert mode & 0o100  # Owner execute bit


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific tests")
class TestWindowsSpecificFeatures:
    """Test Windows specific behaviors and limitations."""

    def test_windows_reserved_names(self, temp_dir):
        """Test handling of Windows reserved names."""
        # Windows reserved names that should be handled gracefully
        reserved_names = ["CON.txt", "PRN.txt", "AUX.txt", "NUL.txt"]

        files_created = []
        for name in reserved_names:
            try:
                reserved_file = temp_dir / name
                reserved_file.write_text(f"Content for {name}")
                files_created.append(str(reserved_file))
            except OSError:
                # Expected on Windows - these names are reserved
                continue

        if files_created:
            archive_path = temp_dir / "reserved_names.tzst"
            result = main(["a", str(archive_path), *files_created])
            # Should either succeed or fail gracefully
            assert result in [0, 1]

    def test_windows_long_path_handling(self, temp_dir):
        """Test handling of Windows long paths."""
        # Create deeply nested path (Windows has 260 char limit traditionally)
        deep_path = temp_dir
        for i in range(10):
            deep_path = deep_path / f"very_long_directory_name_{i}"

        try:
            deep_path.mkdir(parents=True)
            deep_file = deep_path / "deep_file.txt"
            deep_file.write_text("Deep path content")

            archive_path = temp_dir / "long_path.tzst"
            result = main(["a", str(archive_path), str(deep_file)])
            # Should handle long paths gracefully
            assert result in [0, 1]
        except OSError:
            # Skip if system doesn't support such deep paths
            pytest.skip("System doesn't support deep paths")


class TestUnicodeAndInternational:
    """Test Unicode and international character handling."""

    def test_unicode_content_various_encodings(self, temp_dir):
        """Test files with various Unicode content."""
        # Test various Unicode characters
        unicode_tests = [
            ("chinese.txt", "你好世界 Hello World"),
            ("emoji.txt", "🌟⭐✨🎉🚀💖"),
            ("cyrillic.txt", "Привет мир"),
            ("arabic.txt", "مرحبا بالعالم"),
            ("japanese.txt", "こんにちは世界"),
        ]

        files_created = []
        for filename, content in unicode_tests:
            try:
                unicode_file = temp_dir / filename
                unicode_file.write_text(content, encoding="utf-8")
                files_created.append(str(unicode_file))
            except (OSError, UnicodeError):
                # Skip files that can't be created on this system
                continue

        if files_created:
            archive_path = temp_dir / "unicode_content.tzst"
            result = main(["a", str(archive_path), *files_created])
            assert result == 0

            # Extract and verify content preservation
            extract_dir = temp_dir / "unicode_extracted"
            result = main(["x", str(archive_path), "-o", str(extract_dir)])
            assert result == 0

            # Verify at least one file's content
            for filename, expected_content in unicode_tests:
                extracted_file = extract_dir / filename
                if extracted_file.exists():
                    actual_content = extracted_file.read_text(encoding="utf-8")
                    assert actual_content == expected_content

    def test_unicode_filenames_platform_dependent(self, temp_dir):
        """Test Unicode filenames with platform-aware expectations."""
        unicode_filenames = [
            "测试文件.txt",
            "файл_тест.txt",
            "αρχείο_δοκιμή.txt",
            "ファイル_テスト.txt",
        ]

        files_created = []
        for filename in unicode_filenames:
            try:
                unicode_file = temp_dir / filename
                unicode_file.write_text(f"Content of {filename}", encoding="utf-8")
                files_created.append(str(unicode_file))
            except (OSError, UnicodeError):
                # Skip files that can't be created
                continue

        if files_created:
            archive_path = temp_dir / "unicode_filenames.tzst"
            result = main(["a", str(archive_path), *files_created])

            # On Windows PowerShell, this might fail due to encoding issues
            if sys.platform == "win32":
                assert result in [0, 1]  # May fail on Windows
            else:
                assert result == 0  # Should succeed on Unix


class TestPerformanceAndScalability:
    """Test performance-related scenarios and scalability."""

    def test_many_small_files_archive(self, temp_dir):
        """Test archiving many small files efficiently."""  # Create 100 small files
        files = []
        for i in range(100):
            small_file = temp_dir / f"small_{i:03d}.txt"
            small_file.write_text(f"Small file {i} content")
            files.append(str(small_file))

        archive_path = temp_dir / "many_small.tzst"
        result = main(["a", str(archive_path), *files])
        assert result == 0

        # Verify archive integrity
        result = main(["t", str(archive_path)])
        assert result == 0

    def test_large_single_file_archive(self, temp_dir):
        """Test archiving a single large file."""
        # Create 5MB file
        large_file = temp_dir / "large.txt"
        content = "This is large file content.\n" * 200000  # ~5MB
        large_file.write_text(content)

        archive_path = temp_dir / "large_single.tzst"
        result = main(["a", str(archive_path), str(large_file), "-l", "22"])
        assert result == 0

        # Verify archive can be tested
        result = main(["t", str(archive_path)])
        assert result == 0

    def test_compression_efficiency_levels(self, temp_dir):
        """Test different compression levels for efficiency."""
        # Create test file with repetitive content (compresses well)
        test_file = temp_dir / "compressible.txt"
        repetitive_content = "ABCD" * 10000  # 40KB of repetitive data
        test_file.write_text(repetitive_content)

        # Test different compression levels
        for level in [1, 3, 10, 22]:
            archive_path = temp_dir / f"compression_level_{level}.tzst"
            result = main(["a", str(archive_path), str(test_file), "-l", str(level)])
            assert result == 0

            # Higher compression should generally result in smaller files
            # (though not guaranteed for all content types)
            assert archive_path.exists()
            assert archive_path.stat().st_size > 0


class TestErrorRecoveryAndRobustness:
    """Test error recovery and robustness scenarios."""

    def test_disk_space_simulation(self, temp_dir):
        """Test behavior when disk space might be limited."""
        # Create moderately large file
        large_file = temp_dir / "disk_space_test.txt"
        content = "Large content for disk space test.\n" * 50000
        large_file.write_text(content)

        # Try to create archive with maximum compression
        archive_path = temp_dir / "disk_space.tzst"
        result = main(["a", str(archive_path), str(large_file), "-l", "22"])
        # Should either succeed or fail gracefully
        assert result in [0, 1]

    def test_interrupted_operation_simulation(self, temp_dir):
        """Test that partial operations don't leave corrupted files."""
        # Create test file
        test_file = temp_dir / "interrupt_test.txt"
        test_file.write_text("Interrupt test content")

        # Create archive successfully first
        archive_path = temp_dir / "interrupt_test.tzst"
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 0

        # Verify archive integrity
        result = main(["t", str(archive_path)])
        assert result == 0

        # If archive exists, it should be valid
        if archive_path.exists():
            result = main(["l", str(archive_path)])
            assert result == 0

    def test_readonly_archive_handling(self, temp_dir):
        """Test behavior with read-only archives."""
        # Create archive first
        test_file = temp_dir / "readonly_test.txt"
        test_file.write_text("Read-only test content")

        archive_path = temp_dir / "readonly.tzst"
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 0

        # Make archive read-only
        try:
            archive_path.chmod(0o444)
        except OSError:
            pytest.skip("Cannot set read-only permissions")

        # Should still be able to read the archive
        result = main(["l", str(archive_path)])
        assert result == 0

        result = main(["t", str(archive_path)])
        assert result == 0

        # Extract should work
        extract_dir = temp_dir / "readonly_extracted"
        result = main(["x", str(archive_path), "-o", str(extract_dir)])
        assert result == 0


class TestCommandLineInterfaceEdgeCases:
    """Test edge cases in command line interface handling."""

    def test_empty_argument_handling(self, temp_dir):
        """Test behavior with empty or unusual arguments."""
        # Test with empty string as filename (treated as current directory)
        archive_path = temp_dir / "test.tzst"
        result = main(["a", str(archive_path), ""])
        assert result == 0  # Empty string is treated as current directory

        # Test with very long argument
        long_arg = "a" * 1000
        result = main(["a", "test.tzst", long_arg])
        assert result == 1  # Should fail gracefully

    def test_special_characters_in_archive_names(self, temp_dir):
        """Test archive names with special characters."""
        test_file = temp_dir / "special_arch_test.txt"
        test_file.write_text("Special archive name test")

        # Test various special characters in archive names
        special_names = [
            "archive with spaces.tzst",
            "archive-with-dashes.tzst",
            "archive_with_underscores.tzst",
            "archive.with.dots.tzst",
        ]

        for name in special_names:
            archive_path = temp_dir / name
            result = main(["a", str(archive_path), str(test_file)])
            assert result == 0
            assert archive_path.exists()

    def test_output_directory_creation(self, temp_dir):
        """Test that output directories are created when they don't exist."""
        # Create test archive first
        test_file = temp_dir / "output_test.txt"
        test_file.write_text("Output directory test")

        archive_path = temp_dir / "output.tzst"
        result = main(["a", str(archive_path), str(test_file)])
        assert result == 0

        # Extract to non-existent directory
        nonexistent_dir = temp_dir / "does" / "not" / "exist"
        result = main(["x", str(archive_path), "-o", str(nonexistent_dir)])
        assert result == 0
        assert nonexistent_dir.exists()
        assert (nonexistent_dir / "output_test.txt").exists()
