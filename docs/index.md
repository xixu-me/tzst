---
myst:
  html_meta:
    description: "tzst - Next-generation Python library for tar.zst archives with Zstandard compression. Fast, secure, and reliable archive management."
    keywords: "tzst, Python, tar.zst, Zstandard, compression, archive, backup, file management"
    og:title: "tzst - Next-Generation Archive Management"
    og:description: "Fast, secure, and reliable Python library for tar.zst archives with Zstandard compression"
    twitter:title: "tzst - Next-Generation Archive Management"
    twitter:description: "Fast, secure, and reliable Python library for tar.zst archives with Zstandard compression"
---

# tzst Documentation

Welcome to **tzst**, the next-generation Python library engineered for modern archive management, leveraging cutting-edge Zstandard compression to deliver superior performance, security, and reliability.

```{toctree}
:maxdepth: 2
:caption: Contents:

quickstart
api/index
examples
```

```{toctree}
:hidden:

404
README
```

## What is tzst?

**tzst** is a modern Python library built exclusively for Python 3.12+ that provides comprehensive support for creating, extracting, and managing `.tzst` and `.tar.zst` archives. It combines the proven reliability of the tar format with the superior compression efficiency of Zstandard (zstd) to deliver:

- **Superior Performance**: Fast compression and decompression with excellent compression ratios
- **Enterprise-Grade Security**: Safe extraction with built-in protections against path traversal attacks
- **Memory Efficiency**: Streaming mode for handling large archives with minimal memory usage
- **Cross-Platform Compatibility**: Works seamlessly on Windows, macOS, and Linux
- **Developer-Friendly**: Clean, Pythonic API with comprehensive error handling

## Key Features

### 🗜️ Advanced Compression

- **Zstandard Compression**: Best-in-class compression algorithm with configurable levels (1-22)
- **Multiple Extensions**: Support for both `.tzst` and `.tar.zst` file extensions
- **Streaming Support**: Memory-efficient processing for large archives

### 🔒 Security First

- **Safe by Default**: Uses 'data' filter for secure extraction without dangerous path traversal
- **Multiple Filter Options**: Choose from 'data', 'tar', or 'fully_trusted' filters based on your security needs
- **Atomic Operations**: All file operations use temporary files with atomic moves to prevent corruption

### 💻 Dual Interfaces

- **Command Line**: Intuitive CLI with comprehensive options for batch operations
- **Python API**: Clean, object-oriented interface for programmatic use
- **Convenience Functions**: High-level functions for common operations

### ⚡ High Performance

- **Optimized I/O**: Efficient buffering and streaming for large files
- **Conflict Resolution**: Intelligent handling of file conflicts during extraction
- **Cross-Platform**: Native performance on all major operating systems

## Quick Example

```python
from tzst import TzstArchive, create_archive, extract_archive

# Create an archive
create_archive("backup.tzst", ["documents/", "photos/"], compression_level=5)

# Extract an archive
extract_archive("backup.tzst", "restore/")

# Work with archives programmatically
with TzstArchive("data.tzst", "r") as archive:
    contents = archive.list(verbose=True)
    archive.extract("important.txt", "output/")
    is_valid = archive.test()
```

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

### Standalone Binaries

Download platform-specific standalone executables from [GitHub Releases](https://github.com/xixu-me/tzst/releases) - no Python installation required!

## Getting Started

For a quick introduction, see the {doc}`quickstart` guide. For comprehensive usage examples, explore the {doc}`examples` section.

### Installation Options

1. **PyPI Installation** (Recommended): `pip install tzst`
2. **Standalone Binaries**: Download from [GitHub Releases](https://github.com/xixu-me/tzst/releases)
3. **From Source**: Clone and install from repository

### API Documentation

Complete API documentation is available in the {doc}`api/index` section, covering:

- {doc}`api/core`: Main classes and functions
- {doc}`api/cli`: Command-line interface
- {doc}`api/exceptions`: Error handling

## Indices and tables

1. **{doc}`quickstart`** - Get up and running quickly with basic examples
2. **{doc}`examples`** - Comprehensive usage examples and patterns
3. **{doc}`api/index`** - Complete API reference documentation
4. **{doc}`genindex`** - Index of all documented items

## Requirements

- Python 3.12 or higher
- zstandard >= 0.19.0
