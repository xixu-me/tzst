# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add the source directory to the Python path
sys.path.insert(0, os.path.abspath("../src"))

# Import version from the package
from tzst import __version__

# -- Project information -----------------------------------------------------
project = "tzst"
copyright = "2025, Xi Xu"
author = "Xi Xu"
release = __version__
version = __version__

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_title = f"tzst {version} Documentation"
html_short_title = "tzst"

# HTML meta tags
html_meta = {
    "description": "tzst - A Python library for creating and extracting tar.zst archives with high performance and comprehensive features",
    "keywords": "tzst, tar, zstandard, compression, archive, python, extraction, backup",
    "author": "Xi Xu",
    "robots": "index, follow",
    "language": "en",
    "viewport": "width=device-width, initial-scale=1.0",
    "theme-color": "#2980B9",
    "msapplication-TileColor": "#2980B9",
    "og:title": "tzst Documentation",
    "og:description": "tzst - A Python library for creating and extracting tar.zst archives with high performance and comprehensive features",
    "og:type": "website",
    "og:url": "https://tzst.xi-xu.me/",
    "og:image": "https://tzst.xi-xu.me/_static/tzst-logo.png",
    "twitter:card": "summary_large_image",
    "twitter:title": "tzst Documentation",
    "twitter:description": "tzst - A Python library for creating and extracting tar.zst archives with high performance and comprehensive features",
    "twitter:image": "https://tzst.xi-xu.me/_static/tzst-logo.png",
}

# Theme options
html_theme_options = {
    "canonical_url": "https://tzst.xi-xu.me/",
    "logo_only": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "style_nav_header_background": "#2980B9",
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": False,
    "titles_only": False,
}

# Additional HTML options
html_favicon = "_static/favicon.ico"  # Will show warning until favicon is created
html_logo = "_static/tzst-logo.png"  # Will show warning until logo is created
html_use_opensearch = "https://tzst.xi-xu.me/"

# HTML context for custom template variables
html_context = {
    "display_github": True,
    "github_user": "xixu-me",
    "github_repo": "tzst",
    "github_version": "main",
    "conf_py_path": "/docs/",
}

# -- Extension configuration -------------------------------------------------
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": "__init__",
    "exclude-members": "__weakref__",
}

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "zstandard": ("https://python-zstandard.readthedocs.io/en/latest/", None),
}

# Autosummary
autosummary_generate = True

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_admonition",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
