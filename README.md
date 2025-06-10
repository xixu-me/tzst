<h1 align="center">
<img src="https://raw.githubusercontent.com/xixu-me/tzst/refs/heads/main/docs/_static/tzst-logo.png" width="300">
</h1><br>

[![codecov](https://codecov.io/gh/xixu-me/tzst/graph/badge.svg?token=2AIN1559WU)](https://codecov.io/gh/xixu-me/tzst)
[![CodeQL](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql)
[![CI/CD](https://github.com/xixu-me/tzst/actions/workflows/ci.yml/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/ci.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/tzst)](https://pypi.org/project/tzst/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/tzst)](https://pypi.org/project/tzst/)
[![GitHub License](https://img.shields.io/github/license/xixu-me/tzst)](LICENSE)
[![Sponsor](https://img.shields.io/badge/Sponsor-violet)](https://xi-xu.me/#sponsorships)
[![Documentation](https://img.shields.io/badge/Documentation-blue)](https://tzst.xi-xu.me)

**🇺🇸 English** | [🇨🇳 汉语](./README.zh.md) | [🇪🇸 español](./README.es.md) | [🇯🇵 日本語](./README.ja.md) | [🇦🇪 العربية](./README.ar.md) | [🇷🇺 русский](./README.ru.md) | [🇩🇪 Deutsch](./README.de.md) | [🇫🇷 français](./README.fr.md) | [🇰🇷 한국어](./README.ko.md) | [🇧🇷 português](./README.pt.md)

**tzst** is a next-generation Python library engineered for modern archive management, leveraging cutting-edge Zstandard compression to deliver superior performance, security, and reliability. Built exclusively for Python 3.12+, this enterprise-grade solution combines atomic operations, streaming efficiency, and a meticulously crafted API to redefine how developers handle `.tzst`/`.tar.zst` archives in production environments. 🚀

## ✨ Features

- **🗜️ High Compression**: Zstandard compression for excellent compression ratios and speed
- **📁 Tar Compatibility**: Creates standard tar archives compressed with Zstandard
- **💻 Command Line Interface**: Intuitive CLI with streaming support and comprehensive options
- **🐍 Python API**: Clean, Pythonic API for programmatic use
- **🌍 Cross-Platform**: Works on Windows, macOS, and Linux
- **📂 Multiple Extensions**: Supports both `.tzst` and `.tar.zst` extensions
- **💾 Memory Efficient**: Streaming mode for handling large archives with minimal memory usage
- **⚡ Atomic Operations**: Safe file operations with automatic cleanup on interruption
- **🔒 Secure by Default**: Uses the 'data' filter for maximum security during extraction
- **🚨 Enhanced Error Handling**: Clear error messages with helpful alternatives

## 📥 Installation

### From GitHub Releases

Download standalone executables that don't require Python installation:

#### Supported Platforms

| Platform | Architecture | File |
|----------|-------------|------|
| **🐧 Linux** | x86_64 | `tzst-{version}-linux-amd64.zip` |
| **🐧 Linux** | ARM64 | `tzst-{version}-linux-arm64.zip` |
| **🪟 Windows** | x64 | `tzst-{version}-windows-amd64.zip` |
| **🪟 Windows** | ARM64 | `tzst-{version}-windows-arm64.zip` |
| **🍎 macOS** | Intel | `tzst-{version}-darwin-amd64.zip` |
| **🍎 macOS** | Apple Silicon | `tzst-{version}-darwin-arm64.zip` |

#### 🛠️ Installation Steps

1. **📥 Download** the appropriate archive for your platform from the [latest releases page](https://github.com/xixu-me/tzst/releases/latest)
2. **📦 Extract** the archive to get the `tzst` executable (or `tzst.exe` on Windows)
3. **📂 Move** the executable to a directory in your PATH:
   - **🐧 Linux/macOS**: `sudo mv tzst /usr/local/bin/`
   - **🪟 Windows**: Add the directory containing `tzst.exe` to your PATH environment variable
4. **✅ Verify** installation: `tzst --help`

#### 🎯 Benefits of Binary Installation

- ✅ **No Python required** - Standalone executable
- ✅ **Faster startup** - No Python interpreter overhead
- ✅ **Easy deployment** - Single file distribution
- ✅ **Consistent behavior** - Bundled dependencies

### 📦 From PyPI

```bash
pip install tzst
```

### 🔧 From Source

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

### 🚀 Development Installation

This project uses modern Python packaging standards:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

## 🚀 Quick Start

### 💻 Command Line Usage

> **Note**: Download the [standalone binary](#from-github-releases) for the best performance and no Python dependency. Alternatively, use `uvx tzst` for running without installation. See [uv documentation](https://docs.astral.sh/uv/) for details.

```bash
# 📁 Create an archive
tzst a archive.tzst file1.txt file2.txt directory/

# 📤 Extract an archive
tzst x archive.tzst

# 📋 List archive contents
tzst l archive.tzst

# 🧪 Test archive integrity
tzst t archive.tzst
```

### 🐍 Python API Usage

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

## 💻 Command Line Interface

### 📁 Archive Operations

#### ➕ Create Archive

```bash
# Basic usage
tzst a archive.tzst file1.txt file2.txt

# With compression level (1-22, default: 3)
tzst a archive.tzst files/ -l 15

# Alternative commands
tzst add archive.tzst files/
tzst create archive.tzst files/
```

#### 📤 Extract Archive

```bash
# Extract with full directory structure
tzst x archive.tzst

# Extract to specific directory
tzst x archive.tzst -o output/

# Extract specific files
tzst x archive.tzst file1.txt dir/file2.txt

# Extract without directory structure (flat)
tzst e archive.tzst -o output/

# Use streaming mode for large archives
tzst x archive.tzst --streaming -o output/
```

#### 📋 List Contents

```bash
# Simple listing
tzst l archive.tzst

# Verbose listing with details
tzst l archive.tzst -v

# Use streaming mode for large archives
tzst l archive.tzst --streaming -v
```

#### 🧪 Test Integrity

```bash
# Test archive integrity
tzst t archive.tzst

# Test with streaming mode
tzst t archive.tzst --streaming
```

### 📊 Command Reference

| Command | Aliases | Description | Streaming Support |
|---------|---------|-------------|-------------------|
| `a` | `add`, `create` | Create or add to archive | N/A |
| `x` | `extract` | Extract with full paths | ✓ `--streaming` |
| `e` | `extract-flat` | Extract without directory structure | ✓ `--streaming` |
| `l` | `list` | List archive contents | ✓ `--streaming` |
| `t` | `test` | Test archive integrity | ✓ `--streaming` |

### ⚙️ CLI Options

- `-v, --verbose`: Enable verbose output
- `-o, --output DIR`: Specify output directory (extract commands)
- `-l, --level LEVEL`: Set compression level 1-22 (create command)
- `--streaming`: Enable streaming mode for memory-efficient processing
- `--filter FILTER`: Security filter for extraction (data/tar/fully_trusted)
- `--no-atomic`: Disable atomic file operations (not recommended)

### 🔒 Security Filters

```bash
# Extract with maximum security (default)
tzst x archive.tzst --filter data

# Extract with standard tar compatibility
tzst x archive.tzst --filter tar

# Extract with full trust (dangerous - only for trusted archives)
tzst x archive.tzst --filter fully_trusted
```

**🔐 Security Filter Options:**

- `data` (default): Most secure. Blocks dangerous files, absolute paths, and paths outside extraction directory
- `tar`: Standard tar compatibility. Blocks absolute paths and directory traversal
- `fully_trusted`: No security restrictions. Only use with completely trusted archives

## 🐍 Python API

### 📦 TzstArchive Class

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
    
    # Extract with security filter
    archive.extract("file.txt", "output/", filter="data")
    
    # Test integrity
    is_valid = archive.test()

# For large archives, use streaming mode
with TzstArchive("large_archive.tzst", "r", streaming=True) as archive:
    archive.extract(path="output/")
```

**⚠️ Important Limitations:**

- **❌ Append Mode Not Supported**: Create multiple archives or recreate the entire archive instead

### 🎯 Convenience Functions

#### 📁 create_archive()

```python
from tzst import create_archive

# Create with atomic operations (default)
create_archive(
    archive_path="backup.tzst",
    files=["documents/", "photos/", "config.txt"],
    compression_level=10
)
```

#### 📤 extract_archive()

```python
from tzst import extract_archive

# Extract with security (default: 'data' filter)
extract_archive("backup.tzst", "restore/")

# Extract specific files
extract_archive("backup.tzst", "restore/", members=["config.txt"])

# Flatten directory structure
extract_archive("backup.tzst", "restore/", flatten=True)

# Use streaming for large archives
extract_archive("large_backup.tzst", "restore/", streaming=True)
```

#### 📋 list_archive()

```python
from tzst import list_archive

# Simple listing
files = list_archive("backup.tzst")

# Detailed listing
files = list_archive("backup.tzst", verbose=True)

# Streaming for large archives
files = list_archive("large_backup.tzst", streaming=True)
```

#### 🧪 test_archive()

```python
from tzst import test_archive

# Basic integrity test
if test_archive("backup.tzst"):
    print("Archive is valid")

# Test with streaming
if test_archive("large_backup.tzst", streaming=True):
    print("Large archive is valid")
```

## 🔧 Advanced Features

### 📂 File Extensions

The library automatically handles file extensions with intelligent normalization:

- `.tzst` - Primary extension for tar+zstandard archives
- `.tar.zst` - Alternative standard extension
- Auto-detection when opening existing archives
- Automatic extension addition when creating archives

```python
# These all create valid archives
create_archive("backup.tzst", files)      # Creates backup.tzst
create_archive("backup.tar.zst", files)  # Creates backup.tar.zst  
create_archive("backup", files)          # Creates backup.tzst
create_archive("backup.txt", files)      # Creates backup.tzst (normalized)
```

### 🗜️ Compression Levels

Zstandard compression levels range from 1 (fastest) to 22 (best compression):

- **Level 1-3**: Fast compression, larger files
- **Level 3** (default): Good balance of speed and compression
- **Level 10-15**: Better compression, slower
- **Level 20-22**: Maximum compression, much slower

### 🌊 Streaming Mode

Use streaming mode for memory-efficient processing of large archives:

**✅ Benefits:**

- Significantly reduced memory usage
- Better performance for archives that don't fit in memory
- Automatic cleanup of resources

**🎯 When to Use:**

- Archives larger than 100MB
- Limited memory environments
- Processing archives with many large files

```python
# Example: Processing a large backup archive
from tzst import extract_archive, list_archive, test_archive

large_archive = "backup_500gb.tzst"

# Memory-efficient operations
is_valid = test_archive(large_archive, streaming=True)
contents = list_archive(large_archive, streaming=True, verbose=True)
extract_archive(large_archive, "restore/", streaming=True)
```

### ⚡ Atomic Operations

All file creation operations use atomic file operations by default:

- Archives created in temporary files first, then atomically moved
- Automatic cleanup if process is interrupted
- No risk of corrupted or incomplete archives
- Cross-platform compatibility

```python
# Atomic operations enabled by default
create_archive("important.tzst", files)  # Safe from interruption

# Can be disabled if needed (not recommended)
create_archive("test.tzst", files, use_temp_file=False)
```

### 🚨 Error Handling

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
except TzstFileNotFoundError:
    print("Archive file not found")
except KeyboardInterrupt:
    print("Operation interrupted by user")
    # Cleanup handled automatically
```

## 🚀 Performance and Comparison

### 💡 Performance Tips

1. **🗜️ Compression levels**: Level 3 is optimal for most use cases
2. **🌊 Streaming**: Use for archives larger than 100MB
3. **📦 Batch operations**: Add multiple files in single session
4. **📄 File types**: Already compressed files won't compress much further

### 🆚 vs Other Tools

**vs tar + gzip:**

- ✅ Better compression ratios
- ⚡ Faster decompression
- 🔄 Modern algorithm

**vs tar + xz:**

- 🚀 Significantly faster compression
- 📊 Similar compression ratios
- ⚖️ Better speed/compression trade-off

**vs zip:**

- 🗜️ Better compression
- 🔐 Preserves Unix permissions and metadata
- 🌊 Better streaming support

## 📋 Requirements

- 🐍 Python 3.12 or higher
- 📦 zstandard >= 0.19.0

## 🛠️ Development

### 🚀 Setting up Development Environment

This project uses modern Python packaging standards:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

### 🧪 Running Tests

```bash
# Run tests with coverage
pytest --cov=tzst --cov-report=html

# Or use the simpler command (coverage settings are in pyproject.toml)
pytest
```

### ✨ Code Quality

```bash
# Check code quality
ruff check src tests

# Format code
ruff format src tests
```

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for:

- Development setup and project structure
- Code style guidelines and best practices  
- Testing requirements and writing tests
- Pull request process and review workflow

### 🚀 Quick Start for Contributors

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
python -m pytest tests/
```

### 🎯 Types of Contributions Welcome

- 🐛 **Bug fixes** - Fix issues in existing functionality
- ✨ **Features** - Add new capabilities to the library
- 📚 **Documentation** - Improve or add documentation
- 🧪 **Tests** - Add or improve test coverage
- ⚡ **Performance** - Optimize existing code
- 🔒 **Security** - Address security vulnerabilities

## 🙏 Acknowledgments

- [Meta Zstandard](https://github.com/facebook/zstd) for the excellent compression algorithm
- [python-zstandard](https://github.com/indygreg/python-zstandard) for Python bindings
- The Python community for inspiration and feedback

## 📄 License

Copyright &copy; 2025 [Xi Xu](https://xi-xu.me). All rights reserved.

Licensed under the [BSD 3-Clause](LICENSE) license.
