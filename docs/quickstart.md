# Quick Start Guide

This guide will get you up and running with tzst in just a few minutes.

## Installation

Choose your preferred installation method:

### Option 1: PyPI (Recommended)

```bash
pip install tzst
```

### Option 2: Standalone Binary

Download the appropriate executable from [GitHub Releases](https://github.com/xixu-me/tzst/releases):

| Platform | Architecture | Download |
|----------|--------------|----------|
| **🐧 Linux** | x86_64 | `tzst-v{version}-linux-x86_64.zip` |
| **🐧 Linux** | ARM64 | `tzst-v{version}-linux-aarch64.zip` |
| **🪟 Windows** | x64 | `tzst-v{version}-windows-amd64.zip` |
| **🪟 Windows** | ARM64 | `tzst-v{version}-windows-arm64.zip` |
| **🍎 macOS** | Intel | `tzst-v{version}-macos-x86_64.zip` |
| **🍎 macOS** | Apple Silicon | `tzst-v{version}-macos-arm64.zip` |

Extract the archive and add the executable to your PATH.

### Option 3: From Source

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

## Basic Usage

### Command Line Interface

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

## Important Concepts

### Compression Levels

tzst supports compression levels from 1 to 22:

- **Level 1-3**: Fast compression, larger files (good for temporary archives)
- **Level 4-6**: Balanced compression and speed (recommended for most use cases)
- **Level 7-15**: Higher compression, slower (good for long-term storage)
- **Level 16-22**: Maximum compression, much slower (for size-critical applications)

```python
# Fast compression
create_archive("temp.tzst", files, compression_level=1)

# Balanced (default)
create_archive("backup.tzst", files, compression_level=3)

# High compression
create_archive("archive.tzst", files, compression_level=9)

# Maximum compression
create_archive("minimal.tzst", files, compression_level=22)
```

### Security Filters

tzst provides extraction filters to protect against malicious archives:

```python
# Safe data extraction (default, recommended)
extract_archive("archive.tzst", "output/", filter="data")

# Preserve more tar features but still secure
extract_archive("archive.tzst", "output/", filter="tar")

# Full trust mode (use only with trusted archives)
extract_archive("archive.tzst", "output/", filter="fully_trusted")
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

### Handling File Conflicts

Handle file conflicts during extraction:

```python
from tzst import ConflictResolution

# Skip existing files
extract_archive("archive.tzst", "output/", 
                conflict_resolution=ConflictResolution.SKIP)

# Replace all existing files
extract_archive("archive.tzst", "output/", 
                conflict_resolution=ConflictResolution.REPLACE_ALL)

# Auto-rename conflicting files
extract_archive("archive.tzst", "output/", 
                conflict_resolution=ConflictResolution.AUTO_RENAME_ALL)
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
        print("❌ Archive is corrupted!")
        return False
    
    # List contents
    contents = list_archive(archive_path, verbose=True)
    total_size = sum(item['size'] for item in contents if item['is_file'])
    file_count = sum(1 for item in contents if item['is_file'])
    
    print(f"✅ Archive is valid")
    print(f"📁 Files: {file_count}")
    print(f"📦 Total size: {total_size / 1024 / 1024:.1f} MB")
    
    return True
```

## Further Learning

- Explore {doc}`examples` for more advanced usage patterns
- Check the {doc}`api/index` for complete API documentation
- Read the full {doc}`README` for additional features and background
