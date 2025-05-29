# tzst

A Python library for creating and manipulating `.tzst`/`.tar.zst` archives using Zstandard compression.

[![CI/CD](https://github.com/xixu-me/tzst/workflows/CI/CD/badge.svg)](https://github.com/xixu-me/tzst/actions)
[![PyPI version](https://badge.fury.io/py/tzst.svg)](https://badge.fury.io/py/tzst)
[![Python versions](https://img.shields.io/pypi/pyversions/tzst.svg)](https://pypi.org/project/tzst/)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

## Features

- **High Compression**: Uses Zstandard compression for excellent compression ratios and speed
- **Tar Compatibility**: Creates standard tar archives compressed with Zstandard
- **Command Line Interface**: Easy-to-use CLI with intuitive commands
- **Python API**: Clean, Pythonic API for programmatic use
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Multiple Extensions**: Supports both `.tzst` and `.tar.zst` extensions
- **Flexible Extraction**: Extract with full paths or flatten directory structure

## Installation

### From PyPI

```bash
pip install tzst
```

### From Source

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

## Quick Start

### Command Line Usage

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
```

#### List Contents

```bash
# Simple listing
tzst l archive.tzst

# Verbose listing with details
tzst l archive.tzst -v
```

#### Test Integrity

```bash
# Test archive integrity
tzst t archive.tzst
```

### Command Reference

| Command | Aliases | Description |
|---------|---------|-------------|
| `a` | `add`, `create` | Create or add to archive |
| `x` | `extract` | Extract with full paths |
| `e` | `extract-flat` | Extract without directory structure |
| `l` | `list` | List archive contents |
| `t` | `test` | Test archive integrity |

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
    
    # Extract specific file
    archive.extract("file.txt", "output/")
    
    # Extract all files
    archive.extract(path="output/")
    
    # Test integrity
    is_valid = archive.test()
```

### Convenience Functions

#### create_archive()

```python
from tzst import create_archive

create_archive(
    archive_path="backup.tzst",
    files=["documents/", "photos/", "config.txt"],
    compression_level=10
)
```

#### extract_archive()

```python
from tzst import extract_archive

# Extract with directory structure
extract_archive("backup.tzst", "restore/")

# Extract specific files
extract_archive("backup.tzst", "restore/", members=["config.txt"])

# Flatten directory structure
extract_archive("backup.tzst", "restore/", flatten=True)
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
```

#### test_archive()

```python
from tzst import test_archive

if test_archive("backup.tzst"):
    print("Archive is valid")
else:
    print("Archive is corrupted")
```

## File Extensions

The library automatically handles file extensions:

- `.tzst` - Primary extension for tar+zstandard archives
- `.tar.zst` - Alternative standard extension
- Auto-detection when opening existing archives
- Automatic extension addition when creating archives

```python
# These all create valid archives
create_archive("backup.tzst", files)      # Creates backup.tzst
create_archive("backup.tar.zst", files)  # Creates backup.tar.zst  
create_archive("backup", files)          # Creates backup.tzst
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

## Error Handling

The library provides specific exception types for different error conditions:

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
```

## Performance Tips

1. **Choose appropriate compression levels**: Level 3 is usually optimal for most use cases
2. **Use streaming for large files**: The library handles large files efficiently
3. **Batch operations**: Add multiple files in a single archive session when possible
4. **Consider file types**: Already compressed files (images, videos) won't compress much further

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

- Python 3.8 or higher
- zstandard >= 0.19.0

## Development

### Setting up Development Environment

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tzst --cov-report=html

# Run specific test file
pytest tests/test_core.py
```

### Code Quality

```bash
# Lint code
ruff check src tests

# Format code
black src tests

# Type checking (if mypy is installed)
mypy src
```

### Building Documentation

```bash
# Install documentation dependencies
pip install -e .[dev]

# Build documentation (if sphinx is set up)
cd docs
make html
```

## Acknowledgments

- [Meta Zstandard](https://github.com/facebook/zstd) for the excellent compression algorithm
- [python-zstandard](https://github.com/indygreg/python-zstandard) for Python bindings
- The Python community for inspiration and feedback

## Support

- **Documentation**: [Full documentation](https://github.com/xixu-me/tzst#readme)
- **PyPI Package**: [tzst on PyPI](https://pypi.org/project/tzst/)

## License

Copyright &copy; [Xi Xu](https://xi-xu.me). All rights reserved.

Licensed under the [BSD 3-Clause](LICENSE) license.
