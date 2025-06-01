# Contributing to tzst

Thank you for your interest in contributing to tzst! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)
- [Getting Help](#getting-help)

## Code of Conduct

This project follows the principles of respectful collaboration. Please be kind, constructive, and professional in all interactions.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Git
- Basic knowledge of tar archives and compression

### Development Setup

1. **Fork and clone the repository:**

   ```bash
   git clone https://github.com/your-username/tzst.git
   cd tzst
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix/macOS
   source venv/bin/activate
   ```

3. **Install the package in development mode:**

   ```bash
   pip install -e .[dev]
   ```

4. **Verify the installation:**

   ```bash
   python -m pytest tests/
   ```

## Project Structure

```
tzst/
├── src/tzst/           # Main package source code
│   ├── __init__.py     # Package initialization and exports
│   ├── __main__.py     # CLI entry point
│   ├── cli.py          # Command-line interface
│   ├── core.py         # Core archive functionality
│   └── exceptions.py   # Custom exceptions
├── tests/              # Test suite
│   ├── conftest.py     # Pytest configuration and fixtures
│   ├── test_core.py    # Core functionality tests
│   ├── test_cli.py     # CLI tests
│   └── test_*.py       # Additional test modules
├── .github/            # GitHub workflows and templates
├── pyproject.toml      # Project configuration
├── README.md           # Project documentation
├── LICENSE             # BSD 3-Clause License
└── CONTRIBUTING.md     # This file
```

## Making Changes

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues in existing functionality
- **Features**: Add new capabilities to the library
- **Documentation**: Improve or add documentation
- **Tests**: Add or improve test coverage
- **Performance**: Optimize existing code
- **Security**: Address security vulnerabilities

### Branch Naming

Use descriptive branch names:

- `feature/add-streaming-mode`
- `fix/handle-corrupted-archives`
- `docs/improve-api-documentation`
- `test/add-compression-tests`

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or modifying tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Build process or auxiliary tool changes

Examples:

```
feat(core): add streaming compression support

fix(cli): handle invalid archive paths gracefully

docs(readme): update installation instructions
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov

# Run specific test file
python -m pytest tests/test_core.py

# Run with verbose output
python -m pytest -v

# Run integration tests only
python -m pytest -m integration
```

### Test Structure

- Unit tests: Test individual functions and methods
- Integration tests: Test component interactions
- CLI tests: Test command-line interface
- Platform-specific tests: Test OS-specific functionality

### Writing Tests

1. **Use descriptive test names:**

   ```python
   def test_create_archive_with_compression_level_9():
   ```

2. **Use fixtures for common test data:**

   ```python
   def test_extract_archive(sample_archive_path, temp_dir):
   ```

3. **Test edge cases:**
   - Empty files
   - Large files
   - Invalid inputs
   - Corrupted archives

4. **Add markers for test categorization:**

   ```python
   @pytest.mark.integration
   def test_full_archive_workflow():
   ```

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

### Configuration

Settings are defined in `pyproject.toml`:

- Line length: 88 characters
- Target Python version: 3.12+
- Import sorting with isort
- Quote style: double quotes

### Running Code Style Tools

```bash
# Check code style
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Format code
ruff format .

# Check formatting without making changes
ruff format --check .
```

### Code Style Guidelines

1. **Follow PEP 8** with project-specific modifications
2. **Use type hints** for all public APIs
3. **Write docstrings** for classes and public methods
4. **Keep functions focused** and reasonably sized
5. **Use meaningful variable names**
6. **Add comments** for complex logic

### Documentation Strings

Use Google-style docstrings:

```python
def create_archive(
    archive_path: str | Path,
    files: Sequence[str | Path],
    compression_level: int = 3,
) -> None:
    """Create a new tzst archive containing the specified files.
    
    Args:
        archive_path: Path where the archive will be created.
        files: Sequence of file/directory paths to include.
        compression_level: Zstandard compression level (1-22).
        
    Raises:
        TzstArchiveError: If archive creation fails.
        FileNotFoundError: If input files don't exist.
    """
```

## Submitting Changes

### Pull Request Process

1. **Create a feature branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Add tests** for new functionality

4. **Update documentation** if needed

5. **Run the test suite:**

   ```bash
   python -m pytest
   ruff check .
   ruff format --check .
   ```

6. **Commit your changes:**

   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

7. **Push to your fork:**

   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a pull request** using the provided template

### Pull Request Guidelines

- **Fill out the PR template** completely
- **Link related issues** using keywords (fixes #123)
- **Keep PRs focused** - one feature/fix per PR
- **Update CHANGELOG.md** for user-facing changes
- **Ensure all CI checks pass**
- **Respond to review feedback** promptly

### Review Process

1. Automated checks must pass (CI/CD, code style)
2. Code review by maintainers
3. Address any feedback or requested changes
4. Final approval and merge by maintainers

## Release Process

Releases are handled by maintainers:

1. Update version in `src/tzst/__init__.py`
2. Update `CHANGELOG.md`
3. Create a release tag
4. Automated CI/CD publishes to PyPI

## Getting Help

### Resources

- **Issues**: [GitHub Issues](https://github.com/xixu-me/tzst/issues)
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the README and code comments

### Reporting Issues

When reporting bugs:

1. **Use the bug report template**
2. **Provide a minimal reproduction case**
3. **Include system information** (OS, Python version)
4. **Attach relevant files** if possible (archives, logs)

### Suggesting Features

When suggesting features:

1. **Use the feature request template**
2. **Explain the use case** and motivation
3. **Consider backwards compatibility**
4. **Provide implementation ideas** if you have them

## Development Tips

### Performance Considerations

- Use streaming for large files
- Consider memory usage patterns
- Profile code for bottlenecks
- Test with various file sizes

### Security Considerations

- Validate all user inputs
- Use secure defaults (e.g., 'data' filter)
- Handle malicious archives safely
- Be cautious with file paths

### Compatibility

- Support Python 3.12+
- Test on multiple platforms (Windows, macOS, Linux)
- Consider different filesystem behaviors
- Maintain backwards compatibility when possible

## Recognition

Contributors are recognized in several ways:

- Listed in release notes for significant contributions
- Mentioned in README acknowledgments
- GitHub contributor statistics

Thank you for contributing to tzst! Your efforts help make this library better for everyone.
