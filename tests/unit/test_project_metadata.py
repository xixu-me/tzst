"""Project metadata and CI support tests."""

import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_pyproject_declares_python_314_classifier():
    """Package metadata should advertise Python 3.14 support."""
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text("utf-8"))

    classifiers = pyproject["project"]["classifiers"]

    assert "Programming Language :: Python :: 3.14" in classifiers


def test_ci_matrix_includes_python_314():
    """Main test workflow should run on Python 3.14."""
    workflow = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text("utf-8")

    assert 'python-version: ["3.12", "3.13", "3.14"]' in workflow
