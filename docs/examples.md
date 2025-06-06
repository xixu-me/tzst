---
myst:
  html_meta:
    description: "Comprehensive tzst examples - Learn advanced archive creation, extraction, security, and performance optimization"
    keywords: "tzst examples, Python archive examples, tar.zst tutorials, Zstandard compression examples"
    og:title: "tzst Examples and Tutorials"
    og:description: "Comprehensive examples for tzst - archive creation, extraction, security, and performance optimization"
    twitter:title: "tzst Examples and Tutorials"
    twitter:description: "Comprehensive examples for tzst - archive creation, extraction, security, and performance optimization"
---

# Examples

This section provides comprehensive examples of using tzst for various scenarios and use cases.

## Table of Contents

- {ref}`basic-operations`
- {ref}`advanced-archive-creation`
- {ref}`flexible-extraction`
- {ref}`security-and-filtering`
- {ref}`performance-optimization`
- {ref}`error-handling`
- {ref}`real-world-scenarios`
- {ref}`integration-examples`

(basic-operations)=

## Basic Operations

(basic-archive-operations)=

### Creating Your First Archive

```python
from tzst import create_archive

# Simple archive creation
files_to_archive = ["document.pdf", "photos/", "config.json"]
create_archive("my-archive.tzst", files_to_archive)

# With custom compression level
create_archive("high-compression.tzst", files_to_archive, compression_level=9)
```

### Command Line Equivalent

```bash
# Create archive
tzst a my-archive.tzst document.pdf photos/ config.json

# With high compression
tzst a high-compression.tzst document.pdf photos/ config.json --compression-level 9
```

### Basic Extraction

```python
from tzst import extract_archive

# Extract to current directory
extract_archive("my-archive.tzst")

# Extract to specific directory
extract_archive("my-archive.tzst", "extracted/")

# Extract specific files only
extract_archive("my-archive.tzst", "output/", members=["document.pdf", "config.json"])

# Extract with conflict resolution
extract_archive("my-archive.tzst", "output/", conflict_resolution="skip")
```

### Listing Archive Contents

```python
from tzst import list_archive

# Simple listing
contents = list_archive("my-archive.tzst")
for item in contents:
    print(f"{item['name']} ({item['size']} bytes)")

# Detailed listing with timestamps and permissions
contents = list_archive("my-archive.tzst", verbose=True)
for item in contents:
    print(f"{item['name']:30} {item['size']:>10} bytes  {item['mtime']}")
```

## Command Line Usage

> **Note**: Download the [standalone binary](https://github.com/xixu-me/tzst/releases) for the best performance and no Python dependency. Alternatively, use `uvx tzst` for running without installation. See [uv documentation](https://docs.astral.sh/uv/) for details.

### Archive Creation Commands

```bash
# Basic archive creation
tzst a backup.tzst documents/ photos/
# Or with uvx (no installation needed)
uvx tzst a backup.tzst documents/ photos/

# Create with specific compression level
tzst a backup.tzst documents/ photos/ -l 6
uvx tzst a backup.tzst documents/ photos/ -l 6

# Create from multiple sources
tzst a complete-backup.tzst /home/user/documents /home/user/photos /etc/config

# Create with verbose output
tzst a backup.tzst documents/ photos/ -v
```

### Extraction Commands

```bash
# Extract to current directory
tzst x backup.tzst
# Or with uvx
uvx tzst x backup.tzst

# Extract to specific directory
tzst x backup.tzst --output /restore/

# Extract specific files only
tzst x backup.tzst documents/report.pdf photos/vacation.jpg

# Extract with conflict resolution
tzst x backup.tzst --conflict-resolution skip

# Extract flattening directory structure
tzst e backup.tzst --output flat-restore/
```

### Archive Inspection Commands

```bash
# List archive contents
tzst l backup.tzst
# Or with uvx
uvx tzst l backup.tzst

# List with detailed information
tzst l backup.tzst --verbose

# Test archive integrity
tzst t backup.tzst

# Stream large archives efficiently
tzst l huge-archive.tzst --streaming
```

(advanced-archive-creation)=

## Advanced Archive Creation

### Working with the TzstArchive Class

```python
from tzst import TzstArchive
from pathlib import Path

# Create archive with fine-grained control
with TzstArchive("project-backup.tzst", "w", compression_level=6) as archive:
    # Add individual files
    archive.add("README.md")
    archive.add("LICENSE")
    
    # Add directories recursively
    archive.add("src/", recursive=True)
    archive.add("tests/", recursive=True)
    
    # Add with custom archive names
    archive.add("config/production.yaml", arcname="config.yaml")
    archive.add("/tmp/build-info.json", arcname="build-info.json")
```

### Conditional File Addition

```python
import os
from tzst import TzstArchive
from pathlib import Path

def backup_project(project_path, output_archive):
    """Create a project backup excluding certain files."""
    project_path = Path(project_path)
    
    # Define exclusion patterns
    exclude_patterns = {
        "*.pyc", "*.pyo", "__pycache__", 
        ".git", ".svn", "node_modules",
        "*.tmp", "*.log", ".DS_Store"
    }
    
    with TzstArchive(output_archive, "w", compression_level=5) as archive:
        for item in project_path.rglob("*"):
            # Skip excluded patterns
            if any(item.match(pattern) for pattern in exclude_patterns):
                continue
                
            # Skip if it's a directory (will be created automatically)
            if item.is_dir():
                continue
                
            # Add file with relative path
            rel_path = item.relative_to(project_path)
            archive.add(str(item), arcname=str(rel_path))
            print(f"Added: {rel_path}")

# Usage
backup_project("/home/user/myproject", "project-clean.tzst")
```

### Atomic Archive Creation

```python
from tzst import create_archive

# Safe atomic creation (default behavior)
# Creates in temporary file first, then moves to final location
create_archive("important-data.tzst", ["critical/"], use_temp_file=True)

# Direct creation (faster but not atomic)
create_archive("temp-data.tzst", ["temp/"], use_temp_file=False)
```

(flexible-extraction)=

## Flexible Extraction

### Extracting with Different Structures

```python
from tzst import extract_archive, TzstArchive

# Standard extraction (preserves directory structure)
extract_archive("archive.tzst", "output/")

# Flatten all files to single directory
extract_archive("archive.tzst", "flat-output/", flatten=True)

# Extract with streaming for large archives
extract_archive("huge-archive.tzst", "output/", streaming=True)
```

### Selective Extraction

```python
from tzst import TzstArchive

def extract_by_extension(archive_path, output_dir, extensions):
    """Extract only files with specific extensions."""
    with TzstArchive(archive_path, "r") as archive:
        members = archive.getmembers()
        
        # Filter members by extension
        filtered_members = [
            member.name for member in members 
            if any(member.name.endswith(ext) for ext in extensions)
        ]
        
        if filtered_members:
            archive.extractall(output_dir, members=filtered_members)
            print(f"Extracted {len(filtered_members)} files")
        else:
            print("No matching files found")

# Extract only images
extract_by_extension("photos.tzst", "images/", [".jpg", ".png", ".gif"])

# Extract only documents
extract_by_extension("backup.tzst", "docs/", [".pdf", ".docx", ".txt"])
```

### Custom Extraction Logic

```python
from tzst import TzstArchive
import os

def extract_large_files_only(archive_path, output_dir, min_size_mb=10):
    """Extract only files larger than specified size."""
    min_size_bytes = min_size_mb * 1024 * 1024
    
    with TzstArchive(archive_path, "r") as archive:
        large_files = []
        
        for member in archive.getmembers():
            if member.isfile() and member.size > min_size_bytes:
                large_files.append(member.name)
                size_mb = member.size / (1024 * 1024)
                print(f"Will extract: {member.name} ({size_mb:.1f} MB)")
        
        if large_files:
            os.makedirs(output_dir, exist_ok=True)
            for filename in large_files:
                archive.extract(filename, output_dir)
            print(f"Extracted {len(large_files)} large files")

extract_large_files_only("mixed-content.tzst", "large-files/", min_size_mb=5)
```

(security-and-filtering)=

## Security and Filtering

### Safe Extraction Practices

```python
from tzst import extract_archive

# Always use secure filters (default behavior)
extract_archive("untrusted.tzst", "safe-output/", filter="data")

# For trusted archives with special tar features
extract_archive("trusted.tzst", "output/", filter="tar")

# Only for completely trusted archives
extract_archive("internal.tzst", "output/", filter="fully_trusted")
```

### Custom Security Filter

```python
import tarfile
from tzst import TzstArchive

def secure_data_filter(member, path):
    """Custom filter that only allows regular files and directories."""
    # Only allow regular files and directories
    if not (member.isfile() or member.isdir()):
        return None
    
    # Prevent path traversal
    if os.path.isabs(member.name) or ".." in member.name:
        return None
    
    # Limit file size (100MB max)
    if member.isfile() and member.size > 100 * 1024 * 1024:
        return None
    
    return member

# Use custom filter
with TzstArchive("archive.tzst", "r") as archive:
    archive.extractall("secure-output/", filter=secure_data_filter)
```

### Handling File Conflicts

```python
from tzst import extract_archive, ConflictResolution

# Skip existing files
extract_archive("archive.tzst", "output/", 
                conflict_resolution=ConflictResolution.SKIP_ALL)

# Replace all existing files
extract_archive("archive.tzst", "output/", 
                conflict_resolution=ConflictResolution.REPLACE_ALL)

# Auto-rename conflicting files (adds suffix like "_1", "_2", etc.)
extract_archive("archive.tzst", "output/", 
                conflict_resolution=ConflictResolution.AUTO_RENAME_ALL)

# Interactive resolution (command line only)
extract_archive("archive.tzst", "output/", 
                conflict_resolution=ConflictResolution.ASK)
```

### Custom Conflict Resolution

```python
from tzst import extract_archive, ConflictResolution
from pathlib import Path

def custom_conflict_handler(target_path: Path) -> ConflictResolution:
    """Custom logic for handling file conflicts."""
    # Check file age
    if target_path.exists():
        file_age_days = (time.time() - target_path.stat().st_mtime) / (24 * 3600)
        
        if file_age_days > 30:
            print(f"Replacing old file: {target_path}")
            return ConflictResolution.REPLACE
        else:
            print(f"Keeping newer file: {target_path}")
            return ConflictResolution.SKIP
    
    return ConflictResolution.REPLACE

# Use custom callback
extract_archive("archive.tzst", "output/", 
                conflict_resolution=ConflictResolution.ASK,
                interactive_callback=custom_conflict_handler)
```

(performance-optimization)=

## Performance Optimization

### Streaming for Large Archives

```python
from tzst import TzstArchive, list_archive, test_archive

# Memory-efficient operations for large archives
large_archive = "backup-500gb.tzst"

# Test integrity with streaming
is_valid = test_archive(large_archive, streaming=True)

# List contents with streaming
contents = list_archive(large_archive, streaming=True, verbose=True)

# Extract with streaming
with TzstArchive(large_archive, "r", streaming=True) as archive:
    archive.extractall("restore/")
```

### Compression Level Optimization

```python
import time
from tzst import create_archive

def benchmark_compression_levels(files, output_prefix="test"):
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

# Test different compression levels
results = benchmark_compression_levels(["large-directory/"])
```

### Parallel Processing

```python
import concurrent.futures
from tzst import create_archive
from pathlib import Path

def create_archive_batch(file_groups, output_dir="archives/", compression_level=6):
    """Create multiple archives in parallel."""
    Path(output_dir).mkdir(exist_ok=True)
    
    def create_single_archive(args):
        group_name, files = args
        output_path = Path(output_dir) / f"{group_name}.tzst"
        create_archive(output_path, files, compression_level=compression_level)
        return f"Created {output_path}"
    
    # Use ThreadPoolExecutor for I/O-bound operations
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_group = {
            executor.submit(create_single_archive, item): item[0] 
            for item in file_groups.items()
        }
        
        for future in concurrent.futures.as_completed(future_to_group):
            group_name = future_to_group[future]
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"Archive {group_name} failed: {e}")

# Example usage
file_groups = {
    "documents": ["docs/", "papers/"],
    "projects": ["src/", "tests/"],
    "media": ["photos/", "videos/"]
}

create_archive_batch(file_groups)
```

(error-handling)=

## Error Handling

### Comprehensive Error Handling

```python
from tzst import TzstArchive, TzstArchiveError, TzstDecompressionError
import logging

def safe_archive_operation(operation, *args, **kwargs):
    """Wrapper for safe archive operations with logging."""
    try:
        return operation(*args, **kwargs)
    except TzstDecompressionError as e:
        logging.error(f"Decompression error: {e}")
        print("The archive appears to be corrupted or not a valid tzst file.")
        return None
    except TzstArchiveError as e:
        logging.error(f"Archive error: {e}")
        print(f"Archive operation failed: {e}")
        return None
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
        print("Permission denied. Check file/directory permissions.")
        return None
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        print(f"File or directory not found: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")
        return None

# Example usage
def create_backup_safely(files, output_archive):
    def create_operation():
        from tzst import create_archive
        return create_archive(output_archive, files)
    
    result = safe_archive_operation(create_operation)
    if result is not None:
        print(f"Backup created successfully: {output_archive}")
    else:
        print("Backup creation failed!")
```

### Validation and Recovery

```python
from tzst import test_archive, list_archive, TzstArchive
from pathlib import Path

def validate_and_repair_archive(archive_path):
    """Validate archive and attempt basic recovery."""
    archive_path = Path(archive_path)
    
    print(f"Validating {archive_path}...")
    
    # Test basic integrity
    try:
        if test_archive(archive_path):
            print("Archive integrity test passed")
            return True
    except Exception as e:
        print(f"Integrity test failed: {e}")
    
    # Try to list contents
    try:
        contents = list_archive(archive_path)
        print(f"Archive contains {len(contents)} items")
        
        # Try streaming mode if regular mode fails
        contents_streaming = list_archive(archive_path, streaming=True)
        if len(contents_streaming) != len(contents):
            print("Different results between modes - possible corruption")
        
    except Exception as e:
        print(f"Cannot list contents: {e}")
        return False
    
    # Try partial extraction
    try:
        backup_dir = archive_path.parent / f"{archive_path.stem}_recovery"
        backup_dir.mkdir(exist_ok=True)
        
        with TzstArchive(archive_path, "r") as archive:
            extracted_count = 0
            for member in archive.getmembers():
                try:
                    if member.isfile():
                        archive.extract(member.name, backup_dir)
                        extracted_count += 1
                except Exception as e:
                    print(f"Failed to extract {member.name}: {e}")
            
        print(f"Recovered {extracted_count} files to {backup_dir}")
        return True
        
    except Exception as e:
        print(f"Recovery failed: {e}")
        return False

# Example usage
validate_and_repair_archive("potentially-corrupted.tzst")
```

(real-world-scenarios)=

## Real-World Scenarios

### Automated Backup System

```python
#!/usr/bin/env python3
"""
Daily backup script with rotation and validation.
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from tzst import create_archive, test_archive

class BackupManager:
    def __init__(self, source_dirs, backup_dir, retention_days=30):
        self.source_dirs = [Path(d) for d in source_dirs]
        self.backup_dir = Path(backup_dir)
        self.retention_days = retention_days
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self):
        """Create a new backup with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}.tzst"
        backup_path = self.backup_dir / backup_name
        
        print(f"Creating backup: {backup_name}")
        
        # Collect all existing files
        files_to_backup = []
        for source_dir in self.source_dirs:
            if source_dir.exists():
                files_to_backup.append(str(source_dir))
            else:
                print(f"Warning: Source directory not found: {source_dir}")
        
        if not files_to_backup:
            print("No files to backup!")
            return None
        
        try:
            # Create backup with high compression for storage efficiency
            create_archive(backup_path, files_to_backup, compression_level=9)
            
            # Validate the backup
            if test_archive(backup_path):
                file_size = backup_path.stat().st_size / (1024 * 1024)
                print(f"Backup created and validated: {file_size:.1f} MB")
                return backup_path
            else:
                print("Backup validation failed!")
                backup_path.unlink()  # Remove invalid backup
                return None
                
        except Exception as e:
            print(f"Backup failed: {e}")
            return None
    
    def cleanup_old_backups(self):
        """Remove backups older than retention period."""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        
        removed_count = 0
        for backup_file in self.backup_dir.glob("backup_*.tzst"):
            # Extract timestamp from filename
            try:
                timestamp_str = backup_file.stem.split("_", 1)[1]
                file_date = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                
                if file_date < cutoff_date:
                    backup_file.unlink()
                    removed_count += 1
                    print(f"Removed old backup: {backup_file.name}")
                    
            except (ValueError, IndexError):
                print(f"Warning: Could not parse backup date: {backup_file.name}")
        
        print(f"Cleaned up {removed_count} old backups")
    
    def run_backup(self):
        """Run complete backup process."""
        print("Starting backup process...")
        
        backup_path = self.create_backup()
        if backup_path:
            self.cleanup_old_backups()
            print("Backup process completed successfully!")
            return True
        else:
            print("Backup process failed!")
            return False

# Configuration
if __name__ == "__main__":
    # Customize these paths for your setup
    BACKUP_SOURCES = [
        "~/Documents",
        "~/Projects", 
        "~/Pictures",
        "/etc",  # System configs (Linux/macOS)
    ]
    
    BACKUP_DESTINATION = "~/Backups"
    RETENTION_DAYS = 30
    
    # Expand user paths
    sources = [os.path.expanduser(path) for path in BACKUP_SOURCES]
    destination = os.path.expanduser(BACKUP_DESTINATION)
    
    # Run backup
    backup_manager = BackupManager(sources, destination, RETENTION_DAYS)
    success = backup_manager.run_backup()
    
    sys.exit(0 if success else 1)
```

### Log File Archiver

```python
#!/usr/bin/env python3
"""
Archive and compress log files by date.
"""

import re
from datetime import datetime, timedelta
from pathlib import Path
from tzst import create_archive

def archive_logs_by_date(log_dir, archive_dir, days_old=7):
    """Archive log files older than specified days."""
    log_dir = Path(log_dir)
    archive_dir = Path(archive_dir)
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    # Group log files by date
    log_groups = {}
    log_pattern = re.compile(r"(\d{4}-\d{2}-\d{2})")
    
    for log_file in log_dir.glob("*.log"):
        # Try to extract date from filename or modification time
        date_match = log_pattern.search(log_file.name)
        if date_match:
            file_date_str = date_match.group(1)
            try:
                file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
            except ValueError:
                # Fall back to modification time
                file_date = datetime.fromtimestamp(log_file.stat().st_mtime)
        else:
            # Use modification time
            file_date = datetime.fromtimestamp(log_file.stat().st_mtime)
        
        # Skip recent files
        if file_date >= cutoff_date:
            continue
        
        # Group by date
        date_key = file_date.strftime("%Y-%m-%d")
        if date_key not in log_groups:
            log_groups[date_key] = []
        log_groups[date_key].append(log_file)
    
    # Create archives for each date group
    archived_files = []
    for date_key, files in log_groups.items():
        archive_name = f"logs_{date_key}.tzst"
        archive_path = archive_dir / archive_name
        
        # Skip if archive already exists
        if archive_path.exists():
            print(f"Archive already exists: {archive_name}")
            continue
        
        print(f"Archiving {len(files)} log files for {date_key}")
        
        try:
            # Create archive with maximum compression (logs compress well)
            create_archive(archive_path, [str(f) for f in files], compression_level=22)
            
            # Verify archive
            from tzst import test_archive
            if test_archive(archive_path):
                # Remove original files after successful archiving
                for log_file in files:
                    log_file.unlink()
                    archived_files.append(log_file)
                
                file_size = archive_path.stat().st_size / 1024
                print(f"Created {archive_name} ({file_size:.1f} KB)")
            else:
                print(f"Archive validation failed for {archive_name}")
                archive_path.unlink()
        
        except Exception as e:
            print(f"Failed to archive logs for {date_key}: {e}")
    
    print(f"Archived {len(archived_files)} log files")

# Usage
if __name__ == "__main__":
    archive_logs_by_date("/var/log", "/var/archives", days_old=7)
```

### Data Migration Tool

```python
#!/usr/bin/env python3
"""
Migrate data between systems using tzst archives.
"""

import hashlib
from pathlib import Path
from tzst import create_archive, extract_archive, test_archive

class DataMigrator:
    def __init__(self, source_dir, staging_dir):
        self.source_dir = Path(source_dir)
        self.staging_dir = Path(staging_dir)
        self.staging_dir.mkdir(parents=True, exist_ok=True)
    
    def calculate_checksum(self, file_path):
        """Calculate SHA256 checksum of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    def create_migration_package(self, package_name):
        """Create a migration package with checksums."""
        package_path = self.staging_dir / f"{package_name}.tzst"
        checksum_file = self.staging_dir / f"{package_name}.sha256"
        
        print(f"Creating migration package: {package_name}")
        
        # Create the archive
        create_archive(
            package_path, 
            [str(self.source_dir)], 
            compression_level=6  # Balanced for network transfer
        )
        
        # Verify archive
        if not test_archive(package_path):
            raise RuntimeError("Archive validation failed")
        
        # Calculate and save checksum
        checksum = self.calculate_checksum(package_path)
        with open(checksum_file, "w") as f:
            f.write(f"{checksum}  {package_path.name}\n")
        
        package_size = package_path.stat().st_size / (1024 * 1024)        print(f"Package created: {package_size:.1f} MB")
        print(f"Checksum: {checksum}")
        
        return package_path, checksum_file
    
    def verify_and_extract_package(self, package_path, checksum_path, destination):
        """Verify package integrity and extract."""
        package_path = Path(package_path)
        checksum_path = Path(checksum_path)
        destination = Path(destination)
        
        print(f"Verifying package: {package_path.name}")
        
        # Verify checksum
        expected_checksum = checksum_path.read_text().strip().split()[0]
        actual_checksum = self.calculate_checksum(package_path)
        
        if expected_checksum != actual_checksum:
            raise RuntimeError(f"Checksum mismatch! Expected: {expected_checksum}, Got: {actual_checksum}")
        
        print("Checksum verification passed")
        
        # Test archive integrity
        if not test_archive(package_path):
            raise RuntimeError("Archive integrity check failed")
        
        print("Archive integrity verified")
        
        # Extract with conflict resolution
        destination.mkdir(parents=True, exist_ok=True)
        extract_archive(
            package_path, 
            destination,
            conflict_resolution="replace_all"  # Overwrite for migration
        )
        
        print(f"Package extracted to: {destination}")

# Example usage
if __name__ == "__main__":
    # Create migration package
    migrator = DataMigrator("/home/user/important-data", "/tmp/migration")
    package_path, checksum_path = migrator.create_migration_package("data-migration-v1")
    
    # Simulate transfer and extraction on target system
    migrator.verify_and_extract_package(
        package_path, 
        checksum_path, 
        "/home/user/restored-data"
    )
```

(integration-examples)=

## Integration Examples

### Django Management Command

```python
# management/commands/backup_media.py
from django.core.management.base import BaseCommand
from django.conf import settings
from tzst import create_archive
from datetime import datetime
import os

class Command(BaseCommand):
    help = 'Create a backup of media files'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            default='/backups',
            help='Output directory for backup files'
        )
        parser.add_argument(
            '--compression-level',
            type=int,
            default=6,
            help='Compression level (1-22)'
        )
    
    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        output_dir = options['output_dir']
        compression_level = options['compression_level']
        
        if not os.path.exists(media_root):
            self.stdout.write(
                self.style.ERROR(f'Media directory not found: {media_root}')
            )
            return
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'media_backup_{timestamp}.tzst'
        backup_path = os.path.join(output_dir, backup_filename)
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            self.stdout.write(f'Creating media backup: {backup_filename}')
            create_archive(backup_path, [media_root], compression_level=compression_level)
            
            # Verify backup
            from tzst import test_archive
            if test_archive(backup_path):
                file_size = os.path.getsize(backup_path) / (1024 * 1024)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Backup created successfully: {backup_filename} ({file_size:.1f} MB)'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR('Backup validation failed!')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Backup failed: {e}')
            )
```

### Flask Application Integration

```python
from flask import Flask, request, send_file, jsonify
from tzst import create_archive, extract_archive
import tempfile
import os
from pathlib import Path

app = Flask(__name__)

@app.route('/api/backup', methods=['POST'])
def create_backup():
    """API endpoint to create backups."""
    try:
        data = request.get_json()
        paths = data.get('paths', [])
        compression_level = data.get('compression_level', 6)
        
        if not paths:
            return jsonify({'error': 'No paths specified'}), 400
        
        # Create temporary archive
        with tempfile.NamedTemporaryFile(suffix='.tzst', delete=False) as tmp:
            temp_path = tmp.name
        
        create_archive(temp_path, paths, compression_level=compression_level)
        
        # Return archive file
        return send_file(
            temp_path,
            as_attachment=True,
            download_name='backup.tzst',
            mimetype='application/octet-stream'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary file
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)

@app.route('/api/extract', methods=['POST'])
def extract_files():
    """API endpoint to extract archives."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(suffix='.tzst', delete=False) as tmp:
            temp_archive = tmp.name
            file.save(temp_archive)
        
        # Create extraction directory
        extract_dir = tempfile.mkdtemp()
        
        # Extract archive
        extract_archive(temp_archive, extract_dir)
        
        # List extracted files
        extracted_files = []
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), extract_dir)
                extracted_files.append(rel_path)
        
        return jsonify({
            'success': True,
            'extracted_files': extracted_files,
            'extract_path': extract_dir
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary archive
        if 'temp_archive' in locals() and os.path.exists(temp_archive):
            os.unlink(temp_archive)

if __name__ == '__main__':
    app.run(debug=True)
```

### Jupyter Notebook Integration

```python
# Cell 1: Setup
import pandas as pd
from tzst import create_archive, extract_archive, list_archive
from pathlib import Path
import matplotlib.pyplot as plt

# Cell 2: Create dataset archive
def archive_datasets(data_dir="./data", archive_name="datasets.tzst"):
    """Archive all dataset files for sharing."""
    data_path = Path(data_dir)
    
    if not data_path.exists():
        print(f"Creating sample data directory: {data_dir}")
        data_path.mkdir(exist_ok=True)
        
        # Create sample datasets
        sample_data = pd.DataFrame({
            'A': range(100),
            'B': range(100, 200),
            'C': range(200, 300)
        })
        
        sample_data.to_csv(data_path / "sample.csv", index=False)
        sample_data.to_parquet(data_path / "sample.parquet")
    
    # Create archive
    create_archive(archive_name, [str(data_path)], compression_level=9)
    
    # Show archive contents
    contents = list_archive(archive_name, verbose=True)
    df = pd.DataFrame(contents)
    
    print(f"Created archive: {archive_name}")
    return df

# Execute
archive_contents = archive_datasets()
display(archive_contents)

# Cell 3: Analyze archive
def analyze_archive(archive_path="datasets.tzst"):
    """Analyze archive contents and compression."""
    contents = list_archive(archive_path, verbose=True)
    df = pd.DataFrame(contents)
    
    # File type analysis
    df['extension'] = df['name'].str.split('.').str[-1]
    file_types = df.groupby('extension')['size'].agg(['count', 'sum']).reset_index()
    
    # Visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # File count by type
    ax1.bar(file_types['extension'], file_types['count'])
    ax1.set_title('File Count by Type')
    ax1.set_xlabel('File Extension')
    ax1.set_ylabel('Count')
    
    # Size by type
    ax2.bar(file_types['extension'], file_types['sum'] / 1024)  # KB
    ax2.set_title('Total Size by Type (KB)')
    ax2.set_xlabel('File Extension')
    ax2.set_ylabel('Size (KB)')
    
    plt.tight_layout()
    plt.show()
    
    return df, file_types

# Execute
contents_df, file_summary = analyze_archive()
print("File Summary:")
display(file_summary)
```

These examples demonstrate the flexibility and power of tzst for various real-world scenarios. The library's clean API and robust error handling make it suitable for everything from simple backup scripts to complex enterprise applications.
