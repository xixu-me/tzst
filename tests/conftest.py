"""Test configuration and fixtures."""

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
