---
myst:
  html_meta:
    description: "Quick start guide for tzst - Learn how to install and use the Python tar.zst archive library in minutes"
    keywords: "tzst tutorial, Python archive tutorial, tar.zst guide, Zstandard compression guide"
    og:title: "tzst Quick Start Guide"
    og:description: "Learn how to install and use tzst for Python tar.zst archive management in minutes"
    twitter:title: "tzst Quick Start Guide"
    twitter:description: "Learn how to install and use tzst for Python tar.zst archive management in minutes"
    og:type: "website"
    og:image: "https://tzst.xi-xu.me/_static/tzst-square-logo.png"
    og:url: "https://tzst.xi-xu.me/"
    twitter:card: "summary_large_image"
    twitter:image: "https://tzst.xi-xu.me/_static/tzst-square-logo.png"
---

# Quick Start Guide

This guide will get you up and running with tzst in just a few minutes.

(installation)=

## Installation

Choose your preferred installation method:

### Option 1: PyPI

```bash
pip install tzst
```

### Option 2: Standalone Binary

Download the appropriate executable from [GitHub Releases](https://github.com/xixu-me/tzst/releases):

| Platform | Architecture | Download |
|----------|--------------|----------|
| **Linux** | x86_64 | `tzst-{version}-linux-amd64.zip` |
| **Linux** | ARM64 | `tzst-{version}-linux-arm64.zip` |
| **Windows** | x64 | `tzst-{version}-windows-amd64.zip` |
| **Windows** | ARM64 | `tzst-{version}-windows-arm64.zip` |
| **macOS** | Intel | `tzst-{version}-darwin-amd64.zip` |
| **macOS** | Apple Silicon | `tzst-{version}-darwin-arm64.zip` |

Extract the archive and add the executable to your PATH.

### Option 3: Using uvx (No Installation)

Run tzst directly without installation using [uvx](https://docs.astral.sh/uv/):

```bash
uvx tzst --help
uvx tzst a archive.tzst file1.txt file2.txt directory/
uvx tzst x archive.tzst
```

This option is perfect for:

- **One-time usage** - No permanent installation needed
- **Testing** - Try tzst without committing to installation
- **CI/CD pipelines** - Use tzst in automated workflows
- **Isolated environments** - Avoid dependency conflicts

### Option 4: From Source

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

(basic-usage)=

## Basic Usage

### Command Line Interface

> **Note**: Download the [standalone binary](installation) for the best performance and no Python dependency. Alternatively, use `uvx tzst` for running without installation. See [uv documentation](https://docs.astral.sh/uv/) for details.

The CLI provides four main operations:

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

### Command Reference

| Command | Aliases | Description | Streaming Support |
|---------|---------|-------------|-------------------|
| `a` | `add`, `create` | Create or add to archive | N/A |
| `x` | `extract` | Extract with full paths | `--streaming` |
| `e` | `extract-flat` | Extract without directory structure | `--streaming` |
| `l` | `list` | List archive contents | `--streaming` |
| `t` | `test` | Test archive integrity | `--streaming` |

### CLI Options

- `-v, --verbose`: Enable verbose output
- `-o, --output DIR`: Specify output directory (extract commands)
- `-l, --level LEVEL`: Set compression level 1-22 (create command)
- `--streaming`: Enable streaming mode for memory-efficient processing
- `--filter FILTER`: Security filter for extraction (data/tar/fully_trusted)
- `--no-atomic`: Disable atomic file operations (not recommended)

#### Create Archives

```bash
# Create archive with default compression (level 3)
tzst a backup.tzst documents/ photos/

# Create with high compression
tzst a backup.tzst documents/ photos/ --compression-level 9

# Create from current directory
tzst a project.tzst .

# Specify different output location
tzst a /backups/data.tzst /home/user/important/
```

#### Extract Archives

```bash
# Extract to current directory
tzst x backup.tzst

# Extract to specific directory
tzst x backup.tzst --output /restore/

# Extract specific files only
tzst x backup.tzst documents/report.pdf photos/vacation.jpg

# Extract with conflict resolution
tzst x backup.tzst --conflict-resolution skip
```

#### List Contents

```bash
# Simple listing
tzst l backup.tzst

# Detailed listing with file info
tzst l backup.tzst --verbose

# Stream large archives efficiently
tzst l huge-archive.tzst --streaming
```

### Python API

#### Quick Start

```python
from tzst import create_archive, extract_archive, list_archive, test_archive

# Create an archive
create_archive("backup.tzst", ["documents/", "photos/"], compression_level=5)

# Extract an archive
extract_archive("backup.tzst", "restore/")

# List contents
contents = list_archive("backup.tzst", verbose=True)
for item in contents:
    print(f"{item['name']} - {item['size']} bytes")

# Test integrity
is_valid = test_archive("backup.tzst")
print(f"Archive is {'valid' if is_valid else 'corrupted'}")
```

#### Using the TzstArchive Class

```python
from tzst import TzstArchive

# Create a new archive
with TzstArchive("data.tzst", "w", compression_level=6) as archive:
    archive.add("file.txt")
    archive.add("directory/", recursive=True)
    
    # Add with custom archive name
    archive.add("config/prod.yaml", arcname="config.yaml")

# Read an existing archive
with TzstArchive("data.tzst", "r") as archive:
    # List contents
    contents = archive.list(verbose=True)
    for item in contents:
        print(f"{item['name']} - {item['size']} bytes")
    
    # Test integrity
    is_valid = archive.test()
    print(f"Archive is {'valid' if is_valid else 'corrupted'}")
    
    # Extract specific files
    archive.extract("file.txt", "output/")
    
    # Extract all files
    archive.extractall("restore/")
```

## Advanced Features

### Security and Filtering

```python
from tzst import extract_archive

# Safe extraction with built-in security (default)
extract_archive("untrusted.tzst", "safe-output/", filter="data")

# For trusted archives with special features
extract_archive("trusted.tzst", "output/", filter="tar")
```

### Security Filters

tzst provides three security filter options for extraction:

```python
from tzst import extract_archive

# Extract with maximum security (default)
extract_archive("archive.tzst", "output/", filter="data")

# Extract with standard tar compatibility
extract_archive("archive.tzst", "output/", filter="tar")

# Extract with full trust (dangerous - only for trusted archives)
extract_archive("archive.tzst", "output/", filter="fully_trusted")
```

**Security Filter Options:**

- `data` (default): Most secure. Blocks dangerous files, absolute paths, and paths outside extraction directory
- `tar`: Standard tar compatibility. Blocks absolute paths and directory traversal
- `fully_trusted`: No security restrictions. Only use with completely trusted archives

### Conflict Resolution

```python
from tzst import extract_archive, ConflictResolution

# Skip existing files
extract_archive("archive.tzst", "output/",
                conflict_resolution=ConflictResolution.SKIP_ALL)

# Auto-rename conflicting files
extract_archive("archive.tzst", "output/",
                conflict_resolution=ConflictResolution.AUTO_RENAME_ALL)
```

### Performance Optimization

```python
from tzst import create_archive, extract_archive

# Create with different compression levels
create_archive("fast.tzst", files, compression_level=1)    # Fastest
create_archive("balanced.tzst", files, compression_level=6) # Balanced
create_archive("best.tzst", files, compression_level=22)   # Best compression

# Memory-efficient operations for large archives
extract_archive("huge-archive.tzst", "output/", streaming=True)
```

### Streaming Mode

For large archives (>100MB), use streaming mode to reduce memory usage:

```python
# Memory-efficient operations
with TzstArchive("large-archive.tzst", "r", streaming=True) as archive:
    contents = archive.list()
    archive.extractall("output/")
    is_valid = archive.test()
```

**Note**: Streaming mode has limitations - you cannot extract specific files or use random access operations.

### File Extensions

The library automatically handles file extensions with intelligent normalization:

- `.tzst` - Primary extension for tar+zstandard archives
- `.tar.zst` - Alternative standard extension
- Auto-detection when opening existing archives
- Automatic extension addition when creating archives

```python
from tzst import create_archive

# These all create valid archives
create_archive("backup.tzst", files)      # Creates backup.tzst
create_archive("backup.tar.zst", files)  # Creates backup.tar.zst  
create_archive("backup", files)          # Creates backup.tzst
create_archive("backup.txt", files)      # Creates backup.tzst (normalized)
```

### Atomic Operations

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

## Error Handling

```python
from tzst import create_archive, TzstArchiveError, TzstCompressionError

try:
    create_archive("backup.tzst", ["documents/"])
except TzstCompressionError as e:
    print(f"Compression failed: {e}")
except TzstArchiveError as e:
    print(f"Archive operation failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Next Steps

- Explore comprehensive {doc}`examples` for real-world scenarios
- Check the {doc}`api/index` for detailed API documentation
- See advanced features like atomic operations and custom filters
- Learn about integration with web frameworks and automation tools

## Read an Existing Archive

```python
with TzstArchive("data.tzst", "r") as archive:
    # List contents
    contents = archive.list(verbose=True)
    
    # Extract specific file
    archive.extract("file.txt", "output/")
    
    # Test integrity
    is_valid = archive.test()
    
    # Get raw member information
    members = archive.getmembers()
```

## Common Patterns

### Backup Script

```python
#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
from tzst import create_archive

def create_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}.tzst"
    
    # Backup important directories
    directories = ["documents/", "projects/", "config/"]
    
    print(f"Creating backup: {backup_name}")
    create_archive(backup_name, directories, compression_level=6)
    print(f"Backup created: {Path(backup_name).stat().st_size / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    create_backup()
```

### Archive Verification

```python
from tzst import test_archive, list_archive

def verify_archive(archive_path):
    print(f"Verifying {archive_path}...")
    
    # Test integrity
    if not test_archive(archive_path):
        print("Archive is corrupted!")
        return False
    
    # List contents
    contents = list_archive(archive_path, verbose=True)
    total_size = sum(item['size'] for item in contents if item['is_file'])
    file_count = sum(1 for item in contents if item['is_file'])
    print(f"Archive is valid")
    print(f"Files: {file_count}")
    print(f"Total size: {total_size / 1024 / 1024:.1f} MB")
    
    return True
```

## Further Learning

- Explore {doc}`examples` for more advanced usage patterns
- Check {doc}`performance` for detailed performance guidance
- Refer to the {doc}`api/index` for complete API documentation
