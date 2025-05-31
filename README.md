# tzst

[![CodeQL](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql)
[![CI/CD](https://github.com/xixu-me/tzst/actions/workflows/ci.yml/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/ci.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/tzst)](https://pypi.org/project/tzst/)
[![GitHub License](https://img.shields.io/github/license/xixu-me/tzst)](LICENSE)
[![Sponsor](https://img.shields.io/badge/Sponsor-violet)](https://xi-xu.me/#sponsorships)

A Python library for creating and manipulating `.tzst`/`.tar.zst` archives using Zstandard compression.

## Features

- **High Compression**: Uses Zstandard compression for excellent compression ratios and speed
- **Tar Compatibility**: Creates standard tar archives compressed with Zstandard
- **Command Line Interface**: Easy-to-use CLI with intuitive commands and streaming support
- **Python API**: Clean, Pythonic API for programmatic use
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Multiple Extensions**: Supports both `.tzst` and `.tar.zst` extensions
- **Flexible Extraction**: Extract with full paths or flatten directory structure
- **Memory Efficient**: Streaming mode for handling large archives with minimal memory usage
- **Atomic Operations**: Safe file operations with automatic cleanup on interruption
- **Enhanced Error Handling**: Clear error messages with helpful alternatives and suggestions
- **Secure by Default**: Uses the 'data' filter for maximum security during extraction

## Installation

### From PyPI

```bash
pip install tzst
```

### From Source

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

### Development Installation

This project uses [Hatch](https://hatch.pypa.io/) as the build system, configured in `pyproject.toml`. For development:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

Alternatively, if you have [Hatch](https://hatch.pypa.io/) installed:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
hatch env create
hatch shell
```

## Quick Start

### Command Line Usage

> **Recommended**: The `uvx tzst` command is highly recommended for running tzst without installation and with significantly better performance. [uv](https://github.com/astral-sh/uv) provides faster package resolution and execution compared to standard pip/python approaches. See the [uv's documentation](https://docs.astral.sh/uv/) for more details.

```bash
# Create an archive
tzst a archive.tzst file1.txt file2.txt directory/

# Extract an archive
tzst x archive.tzst

# List archive contents
tzst l archive.tzst

# Test archive integrity
tzst t archive.tzst
```

### Python API Usage

```python
from tzst import create_archive, extract_archive, list_archive

# Create an archive
create_archive("archive.tzst", ["file1.txt", "file2.txt", "directory/"])

# Extract an archive
extract_archive("archive.tzst", "output_directory/")

# List archive contents
contents = list_archive("archive.tzst", verbose=True)
for item in contents:
    print(f"{item['name']}: {item['size']} bytes")
```

## Command Line Interface

The `tzst` command provides a comprehensive CLI for archive operations:

### Archive Operations

#### Create Archive

```bash
# Basic usage
tzst a archive.tzst file1.txt file2.txt

# With compression level (1-22, default: 3)
tzst a archive.tzst files/ -l 15

# Disable atomic file operations (not recommended)
tzst a archive.tzst files/ --no-atomic

# Alternative commands
tzst add archive.tzst files/
tzst create archive.tzst files/
```

#### Extract Archive

```bash
# Extract with full directory structure
tzst x archive.tzst

# Extract to specific directory
tzst x archive.tzst -o output/

# Extract specific files
tzst x archive.tzst file1.txt dir/file2.txt

# Extract without directory structure (flat)
tzst e archive.tzst -o output/

# Use streaming mode for large archives (reduces memory usage)
tzst x archive.tzst --streaming -o output/
```

#### List Contents

```bash
# Simple listing
tzst l archive.tzst

# Verbose listing with details
tzst l archive.tzst -v

# Use streaming mode for large archives
tzst l archive.tzst --streaming -v
```

#### Test Integrity

```bash
# Test archive integrity
tzst t archive.tzst

# Test with streaming mode for large archives
tzst t archive.tzst --streaming
```

### Command Reference

| Command | Aliases | Description | Streaming Support |
|---------|---------|-------------|-------------------|
| `a` | `add`, `create` | Create or add to archive | N/A |
| `x` | `extract` | Extract with full paths | ✓ `--streaming` |
| `e` | `extract-flat` | Extract without directory structure | ✓ `--streaming` |
| `l` | `list` | List archive contents | ✓ `--streaming` |
| `t` | `test` | Test archive integrity | ✓ `--streaming` |

### CLI Options

#### Global Options

- `-v, --verbose`: Enable verbose output
- `-o, --output DIR`: Specify output directory (extract commands)
- `-l, --level LEVEL`: Set compression level 1-22 (create command)
- `--streaming`: Enable streaming mode for memory-efficient processing of large archives
- `--filter FILTER`: Security filter for extraction (extract commands only)
- `--no-atomic`: Disable atomic file operations (create command only, not recommended)

#### Streaming Mode

The `--streaming` flag is available for extract, list, and test operations:

```bash
# Memory-efficient operations on large archives
tzst x large_archive.tzst --streaming
tzst l large_archive.tzst --streaming -v
tzst t large_archive.tzst --streaming
```

**Benefits of streaming mode:**

- Significantly reduced memory usage for large archives
- Better performance when processing archives that don't fit in memory
- Automatic cleanup of resources

**Note:** Some advanced operations may be limited in streaming mode.

#### Security Filters

For enhanced security when extracting archives from untrusted sources, tzst provides extraction filters:

```bash
# Extract with maximum security (default)
tzst x archive.tzst --filter data

# Extract with standard tar compatibility
tzst x archive.tzst --filter tar

# Extract with full trust (dangerous - only for trusted archives)
tzst x archive.tzst --filter fully_trusted
```

**Security Filter Options:**

- `data` (default, recommended): Most secure option. Blocks dangerous files like device files, absolute paths, and paths outside the extraction directory. Sets safe permissions and clears user/group metadata.
- `tar`: Standard tar compatibility. Blocks absolute paths and directory traversal but allows more file types and metadata.
- `fully_trusted`: No security restrictions. Only use with completely trusted archives as it can be exploited for path traversal attacks.

**Security Warning:** Always use the default `data` filter when extracting archives from untrusted sources. Never use `fully_trusted` unless you completely trust the archive source.

## Python API

### TzstArchive Class

The main class for working with tzst archives:

```python
from tzst import TzstArchive

# Create a new archive
with TzstArchive("archive.tzst", "w", compression_level=5) as archive:
    archive.add("file.txt")
    archive.add("directory/", recursive=True)

# Read an existing archive
with TzstArchive("archive.tzst", "r") as archive:
    # List contents
    contents = archive.list(verbose=True)
    
    # Extract specific file with security filter
    archive.extract("file.txt", "output/", filter="data")
    
    # Extract all files (uses 'data' filter by default for security)
    archive.extract(path="output/")
    
    # Extract with different security levels
    archive.extract(path="output/", filter="tar")        # Standard tar compatibility
    archive.extract(path="output/", filter="data")       # Maximum security (default)
    # archive.extract(path="output/", filter="fully_trusted")  # Only for trusted archives!
    
    # Test integrity
    is_valid = archive.test()

# For large archives, use streaming mode to reduce memory usage
with TzstArchive("large_archive.tzst", "r", streaming=True) as archive:
    # Streaming mode is more memory efficient but may limit some operations
    contents = archive.list(verbose=True)
    archive.extract(path="output/")
```

**Important Limitations:**

- **Append Mode Not Supported**: The `TzstArchive` class does not support append mode (`"a"`). If you need to add files to an existing archive, you must either:
  1. Create multiple separate archives
  2. Recreate the entire archive with all files
  3. Use standard tar and compress separately with external tools
  4. Extract the existing archive, add new files, and recompress

### Convenience Functions

#### create_archive()

```python
from tzst import create_archive

# Create archive with atomic file operations (default behavior)
create_archive(
    archive_path="backup.tzst",
    files=["documents/", "photos/", "config.txt"],
    compression_level=10
)

# Disable atomic operations if needed (not recommended)
create_archive(
    archive_path="backup.tzst", 
    files=["documents/"],
    use_temp_file=False
)
```

**Atomic File Operations**: By default, `create_archive()` uses atomic file operations to prevent incomplete archives if the process is interrupted. The archive is first created in a temporary file, then atomically moved to the final location upon successful completion.

#### extract_archive()

```python
from tzst import extract_archive

# Extract with directory structure (uses 'data' filter by default for security)
extract_archive("backup.tzst", "restore/")

# Extract specific files
extract_archive("backup.tzst", "restore/", members=["config.txt"])

# Flatten directory structure
extract_archive("backup.tzst", "restore/", flatten=True)

# Extract with different security filters
extract_archive("backup.tzst", "restore/", filter="data")  # Maximum security (default)
extract_archive("backup.tzst", "restore/", filter="tar")   # Standard tar compatibility

# For large archives, use streaming mode for memory efficiency
extract_archive("large_backup.tzst", "restore/", streaming=True)
```

#### list_archive()

```python
from tzst import list_archive

# Simple listing
files = list_archive("backup.tzst")
for file_info in files:
    print(file_info["name"])

# Detailed listing
files = list_archive("backup.tzst", verbose=True)
for file_info in files:
    print(f"{file_info['name']}: {file_info['size']} bytes, "
          f"modified: {file_info['mtime_str']}")

# Use streaming mode for large archives
files = list_archive("large_backup.tzst", verbose=True, streaming=True)
```

#### test_archive()

```python
from tzst import test_archive

# Basic integrity test
if test_archive("backup.tzst"):
    print("Archive is valid")
else:
    print("Archive is corrupted")

# Test large archive with streaming mode
if test_archive("large_backup.tzst", streaming=True):
    print("Large archive is valid")
```

## File Extensions

The library automatically handles file extensions with intelligent normalization:

- `.tzst` - Primary extension for tar+zstandard archives
- `.tar.zst` - Alternative standard extension
- Auto-detection when opening existing archives
- Automatic extension addition when creating archives

**Extension Behavior:**

- If no extension is provided, `.tzst` is automatically added
- Inconsistent extensions (e.g., `.txt`) are normalized to `.tzst`
- Both `.tzst` and `.tar.zst` are treated as valid and equivalent
- Opening archives automatically detects the correct format regardless of extension

```python
# These all create valid archives
create_archive("backup.tzst", files)      # Creates backup.tzst
create_archive("backup.tar.zst", files)  # Creates backup.tar.zst  
create_archive("backup", files)          # Creates backup.tzst
create_archive("backup.txt", files)      # Creates backup.tzst (normalized)
```

## Compression Levels

Zstandard compression levels range from 1 (fastest) to 22 (best compression):

- **Level 1-3**: Fast compression, larger files
- **Level 3** (default): Good balance of speed and compression
- **Level 10-15**: Better compression, slower
- **Level 20-22**: Maximum compression, much slower

```python
# Fast compression
create_archive("fast.tzst", files, compression_level=1)

# Balanced (default)
create_archive("balanced.tzst", files, compression_level=3)

# Maximum compression
create_archive("compressed.tzst", files, compression_level=22)
```

## Error Handling and Recovery

The library provides comprehensive error handling with specific exception types and helpful error messages:

```python
from tzst import TzstArchive
from tzst.exceptions import (
    TzstError,
    TzstArchiveError,
    TzstCompressionError,
    TzstDecompressionError,
    TzstFileNotFoundError
)

try:
    with TzstArchive("archive.tzst", "r") as archive:
        archive.extract()
except TzstDecompressionError:
    print("Failed to decompress archive")
except TzstArchiveError:
    print("Archive operation failed")
except TzstFileNotFoundError:
    print("Archive file not found")
except KeyboardInterrupt:
    print("Operation interrupted by user")
    # Cleanup is handled automatically
```

### Enhanced Error Messages

The library now provides enhanced error messages with clear alternatives:

```python
# Append mode is not supported, but errors provide helpful alternatives
try:
    with TzstArchive("archive.tzst", "a") as archive:
        archive.add("newfile.txt")
except NotImplementedError as e:
    print(e)  # Detailed message with alternatives:
    # "Append mode is not supported for tzst archives.
    #  Alternatives: 1) Create multiple archives, 2) Recreate the archive,
    #  3) Use standard tar and compress separately."
```

## Safety and Recovery

### Atomic File Operations

All file creation operations use atomic file operations by default to ensure data integrity:

- **Archive Creation**: Archives are created in temporary files first, then atomically moved to final location
- **Interruption Safety**: Automatic cleanup if process is interrupted (Ctrl+C, system shutdown)
- **No Partial Files**: No risk of corrupted or incomplete archives in the final location
- **Cross-Platform**: Works reliably on Windows, macOS, and Linux file systems

**Which Operations Are Atomic:**

- `create_archive()` function (when `use_temp_file=True`, which is default)
- Creating new archives via `TzstArchive` class in write mode
- CLI archive creation commands (`tzst a`, `tzst add`, `tzst create`)

**Which Operations Are Not Atomic:**

- Extraction operations (files are written directly to destination)
- Reading operations (no file modifications)
- Operations with `use_temp_file=False` (not recommended)

```python
# Atomic operations are enabled by default
create_archive("important.tzst", files)  # Safe from interruption

# Can be disabled if needed (not recommended)
create_archive("test.tzst", files, use_temp_file=False)

# Archive class also uses atomic operations
with TzstArchive("backup.tzst", "w") as archive:
    archive.add("documents/")  # Safe from interruption
```

### Enhanced Error Messages

The library provides comprehensive error handling with specific exception types and helpful error messages:

```python
# Append mode example with helpful alternatives
try:
    with TzstArchive("archive.tzst", "a") as archive:
        archive.add("newfile.txt")
except NotImplementedError as e:
    print(e)  # Detailed message with alternatives:
    # "Append mode is not supported for tzst archives.
    #  Alternatives: 1) Create multiple archives, 2) Recreate the archive,
    #  3) Use standard tar and compress separately."
```

### Recovery and Cleanup

The library automatically handles cleanup in various failure scenarios:

- **Process Interruption**: Temporary files are automatically cleaned up
- **Disk Space Issues**: Partial files are removed if creation fails
- **Permission Errors**: No incomplete archives are left behind
- **Memory Errors**: Resources are properly released

## Performance Tips

1. **Choose appropriate compression levels**: Level 3 is usually optimal for most use cases
2. **Use streaming for large archives**: Enable streaming mode (`streaming=True`) for archives larger than 100MB to reduce memory usage significantly
3. **Atomic file operations**: The library uses atomic file operations by default to prevent incomplete archives on interruption - archives are created in temporary files first, then moved atomically
4. **Batch operations**: Add multiple files in a single archive session when possible
5. **Consider file types**: Already compressed files (images, videos) won't compress much further
6. **CLI streaming options**: Use `--streaming` flag in CLI commands for memory-efficient processing of large archives
7. **Compression level selection**: Higher levels (15-22) provide better compression but take significantly longer

## Memory Usage and Streaming

### Memory Usage Guidelines

- **Small archives (<10MB)**: Standard mode is recommended for simplicity
- **Medium archives (10MB-100MB)**: Either mode works well, consider file count and system resources
- **Large archives (>100MB)**: Strongly recommend streaming mode to prevent memory exhaustion
- **Very large archives (>1GB)**: Always use streaming mode; standard mode may cause system instability
- **Limited memory environments**: Use streaming mode regardless of archive size

### Streaming Mode Benefits

- **Reduced Memory Usage**: Process archives without loading entire contents into memory
- **Large File Support**: Handle archives larger than available RAM
- **Better Performance**: Improved performance for sequential access patterns
- **Resource Management**: Automatic cleanup of file handles and temporary resources

### When to Use Streaming

- Archives larger than 100MB
- Limited memory environments
- Processing archives with many large files
- Automated backup/restore operations

```python
# Example: Processing a large backup archive
from tzst import extract_archive, list_archive, test_archive

# Memory-efficient operations
large_archive = "backup_500gb.tzst"

# Test integrity with minimal memory usage
is_valid = test_archive(large_archive, streaming=True)

# List contents without loading entire archive
contents = list_archive(large_archive, streaming=True, verbose=True)

# Extract with streaming for large archives
extract_archive(large_archive, "restore/", streaming=True)
```

## Comparison with Standard Tools

### vs tar + gzip

- **Better compression**: Zstandard typically achieves better compression ratios than gzip
- **Faster decompression**: Zstandard decompresses faster than gzip
- **Modern algorithm**: Zstandard is a more modern compression algorithm

### vs tar + xz

- **Faster compression**: Zstandard is significantly faster than xz at similar compression levels
- **Comparable compression**: Similar compression ratios to xz
- **Better balance**: Better speed/compression trade-off

### vs zip

- **Better compression**: Generally better compression than zip
- **Preserves permissions**: Maintains Unix file permissions and metadata
- **Streaming support**: Better support for large files and streaming

## Requirements

- Python 3.12 or higher
- zstandard >= 0.19.0

## Development

### Setting up Development Environment

This project uses **Hatch** as the build system and dependency manager, with configuration in `pyproject.toml`. Choose one of the following setup methods:

#### Using pip (Traditional approach)

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

#### Using Hatch (Recommended for development)

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install hatch  # Install Hatch if not already installed
hatch env create   # Create development environment
hatch shell        # Activate development environment
```

The `pyproject.toml` file configures the entire build process, including:

- Build system (hatchling)
- Dependencies and optional development dependencies
- Project metadata and entry points
- Tool configurations (pytest, ruff, black)

### Running Tests

#### Using pytest directly

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tzst --cov-report=html

# Run specific test file
pytest tests/test_core.py
```

#### Using Hatch

```bash
# Run tests in development environment
hatch run pytest

# Run with coverage
hatch run pytest --cov=tzst --cov-report=html
```

### Code Quality Tools

#### Using tools directly

```bash
# Check code quality with Ruff
ruff check src tests

# Format code with Black
black src tests

# Type checking (if mypy is installed)
mypy src
```

#### Using Hatch

```bash
# Check code quality with Ruff
hatch run ruff check src tests

# Format code with Black
hatch run black src tests
```

### Building and Distribution

```bash
# Install build dependencies
pip install build

# Build wheel and source distribution
python -m build

# Using Hatch for building
hatch build
```

### Project Documentation

The `pyproject.toml` file serves as the central configuration for the entire project:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "tzst"
description = "A Python library for creating and manipulating .tzst/.tar.zst archives"
# ... additional metadata
```

Key configuration sections:

- **Build system**: Uses Hatchling for modern Python packaging
- **Dependencies**: Runtime and optional development dependencies  
- **Entry points**: CLI command registration
- **Tool configurations**: pytest, ruff, black, and other development tools

## Acknowledgments

- [Meta Zstandard](https://github.com/facebook/zstd) for the excellent compression algorithm
- [python-zstandard](https://github.com/indygreg/python-zstandard) for Python bindings
- The Python community for inspiration and feedback

## License

Copyright &copy; 2025 [Xi Xu](https://xi-xu.me). All rights reserved.

Licensed under the [BSD 3-Clause](LICENSE) license.
