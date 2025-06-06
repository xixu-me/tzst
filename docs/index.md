---
myst:
  html_meta:
    description: "tzst - Next-generation Python library for tar.zst archives with Zstandard compression. Fast, secure, and reliable archive management."
    keywords: "tzst, Python, tar.zst, Zstandard, compression, archive, backup, file management"
    og:title: "tzst - Next-Generation Archive Management"
    og:description: "Fast, secure, and reliable Python library for tar.zst archives with Zstandard compression"
    twitter:title: "tzst - Next-Generation Archive Management"
    twitter:description: "Fast, secure, and reliable Python library for tar.zst archives with Zstandard compression"
    og:type: "website"
    og:image: "https://tzst.xi-xu.me/_static/tzst-square-logo.png"
    og:url: "https://tzst.xi-xu.me/"
    twitter:card: "summary_large_image"
    twitter:image: "https://tzst.xi-xu.me/_static/tzst-square-logo.png"
---

# tzst Documentation

[![codecov](https://codecov.io/gh/xixu-me/tzst/graph/badge.svg?token=2AIN1559WU)](https://codecov.io/gh/xixu-me/tzst)
[![CodeQL](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql)
[![CI/CD](https://github.com/xixu-me/tzst/actions/workflows/ci.yml/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/ci.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/tzst)](https://pypi.org/project/tzst/)
[![GitHub License](https://img.shields.io/github/license/xixu-me/tzst)](https://github.com/xixu-me/tzst/blob/main/LICENSE)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/tzst)](https://pypi.org/project/tzst/)
[![GitHub Stars](https://img.shields.io/github/stars/xixu-me/tzst?style=social)
[![Sponsor](https://img.shields.io/badge/Sponsor-violet)](https://xi-xu.me/#sponsorships)

Welcome to **tzst**, the next-generation Python library engineered for modern archive management, leveraging cutting-edge Zstandard compression to deliver superior performance, security, and reliability.

```{toctree}
:maxdepth: 2
:caption: Contents:

quickstart
performance
examples
api/index
development
genindex
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

### Advanced Compression

- **Zstandard Compression**: Best-in-class compression algorithm with configurable levels (1-22)
- **Multiple Extensions**: Support for both `.tzst` and `.tar.zst` file extensions
- **Streaming Support**: Memory-efficient processing for large archives

### Security First

- **Safe by Default**: Uses 'data' filter for secure extraction without dangerous path traversal
- **Multiple Filter Options**: Choose from 'data', 'tar', or 'fully_trusted' filters based on your security needs
- **Atomic Operations**: All file operations use temporary files with atomic moves to prevent corruption

### Dual Interfaces

- **Command Line**: Intuitive CLI with comprehensive options for batch operations
- **Python API**: Clean, object-oriented interface for programmatic use
- **Convenience Functions**: High-level functions for common operations

### High Performance

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

### From GitHub Releases

Download platform-specific standalone executables from [GitHub Releases](https://github.com/xixu-me/tzst/releases) - no Python installation required!

#### Supported Platforms

| Platform | Architecture | File |
|----------|-------------|------|
| **Linux** | x86_64 | `tzst-v{version}-linux-x86_64.zip` |
| **Linux** | ARM64 | `tzst-v{version}-linux-aarch64.zip` |
| **Windows** | x64 | `tzst-v{version}-windows-amd64.zip` |
| **Windows** | ARM64 | `tzst-v{version}-windows-arm64.zip` |
| **macOS** | Intel | `tzst-v{version}-macos-x86_64.zip` |
| **macOS** | Apple Silicon | `tzst-v{version}-macos-arm64.zip` |

#### Installation Steps

1. **Download** the appropriate archive for your platform from the [latest releases page](https://github.com/xixu-me/tzst/releases/latest)
2. **Extract** the archive to get the `tzst` executable (or `tzst.exe` on Windows)
3. **Move** the executable to a directory in your PATH:
   - **Linux/macOS**: `sudo mv tzst /usr/local/bin/`
   - **Windows**: Add the directory containing `tzst.exe` to your PATH environment variable
4. **Verify** installation: `tzst --help`

#### Benefits of Binary Installation

- **No Python required** - Standalone executable
- **Faster startup** - No Python interpreter overhead
- **Easy deployment** - Single file distribution
- **Consistent behavior** - Bundled dependencies

### Using uvx (No Installation)

Run tzst directly without installation using [uvx](https://docs.astral.sh/uv/):

```bash
uvx tzst --help
uvx tzst a archive.tzst file1.txt file2.txt directory/
uvx tzst x archive.tzst
```

Perfect for one-time usage, testing, CI/CD pipelines, and isolated environments.

### From Source

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

## Getting Started

For a quick introduction, see the {doc}`quickstart` guide. For comprehensive usage examples, explore the {doc}`examples` section.

### Installation Options

1. **PyPI Installation**: `pip install tzst`
2. **Standalone Binaries**: Download from [GitHub Releases](https://github.com/xixu-me/tzst/releases)
3. **uvx (No Installation)**: Run directly with `uvx tzst`
4. **From Source**: Clone and install from repository

### API Documentation

Complete API documentation is available in the {doc}`api/index` section, covering:

- {doc}`api/core`: Main classes and functions
- {doc}`api/cli`: Command-line interface
- {doc}`api/exceptions`: Error handling

## Development

For comprehensive development information, see the {doc}`development` guide, which covers:

- Setting up development environment
- Running tests and code quality checks
- Documentation building
- Contributing workflow and guidelines
- Project structure and best practices

### Quick Start

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
pytest
```

## Contributing

We welcome contributions! Please read our [Contributing Guide](https://github.com/xixu-me/tzst/blob/main/CONTRIBUTING.md) for:

- Development setup and project structure
- Code style guidelines and best practices  
- Testing requirements and writing tests
- Pull request process and review workflow

### Types of Contributions Welcome

- **Bug fixes** - Fix issues in existing functionality
- **Features** - Add new capabilities to the library
- **Documentation** - Improve or add documentation
- **Tests** - Add or improve test coverage
- **Performance** - Optimize existing code
- **Security** - Address security vulnerabilities

## Acknowledgments

- [Meta Zstandard](https://github.com/facebook/zstd) for the excellent compression algorithm
- [python-zstandard](https://github.com/indygreg/python-zstandard) for Python bindings
- The Python community for inspiration and feedback

## License

Copyright © 2025 [Xi Xu](https://xi-xu.me). All rights reserved.

Licensed under the [BSD 3-Clause](https://github.com/xixu-me/tzst/blob/main/LICENSE) license.

## Documentation Guide

1. **{doc}`quickstart`** - Get up and running quickly with basic examples
2. **{doc}`performance`** - Performance optimization guide and comparisons
3. **{doc}`examples`** - Comprehensive usage examples and patterns
4. **{doc}`api/index`** - Complete API reference documentation
5. **{doc}`development`** - Development and contribution guidelines
6. **{ref}`genindex`** - Index of all documented items

## Requirements

- Python 3.12 or higher
- zstandard >= 0.19.0
