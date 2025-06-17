# Security Policy

## Overview

The tzst project takes security seriously and is committed to providing a secure archive management library. This document outlines our security policies, supported versions, vulnerability reporting procedures, and security best practices.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x.x   | ✅ Yes     |
| < 1.0   | ❌ No      |

We provide security updates for the latest major version. Users are strongly encouraged to keep their installations up to date.

## Security Features

### Built-in Security by Default

tzst is designed with security as a primary concern and implements multiple layers of protection:

#### 🔒 Secure Extraction Filters

tzst provides three security filter levels for extraction operations:

- **`data` (default)**: Maximum security level
  - Blocks dangerous files (device files, named pipes, etc.)
  - Prevents absolute path extraction
  - Blocks directory traversal attacks (`../` sequences)
  - Restricts extraction to the specified directory
  - **Recommended for untrusted archives**

- **`tar`**: Standard tar compatibility
  - Blocks absolute paths
  - Prevents directory traversal
  - Allows Unix-specific features (symlinks, permissions)
  - **Use for trusted archives requiring tar features**

- **`fully_trusted`**: No security restrictions
  - Allows all archive features
  - **Only use with completely trusted archives**
  - ⚠️ **Warning**: Can be dangerous with untrusted content

#### ⚡ Atomic Operations

All file creation operations use atomic file operations by default:

- Archives are created in temporary files first, then atomically moved
- Automatic cleanup if the process is interrupted
- Prevents corrupted or incomplete archives
- Cross-platform compatibility
- Use `use_temp_file=False` only when necessary (not recommended)

#### 🛡️ Path Traversal Protection

- Validates all file paths before extraction
- Normalizes paths to prevent directory traversal
- Blocks extraction outside target directory
- Handles edge cases across different operating systems

#### 🔍 Input Validation

- Validates compression levels (1-22)
- Validates archive formats
- Validates file paths and names
- Comprehensive error handling with clear messages

## Best Practices for Users

### 1. Always Use Secure Defaults

```python
from tzst import extract_archive

# ✅ Good: Uses secure 'data' filter by default
extract_archive("untrusted.tzst", "output/")

# ✅ Good: Explicitly specify secure filter
extract_archive("untrusted.tzst", "output/", filter="data")
```

### 2. Choose Appropriate Security Filters

```python
# For untrusted archives (recommended)
extract_archive("untrusted.tzst", "output/", filter="data")

# For trusted archives needing tar features
extract_archive("trusted.tzst", "output/", filter="tar")

# Only for completely trusted archives (use with caution)
extract_archive("internal.tzst", "output/", filter="fully_trusted")
```

### 3. Validate Archive Sources

- Only process archives from trusted sources
- Verify archive integrity before extraction
- Use appropriate security filters based on trust level
- Consider implementing additional validation layers

### 4. Use Safe Extraction Practices

```python
import tempfile
from pathlib import Path
from tzst import extract_archive, test_archive

def safe_extract(archive_path, trust_level="untrusted"):
    """Safely extract an archive with appropriate security measures."""
    
    # Test archive integrity first
    if not test_archive(archive_path):
        raise ValueError("Archive integrity check failed")
    
    # Choose security filter based on trust level
    filters = {
        "untrusted": "data",
        "trusted": "tar", 
        "internal": "fully_trusted"
    }
    
    security_filter = filters.get(trust_level, "data")
    
    # Extract to temporary directory first
    with tempfile.TemporaryDirectory() as temp_dir:
        extract_archive(
            archive_path, 
            temp_dir, 
            filter=security_filter
        )
        # Process extracted files safely
        # Move to final destination if validation passes
```

### 5. Error Handling

```python
from tzst import TzstArchiveError, TzstDecompressionError

try:
    extract_archive("archive.tzst", "output/")
except TzstDecompressionError:
    # Handle corrupted or invalid archives
    print("Archive appears to be corrupted")
except TzstArchiveError as e:
    # Handle general archive errors
    print(f"Archive operation failed: {e}")
except PermissionError:
    # Handle permission issues
    print("Insufficient permissions")
```

## Security Considerations for Different Use Cases

### Processing Untrusted Archives

When processing archives from untrusted sources (internet downloads, user uploads, etc.):

1. **Always use `data` filter** (default behavior)
2. **Extract to isolated directory** with limited permissions
3. **Validate extracted content** before use
4. **Use resource limits** to prevent DoS attacks
5. **Run in sandboxed environment** when possible

### Enterprise/Internal Use

For trusted internal archives:

1. Use `tar` filter for standard compatibility
2. Implement organizational security policies
3. Use secure transport channels
4. Maintain audit logs of archive operations
5. Regular security assessments

### Development/Testing

Even in development:

1. Use secure defaults
2. Don't disable security features without understanding implications
3. Test with malicious archives (in isolated environments)
4. Validate security assumptions

## Reporting Security Vulnerabilities

We take security vulnerabilities seriously and appreciate responsible disclosure.

### How to Report

**DO NOT** report security vulnerabilities through public GitHub issues.

Instead, please report security vulnerabilities via email to:

📧 **[i@xi-xu.me](mailto:i@xi-xu.me)**

### Information to Include

Please include as much of the following information as possible:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** and attack scenarios
4. **Affected versions** (if known)
5. **Suggested fix** (if you have one)
6. **Your contact information** for follow-up

### What to Expect

1. **Acknowledgment**: We'll acknowledge receipt within 48 hours
2. **Initial Assessment**: We'll provide an initial assessment within 5 business days
3. **Communication**: We'll keep you informed throughout the investigation
4. **Resolution**: We'll work to resolve confirmed vulnerabilities promptly
5. **Credit**: We'll credit you in security advisories (unless you prefer anonymity)

### Response Timeline

- **Critical vulnerabilities**: Patch within 7 days
- **High-severity vulnerabilities**: Patch within 14 days  
- **Medium/Low-severity vulnerabilities**: Patch within 30 days

## Security Updates and Advisories

### How We Communicate Security Issues

1. **GitHub Security Advisories**: For confirmed vulnerabilities
2. **Release Notes**: Security fixes are prominently mentioned
3. **PyPI**: Updated packages with security fixes
4. **Documentation**: Security best practices updates

### Staying Informed

To stay informed about security updates:

1. **Watch the repository** for release notifications
2. **Subscribe to GitHub Security Advisories**
3. **Follow our release notes** for security mentions
4. **Use dependency scanners** to identify outdated versions

## Development Security Practices

### Code Review Process

- All changes undergo security-focused code review
- Security-sensitive changes require additional review
- Automated security scanning in CI/CD pipeline
- Regular dependency vulnerability scanning

### Testing

- Comprehensive security test suite
- Fuzzing with malformed archives
- Path traversal attack simulations
- Permission and access control testing

### Dependencies

- Minimal dependency footprint
- Regular dependency updates
- Automated vulnerability scanning
- Pinned versions for reproducible builds

## Known Security Considerations

### Archive Bombs

While tzst includes basic protections, be aware of:

- **Zip bombs**: Archives with extreme compression ratios
- **Memory exhaustion**: Very large expanded archives
- **Resource consumption**: Processing time attacks

**Mitigation**: Use streaming mode for large archives and implement resource limits.

### Symbolic Links

Different security filters handle symbolic links differently:

- `data` filter: Generally restricts symbolic links
- `tar` filter: Preserves symbolic links with basic safety checks
- `fully_trusted` filter: Allows all symbolic link operations

**Recommendation**: Use `data` filter for untrusted content.

### File Permissions

Extracted file permissions depend on:

- Source archive permissions
- Extraction filter settings
- Operating system capabilities
- User privileges

**Recommendation**: Review and validate extracted file permissions.

## Contact

For security-related questions or concerns:

- **Security issues**: [i@xi-xu.me](mailto:i@xi-xu.me) (private)
- **General questions**: [GitHub Discussions](https://github.com/xixu-me/tzst/discussions)
- **Documentation**: [Project Documentation](https://tzst.xi-xu.me)

## Acknowledgments

We thank the security research community for their responsible disclosure of vulnerabilities and continuous efforts to improve software security.

---

**Last Updated**: June 2025  
**Version**: 1.0

For the most current security information, please check our [GitHub repository](https://github.com/xixu-me/tzst) and [official documentation](https://tzst.xi-xu.me).
