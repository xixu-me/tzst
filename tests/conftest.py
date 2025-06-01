"""Test configuration and fixtures."""

import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_files(temp_dir):
    """Create sample files for testing."""
    files = []

    # Create a simple text file
    text_file = temp_dir / "test.txt"
    text_file.write_text("Hello, World!\nThis is a test file.\n")
    files.append(text_file)

    # Create a binary file
    binary_file = temp_dir / "test.bin"
    binary_file.write_bytes(b"\x00\x01\x02\x03\x04\x05" * 100)
    files.append(binary_file)

    # Create a subdirectory with files
    subdir = temp_dir / "subdir"
    subdir.mkdir()
    sub_file = subdir / "sub.txt"
    sub_file.write_text("Subdirectory file content\n")
    files.append(sub_file)

    # Create another subdirectory
    subdir2 = temp_dir / "subdir" / "nested"
    subdir2.mkdir()
    nested_file = subdir2 / "nested.txt"
    nested_file.write_text("Nested file content\n")
    files.append(nested_file)

    return files


@pytest.fixture
def sample_archive_path(temp_dir):
    """Get path for a sample archive."""
    return temp_dir / "test.tzst"


@pytest.fixture
def comprehensive_test_files(temp_dir):
    """Create comprehensive test files covering edge cases found during testing."""
    files = []

    # Empty file
    empty_file = temp_dir / "empty_file.txt"
    empty_file.touch()
    files.append(empty_file)

    # File with only whitespace
    whitespace_file = temp_dir / "whitespace_only.txt"
    whitespace_file.write_text("   \n\t\n   \n")
    files.append(whitespace_file)

    # File with only newlines
    newlines_file = temp_dir / "newlines_only.txt"
    newlines_file.write_text("\n\n\n\n\n")
    files.append(newlines_file)

    # Binary file with null bytes
    null_bytes_file = temp_dir / "null_bytes.bin"
    null_bytes_file.write_bytes(b"\x00\x00\x00\x01\x00\x02\x00\x00\x03")
    files.append(null_bytes_file)

    # Large text file
    large_file = temp_dir / "large_file.txt"
    large_content = "This is a large file for testing compression.\n" * 10000
    large_file.write_text(large_content)
    files.append(large_file)

    # Binary data file
    binary_data_file = temp_dir / "binary_data.bin"
    binary_content = bytes(range(256)) * 100  # 25.6KB of binary data
    binary_data_file.write_bytes(binary_content)
    files.append(binary_data_file)

    # File with spaces and special characters in name
    special_chars_file = temp_dir / "file with spaces.txt"
    special_chars_file.write_text("File with special characters in name")
    files.append(special_chars_file)

    # Unicode content file (should work on all platforms)
    unicode_content_file = temp_dir / "unicode_content.txt"
    unicode_content_file.write_text("Hello 世界! 🌍", encoding="utf-8")
    files.append(unicode_content_file)

    # Create nested directory structure
    nested_dir = temp_dir / "nested" / "very" / "deep" / "directory"
    nested_dir.mkdir(parents=True, exist_ok=True)
    nested_file = nested_dir / "deepest_file.txt"
    nested_file.write_text("File in deeply nested structure")
    files.append(nested_file)

    return files


@pytest.fixture
def platform_specific_files(temp_dir):
    """Create platform-specific test files."""
    files = []

    if os.name == "posix":  # Unix/Linux
        # Create executable file
        script_file = temp_dir / "test_script.sh"
        script_file.write_text("#!/bin/bash\necho 'Hello World'\n")
        try:
            script_file.chmod(0o755)
            files.append(script_file)
        except OSError:
            pass

        # Create symlink if possible
        target_file = temp_dir / "symlink_target.txt"
        target_file.write_text("Symlink target content")
        files.append(target_file)

        symlink_file = temp_dir / "test_symlink.txt"
        try:
            symlink_file.symlink_to(target_file)
            files.append(symlink_file)
        except OSError:
            pass

    return files


@pytest.fixture
def compression_test_files(temp_dir):
    """Create files for testing different compression levels."""
    files = []

    # Highly compressible file (repetitive content)
    compressible_file = temp_dir / "highly_compressible.txt"
    compressible_content = "A" * 5000 + "B" * 5000 + "C" * 5000
    compressible_file.write_text(compressible_content)
    files.append(compressible_file)

    # Poorly compressible file (pseudo-random data)
    random_file = temp_dir / "poorly_compressible.bin"
    random_data = bytes((i * 7 + 23) % 256 for i in range(15000))
    random_file.write_bytes(random_data)
    files.append(random_file)

    return files
