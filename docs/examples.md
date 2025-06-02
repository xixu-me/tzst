# Examples

This page provides practical examples of using tzst in various scenarios.

## Basic Operations

### Creating Your First Archive

```python
from tzst import TzstArchive

# Create a simple archive
with TzstArchive("my_first_archive.tzst", "w") as archive:
    archive.add("important_file.txt")
    archive.add("documents/", recursive=True)
    
print("Archive created successfully!")
```

### Extracting an Archive

```python
from tzst import TzstArchive

# Extract everything safely
with TzstArchive("my_first_archive.tzst", "r") as archive:
    archive.extract("extracted_files/", filter="data")
    
print("Files extracted to extracted_files/")
```

## Advanced Usage

### High-Compression Backup

```python
from tzst import create_archive
import os

# Create a highly compressed backup
def create_backup(source_dirs, backup_name):
    create_archive(
        archive_path=f"{backup_name}.tzst",
        files=source_dirs,
        compression_level=15,  # High compression
    )
    
    # Check the compression ratio
    original_size = sum(
        os.path.getsize(os.path.join(dirpath, filename))
        for directory in source_dirs
        if os.path.exists(directory)
        for dirpath, dirnames, filenames in os.walk(directory)
        for filename in filenames
    )
    
    compressed_size = os.path.getsize(f"{backup_name}.tzst")
    ratio = (1 - compressed_size / original_size) * 100
    
    print(f"Backup created: {backup_name}.tzst")
    print(f"Compression ratio: {ratio:.1f}%")
    print(f"Original size: {original_size:,} bytes")
    print(f"Compressed size: {compressed_size:,} bytes")

# Usage
create_backup(["documents/", "photos/", "projects/"], "full_backup")
```

### Processing Large Archives with Streaming

```python
from tzst import TzstArchive

def process_large_archive(archive_path, output_dir):
    """Process a large archive efficiently using streaming mode."""
    
    # Use streaming to handle large archives
    with TzstArchive(archive_path, "r", streaming=True) as archive:
        # First, list contents to understand what we're dealing with
        print("Analyzing archive contents...")
        contents = archive.list(verbose=True)
        
        total_files = sum(1 for item in contents if item['is_file'])
        total_size = sum(item['size'] for item in contents if item['is_file'])
        
        print(f"Archive contains {total_files} files ({total_size:,} bytes)")
        
        # Extract only specific file types
        text_files = [item['name'] for item in contents 
                     if item['name'].endswith(('.txt', '.md', '.py'))]
        
        if text_files:
            print(f"Extracting {len(text_files)} text files...")
            archive.extract(output_dir, members=text_files, filter="data")
        
        print("Processing complete!")

# Usage
process_large_archive("large_dataset.tzst", "extracted_text_files/")
```

### Batch Archive Operations

```python
from tzst import test_archive, list_archive
import os
from pathlib import Path

def verify_archive_collection(archive_dir):
    """Verify integrity of all archives in a directory."""
    
    archive_dir = Path(archive_dir)
    archives = list(archive_dir.glob("*.tzst"))
    
    print(f"Found {len(archives)} archives to verify...")
    
    results = []
    for archive_path in archives:
        print(f"Testing {archive_path.name}...")
        
        try:
            # Test integrity
            is_valid = test_archive(str(archive_path))
            
            if is_valid:
                # Get archive info
                contents = list_archive(str(archive_path), verbose=True)
                file_count = sum(1 for item in contents if item['is_file'])
                total_size = sum(item['size'] for item in contents if item['is_file'])
                
                results.append({
                    'name': archive_path.name,
                    'status': 'Valid',
                    'file_count': file_count,
                    'total_size': total_size
                })
            else:
                results.append({
                    'name': archive_path.name,
                    'status': 'Corrupted',
                    'file_count': 0,
                    'total_size': 0
                })
                
        except Exception as e:
            results.append({
                'name': archive_path.name,
                'status': f'Error: {e}',
                'file_count': 0,
                'total_size': 0
            })
    
    # Print summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    for result in results:
        status = result['status']
        if status == 'Valid':
            print(f"✓ {result['name']}: {result['file_count']} files, "
                  f"{result['total_size']:,} bytes")
        else:
            print(f"✗ {result['name']}: {status}")
    
    valid_count = sum(1 for r in results if r['status'] == 'Valid')
    print(f"\nSummary: {valid_count}/{len(results)} archives are valid")

# Usage
verify_archive_collection("backup_archives/")
```

## Security Examples

### Safe Archive Extraction

```python
from tzst import TzstArchive
from tzst.exceptions import TzstArchiveError

def safe_extract(archive_path, output_dir, max_size_mb=100):
    """Safely extract an archive with size limits and security filters."""
    
    try:
        with TzstArchive(archive_path, "r") as archive:
            # First, analyze the archive
            contents = archive.list(verbose=True)
            
            # Check total uncompressed size
            total_size = sum(item['size'] for item in contents if item['is_file'])
            max_size_bytes = max_size_mb * 1024 * 1024
            
            if total_size > max_size_bytes:
                print(f"Warning: Archive is {total_size:,} bytes when uncompressed")
                print(f"This exceeds the limit of {max_size_bytes:,} bytes")
                response = input("Continue anyway? (y/N): ")
                if response.lower() != 'y':
                    return False
            
            # Check for suspicious files
            suspicious_files = []
            for item in contents:
                name = item['name']
                # Check for directory traversal attempts
                if '..' in name or name.startswith('/'):
                    suspicious_files.append(name)
                # Check for executable files
                if name.endswith(('.exe', '.bat', '.sh', '.com')):
                    suspicious_files.append(name)
            
            if suspicious_files:
                print(f"Warning: Found {len(suspicious_files)} suspicious files:")
                for file in suspicious_files[:5]:  # Show first 5
                    print(f"  - {file}")
                if len(suspicious_files) > 5:
                    print(f"  ... and {len(suspicious_files) - 5} more")
                
                response = input("Continue extraction? (y/N): ")
                if response.lower() != 'y':
                    return False
            
            # Extract with the safest filter
            print(f"Extracting {len(contents)} items to {output_dir}")
            archive.extract(output_dir, filter="data")
            print("Extraction completed safely!")
            return True
            
    except TzstArchiveError as e:
        print(f"Archive error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

# Usage
safe_extract("untrusted_archive.tzst", "safe_output/", max_size_mb=50)
```

### Archive Validation Pipeline

```python
from tzst import TzstArchive, test_archive
import hashlib
import json
from pathlib import Path

def create_archive_manifest(archive_path):
    """Create a manifest of archive contents for validation."""
    
    manifest = {
        'archive_path': str(archive_path),
        'files': [],
        'created_at': str(Path(archive_path).stat().st_mtime)
    }
    
    with TzstArchive(archive_path, "r") as archive:
        contents = archive.list(verbose=True)
        
        for item in contents:
            if item['is_file']:
                manifest['files'].append({
                    'name': item['name'],
                    'size': item['size'],
                    'mtime': item['mtime']
                })
    
    # Save manifest
    manifest_path = Path(archive_path).with_suffix('.manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Manifest created: {manifest_path}")
    return manifest

def validate_archive_with_manifest(archive_path):
    """Validate an archive against its manifest."""
    
    manifest_path = Path(archive_path).with_suffix('.manifest.json')
    
    if not manifest_path.exists():
        print("No manifest found, creating new one...")
        create_archive_manifest(archive_path)
        return True
    
    # Load manifest
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    print("Validating archive integrity...")
    if not test_archive(archive_path):
        print("❌ Archive integrity check failed!")
        return False
    
    print("Validating against manifest...")
    with TzstArchive(archive_path, "r") as archive:
        contents = archive.list(verbose=True)
        current_files = {item['name']: item for item in contents if item['is_file']}
    
    manifest_files = {item['name']: item for item in manifest['files']}
    
    # Check for missing files
    missing = set(manifest_files.keys()) - set(current_files.keys())
    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
        return False
    
    # Check for extra files
    extra = set(current_files.keys()) - set(manifest_files.keys())
    if extra:
        print(f"⚠️  Extra files: {', '.join(extra)}")
    
    # Check file sizes
    size_mismatches = []
    for name, manifest_file in manifest_files.items():
        if name in current_files:
            if current_files[name]['size'] != manifest_file['size']:
                size_mismatches.append(name)
    
    if size_mismatches:
        print(f"❌ Size mismatches: {', '.join(size_mismatches)}")
        return False
    
    print("✅ Archive validation passed!")
    return True

# Usage
archive_path = "important_backup.tzst"
if validate_archive_with_manifest(archive_path):
    print("Archive is valid and matches manifest")
else:
    print("Archive validation failed!")
```

## Performance Examples

### Compression Level Comparison

```python
from tzst import create_archive
import time
import os
from pathlib import Path

def compression_benchmark(files, output_prefix="test"):
    """Compare different compression levels for the same files."""
    
    results = []
    levels = [1, 3, 6, 9, 15, 22]  # Representative levels
    
    for level in levels:
        archive_path = f"{output_prefix}_level_{level}.tzst"
        
        print(f"Testing compression level {level}...")
        start_time = time.time()
        
        create_archive(
            archive_path=archive_path,
            files=files,
            compression_level=level
        )
        
        compression_time = time.time() - start_time
        archive_size = os.path.getsize(archive_path)
        
        results.append({
            'level': level,
            'time': compression_time,
            'size': archive_size,
            'path': archive_path
        })
        
        print(f"  Time: {compression_time:.2f}s, Size: {archive_size:,} bytes")
    
    # Print comparison table
    print("\n" + "="*70)
    print("COMPRESSION LEVEL COMPARISON")
    print("="*70)
    print(f"{'Level':<6} {'Time (s)':<10} {'Size (MB)':<12} {'Ratio':<8} {'Speed'}")
    print("-" * 70)
    
    baseline_size = results[0]['size']  # Level 1 as baseline
    baseline_time = results[0]['time']
    
    for result in results:
        size_mb = result['size'] / (1024 * 1024)
        ratio = result['size'] / baseline_size
        speed_factor = baseline_time / result['time']
        
        print(f"{result['level']:<6} {result['time']:<10.2f} {size_mb:<12.1f} "
              f"{ratio:<8.2f} {speed_factor:<.2f}x")
    
    # Clean up test files
    for result in results:
        os.remove(result['path'])
    
    return results

# Usage
benchmark_files = ["large_directory/", "data_files/"]
results = compression_benchmark(benchmark_files, "benchmark")
```

## Error Handling Examples

### Robust Archive Processing

```python
from tzst import TzstArchive, extract_archive
from tzst.exceptions import TzstArchiveError, TzstDecompressionError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def robust_archive_processor(archive_paths, output_base_dir):
    """Process multiple archives with comprehensive error handling."""
    
    results = {
        'success': [],
        'failed': [],
        'skipped': []
    }
    
    for archive_path in archive_paths:
        try:
            logger.info(f"Processing {archive_path}")
            
            # Create output directory for this archive
            archive_name = Path(archive_path).stem
            output_dir = Path(output_base_dir) / archive_name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # First, test the archive
            logger.info(f"Testing integrity of {archive_path}")
            with TzstArchive(archive_path, "r") as archive:
                if not archive.test():
                    raise TzstArchiveError(f"Archive {archive_path} failed integrity test")
                
                # Get archive info
                contents = archive.list(verbose=True)
                file_count = sum(1 for item in contents if item['is_file'])
                total_size = sum(item['size'] for item in contents if item['is_file'])
                
                logger.info(f"Archive contains {file_count} files ({total_size:,} bytes)")
                
                # Extract with error handling
                logger.info(f"Extracting to {output_dir}")
                archive.extract(str(output_dir), filter="data")
                
                results['success'].append({
                    'path': archive_path,
                    'file_count': file_count,
                    'total_size': total_size,
                    'output_dir': str(output_dir)
                })
                
                logger.info(f"Successfully processed {archive_path}")
                
        except TzstArchiveError as e:
            logger.error(f"Archive error processing {archive_path}: {e}")
            results['failed'].append({
                'path': archive_path,
                'error': str(e),
                'error_type': 'TzstArchiveError'
            })
            
        except TzstDecompressionError as e:
            logger.error(f"Decompression error processing {archive_path}: {e}")
            results['failed'].append({
                'path': archive_path,
                'error': str(e),
                'error_type': 'TzstDecompressionError'
            })
            
        except FileNotFoundError:
            logger.warning(f"Archive not found: {archive_path}")
            results['skipped'].append({
                'path': archive_path,
                'reason': 'File not found'
            })
            
        except PermissionError as e:
            logger.error(f"Permission error processing {archive_path}: {e}")
            results['failed'].append({
                'path': archive_path,
                'error': str(e),
                'error_type': 'PermissionError'
            })
            
        except Exception as e:
            logger.error(f"Unexpected error processing {archive_path}: {e}")
            results['failed'].append({
                'path': archive_path,
                'error': str(e),
                'error_type': 'UnexpectedError'
            })
    
    # Print summary
    print("\n" + "="*60)
    print("PROCESSING SUMMARY")
    print("="*60)
    print(f"✅ Successfully processed: {len(results['success'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"⏭️  Skipped: {len(results['skipped'])}")
    
    if results['failed']:
        print("\nFailures:")
        for failure in results['failed']:
            print(f"  - {failure['path']}: {failure['error_type']}")
    
    return results

# Usage
archive_list = [
    "backup1.tzst",
    "backup2.tzst", 
    "backup3.tzst",
    "missing_file.tzst"  # This will be skipped
]

results = robust_archive_processor(archive_list, "extracted_archives/")
```
