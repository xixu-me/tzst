---
myst:
  html_meta:
    description: "tzst Performance Guide - Compression level optimization, performance tips, and comparison with other archive tools"
    keywords: "tzst performance, compression benchmarks, tar gzip comparison, archive performance optimization"
    og:title: "tzst Performance Guide"
    og:description: "Performance optimization tips and comparison with other archive tools for tzst"
    twitter:title: "tzst Performance Guide"
    twitter:description: "Performance optimization tips and comparison with other archive tools for tzst"
    og:type: "website"
    og:image: "https://tzst.xi-xu.me/_static/tzst-square-logo.png"
    og:url: "https://tzst.xi-xu.me/"
    twitter:card: "summary_large_image"
    twitter:image: "https://tzst.xi-xu.me/_static/tzst-square-logo.png"
---

# Performance Guide

This guide covers performance optimization techniques and provides detailed comparisons with other archive tools.

## Performance Tips

### 1. Compression Levels

Choose the right compression level for your use case:

- **Level 1-3**: Fast compression, larger files (good for temporary archives or real-time processing)
- **Level 3** (default): Optimal balance for most use cases
- **Level 6-9**: Higher compression, moderate speed (good for regular backups)
- **Level 15-22**: Maximum compression, slower (for long-term storage or bandwidth-limited scenarios)

```python
from tzst import create_archive

# For temporary files or frequent operations
create_archive("temp.tzst", files, compression_level=1)

# Balanced default (recommended)
create_archive("backup.tzst", files, compression_level=3)

# Long-term storage
create_archive("archive.tzst", files, compression_level=9)

# Maximum compression for critical space savings
create_archive("minimal.tzst", files, compression_level=22)
```

### 2. Streaming

Use streaming mode for archives larger than 100MB:

```python
from tzst import extract_archive, list_archive, test_archive

# Memory-efficient operations for large archives
extract_archive("large-backup.tzst", "restore/", streaming=True)
contents = list_archive("large-backup.tzst", streaming=True)
is_valid = test_archive("large-backup.tzst", streaming=True)
```

**Streaming Benefits:**

- Significantly reduced memory usage
- Better performance for large archives
- Handles archives that don't fit in memory

### 3. Batch Operations

Add multiple files in a single session when possible:

```python
from tzst import TzstArchive

# Efficient: Single archive session
with TzstArchive("backup.tzst", "w") as archive:
    archive.add("file1.txt")
    archive.add("file2.txt")
    archive.add("directory/", recursive=True)

# Less efficient: Multiple separate operations
create_archive("backup1.tzst", ["file1.txt"])
create_archive("backup2.tzst", ["file2.txt"])
```

### 4. File Type Considerations

- Already compressed files (`.jpg`, `.png`, `.mp4`, `.pdf`) won't compress much further
- Text files, source code, and logs compress very well
- Consider compression level based on your data types

## Comparison with Other Tools

### vs tar + gzip

**tzst Advantages:**

- **Better compression ratios**: 10-40% smaller archives
- **Faster decompression**: 2-3x faster extraction
- **Modern algorithm**: Better handling of various file types
- **Streaming support**: Better memory efficiency

**When to use tar + gzip:**

- Legacy system compatibility requirements
- Very old systems without zstd support

### vs tar + xz

**tzst Advantages:**

- **Significantly faster compression**: 3-10x faster creation
- **Faster decompression**: 2-4x faster extraction
- **Better speed/compression trade-off**: Similar compression with much better speed
- **More compression levels**: Fine-grained control (22 levels vs 9)

**When to use tar + xz:**

- Maximum compression is critical and time is not a factor
- Systems that don't support zstd

### vs zip

**tzst Advantages:**

- **Better compression**: 15-30% smaller archives
- **Preserves Unix permissions and metadata**: Full POSIX compatibility
- **Better streaming support**: Memory-efficient for large archives
- **Better directory handling**: Preserves directory structure and timestamps

**When to use zip:**

- Cross-platform compatibility with very old systems
- Individual file access without full extraction is required
- Windows-centric environments with no command-line tools

## Benchmarking Examples

### Compression Level Benchmark

```python
import time
from pathlib import Path
from tzst import create_archive

def benchmark_compression_levels(files, output_prefix="benchmark"):
    """Compare different compression levels."""
    levels_to_test = [1, 3, 6, 9, 15, 22]
    
    results = []
    for level in levels_to_test:
        output_file = f"{output_prefix}_level_{level}.tzst"
        
        # Measure compression time
        start_time = time.time()
        create_archive(output_file, files, compression_level=level)
        compress_time = time.time() - start_time
        
        # Get file size
        file_size = Path(output_file).stat().st_size
        
        results.append({
            'level': level,
            'time': compress_time,
            'size': file_size,
            'size_mb': file_size / (1024 * 1024)
        })
        
        print(f"Level {level}: {compress_time:.2f}s, {file_size/1024/1024:.1f} MB")
    
    return results

# Example usage
files = ["documents/", "projects/"]
results = benchmark_compression_levels(files)
```

### Memory Usage Comparison

```python
import psutil
import os
from tzst import extract_archive

def monitor_memory_usage(func, *args, **kwargs):
    """Monitor memory usage during function execution."""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    func(*args, **kwargs)
    
    peak_memory = process.memory_info().rss / 1024 / 1024  # MB
    return peak_memory - initial_memory

# Compare streaming vs non-streaming extraction
large_archive = "large-dataset.tzst"

memory_normal = monitor_memory_usage(extract_archive, large_archive, "output1/")
memory_streaming = monitor_memory_usage(extract_archive, large_archive, "output2/", streaming=True)

print(f"Normal extraction: {memory_normal:.1f} MB")
print(f"Streaming extraction: {memory_streaming:.1f} MB")
print(f"Memory savings: {memory_normal - memory_streaming:.1f} MB")
```

## Best Practices

### For Development

```python
# Fast compression for frequent builds
create_archive("build-artifacts.tzst", ["build/"], compression_level=1)
```

### For Backups

```python
# Balanced compression for regular backups
create_archive("daily-backup.tzst", ["data/"], compression_level=6)
```

### For Distribution

```python
# Higher compression for software distribution
create_archive("software-package.tzst", ["app/"], compression_level=9)
```

### For Archival Storage

```python
# Maximum compression for long-term storage
create_archive("archive-2024.tzst", ["historical-data/"], compression_level=22)
```

## Hardware Considerations

### CPU Usage

- Higher compression levels use more CPU but for shorter time periods
- Modern multi-core systems handle zstd compression very efficiently
- Consider system load when choosing compression levels

### Memory Usage

- Streaming mode: ~16-32 MB memory usage regardless of archive size
- Normal mode: Memory usage proportional to archive size
- Use streaming for archives >100 MB or on memory-constrained systems

### Storage

- SSDs benefit from higher compression (less I/O)
- HDDs may prefer lower compression levels (CPU vs I/O trade-off)
- Network storage benefits from higher compression (bandwidth savings)

## Integration with Build Systems

### Makefile Example

```makefile
# Fast compression for development
build-dev: 
 tzst a build-dev.tzst build/ -l 1

# Production compression
build-prod:
 tzst a build-prod.tzst build/ -l 9

# CI/CD artifacts
artifacts:
 tzst a artifacts.tzst dist/ logs/ -l 6
```

### GitHub Actions Example

```yaml
- name: Create release archive
  run: |
    tzst a release-${{ github.ref_name }}.tzst \
      build/ docs/ \
      --compression-level 9
```

This performance guide helps you choose the right settings for your specific use case and understand how tzst compares to alternative archive tools.
