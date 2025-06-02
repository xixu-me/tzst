# Quick Start Guide

This guide will help you get started with tzst quickly and efficiently.

## Installation

Install tzst using pip:

```bash
pip install tzst
```

## Basic Usage

### Creating Archives

Use the `TzstArchive` class or convenience functions to create archives:

```python
from tzst import TzstArchive, create_archive

# Using TzstArchive class
with TzstArchive("my_archive.tzst", "w", compression_level=5) as archive:
    archive.add("file.txt")
    archive.add("directory/", recursive=True)

# Using convenience function
create_archive(
    archive_path="backup.tzst",
    files=["documents/", "photos/", "config.txt"],
    compression_level=10
)
```

### Extracting Archives

Extract archives safely with built-in security filters:

```python
from tzst import TzstArchive, extract_archive

# Using TzstArchive class
with TzstArchive("my_archive.tzst", "r") as archive:
    # Extract all files with security filter
    archive.extract("output/", filter="data")
    
    # Extract specific files
    archive.extract("output/", members=["file.txt"], filter="data")

# Using convenience function
extract_archive("backup.tzst", "restore/")
```

### Listing Archive Contents

View what's inside an archive:

```python
from tzst import TzstArchive, list_archive

# Using TzstArchive class
with TzstArchive("my_archive.tzst", "r") as archive:
    contents = archive.list(verbose=True)
    for item in contents:
        print(f"{item['name']} - {item['size']} bytes")

# Using convenience function
files = list_archive("backup.tzst", verbose=True)
```

### Testing Archive Integrity

Verify that an archive is valid:

```python
from tzst import TzstArchive, test_archive

# Using TzstArchive class
with TzstArchive("my_archive.tzst", "r") as archive:
    is_valid = archive.test()
    print(f"Archive is {'valid' if is_valid else 'corrupted'}")

# Using convenience function
if test_archive("backup.tzst"):
    print("Archive is valid")
```

## Command Line Interface

tzst provides a comprehensive CLI for archive operations:

### Creating Archives

```bash
# Create an archive with multiple files
tzst a backup.tzst documents/ photos/ config.txt

# Create with high compression
tzst a -l 15 backup.tzst large_files/

# Create without atomic operations (faster, less safe)
tzst a --no-atomic backup.tzst files/
```

### Extracting Archives

```bash
# Extract all files (default: safe extraction)
tzst x backup.tzst

# Extract to specific directory
tzst x backup.tzst -o restore/

# Extract specific files only
tzst x backup.tzst config.txt documents/

# Extract with streaming (memory efficient)
tzst x backup.tzst --streaming
```

### Listing Contents

```bash
# Simple listing
tzst l backup.tzst

# Detailed listing with file info
tzst l backup.tzst -v

# Streaming mode for large archives
tzst l backup.tzst --streaming
```

### Testing Archives

```bash
# Test archive integrity
tzst t backup.tzst

# Test with streaming
tzst t backup.tzst --streaming
```

## Security Considerations

tzst includes built-in security features to protect against malicious archives:

### Extraction Filters

Always use appropriate filters when extracting archives from untrusted sources:

- **`data`** (default): Safest option, only extracts regular files and directories
- **`tar`**: Honors most tar features but still secure
- **`fully_trusted`**: No restrictions (only use with completely trusted archives)

```python
# Safe extraction (recommended)
archive.extract("output/", filter="data")

# Command line
tzst x archive.tzst --filter=data
```

### Best Practices

1. **Always use the default `data` filter** for untrusted archives
2. **Enable atomic operations** (default) for data integrity
3. **Use streaming mode** for very large archives to save memory
4. **Validate archives** with `test()` before processing
5. **Specify output directories** explicitly to avoid overwrites

## Performance Tips

### Memory Efficiency

For large archives, use streaming mode:

```python
# Streaming mode uses less memory
with TzstArchive("large.tzst", "r", streaming=True) as archive:
    archive.extract("output/")
```

### Compression Levels

Choose appropriate compression levels based on your needs:

- **Level 1-3**: Fast compression, larger files
- **Level 3-6**: Balanced (default: 3)
- **Level 7-15**: Better compression, slower
- **Level 16-22**: Maximum compression, much slower

```python
# Fast compression for temporary files
TzstArchive("temp.tzst", "w", compression_level=1)

# Maximum compression for long-term storage
TzstArchive("backup.tzst", "w", compression_level=15)
```

## Error Handling

tzst provides specific exceptions for different error conditions:

```python
from tzst import TzstArchive
from tzst.exceptions import TzstArchiveError, TzstDecompressionError

try:
    with TzstArchive("archive.tzst", "r") as archive:
        archive.extract("output/")
except TzstArchiveError as e:
    print(f"Archive error: {e}")
except TzstDecompressionError as e:
    print(f"Decompression error: {e}")
```

## Next Steps

- Explore the complete {doc}`api/index` documentation
- Check out more {doc}`examples` and use cases
- Read about advanced features in the full documentation
