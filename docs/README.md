# Documentation

This directory contains the Sphinx documentation for the tzst library.

## Setup

1. Install documentation dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Install the tzst package in development mode (required for autodoc):

   ```bash
   pip install -e ..
   ```

## Building Documentation

### Local Development

Build the documentation locally:

```bash
# On Unix/macOS
make html

# On Windows
make.bat html
```

The built documentation will be in `_build/html/`. Open `_build/html/index.html` in your browser.

### Live Reload (Recommended for Development)

For automatic rebuilding when files change:

```bash
# Install sphinx-autobuild if not already installed
pip install sphinx-autobuild

# Start live reload server
make livehtml
# or
sphinx-autobuild . _build/html
```

This will start a local server (usually at <http://localhost:8000>) that automatically rebuilds and refreshes when you save changes.

### Other Build Targets

```bash
# Check documentation coverage
make coverage

# Check for broken links
make linkcheck

# Build PDF (requires LaTeX)
make latexpdf

# Clean build directory
make clean
```

## Documentation Structure

- `index.md` - Main documentation homepage
- `quickstart.md` - Quick start guide for new users
- `examples.md` - Practical examples and use cases
- `api/` - API reference documentation
  - `index.md` - API overview
  - `core.md` - Core functionality documentation
  - `cli.md` - CLI documentation
  - `exceptions.md` - Exception classes documentation

## Writing Documentation

### Markdown vs reStructuredText

This documentation uses MyST parser, which allows you to write in Markdown with some reStructuredText features. You can use either `.md` or `.rst` files.

### Adding New Pages

1. Create a new `.md` file in the appropriate directory
2. Add it to the relevant `toctree` directive in the parent index file
3. Use proper Markdown headers and cross-references

### API Documentation

API documentation is automatically generated from docstrings using Sphinx autodoc. To document a new module:

1. Add the module to the appropriate API file (e.g., `api/core.md`)
2. Use autodoc directives like `automodule`, `autoclass`, `autofunction`

### Code Examples

Use fenced code blocks with language specification:

````markdown
```python
from tzst import TzstArchive

with TzstArchive("example.tzst", "w") as archive:
    archive.add("file.txt")
```
````

### Cross-References

Link to other documentation pages:

```markdown
See the {doc}`quickstart` guide for more information.
```

Link to API documentation:

```markdown
Use the {class}`tzst.TzstArchive` class.
```

## Automated Deployment

Documentation is automatically built and deployed to GitHub Pages when changes are pushed to the main branch. The workflow is defined in `.github/workflows/publish_docs.yml`.

### Local Testing of Deployment

To test the deployment process locally:

1. Build the documentation: `make html`
2. Serve the built files: `python -m http.server 8000 -d _build/html`
3. Visit <http://localhost:8000>

## Troubleshooting

### Import Errors

If you get import errors when building documentation:

1. Make sure the tzst package is installed: `pip install -e ..`
2. Check that all dependencies are installed: `pip install -r requirements.txt`
3. Verify your Python path includes the src directory

### Theme Issues

If the RTD theme isn't working:

1. Install the theme: `pip install sphinx-rtd-theme`
2. Check that it's listed in `requirements.txt`
3. Verify the theme configuration in `conf.py`

### Build Warnings

Address all Sphinx warnings to ensure high-quality documentation:

- Fix broken cross-references
- Add missing docstrings
- Resolve autodoc import issues
- Fix malformed markup

## Contributing

When contributing to documentation:

1. Follow the existing style and structure
2. Test your changes locally before submitting
3. Add examples for new features
4. Update the changelog if appropriate
5. Ensure all links work correctly
