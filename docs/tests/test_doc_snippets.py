"""Test all documentation code snippets.

This module discovers and tests all Python snippet files in the documentation.
Each snippet file should be executable and should not raise any errors.
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

# Path to the snippets directory
SNIPPETS_DIR = Path(__file__).parent.parent / "source" / "_snippets"


def get_snippet_files():
    """Collect all Python files in the snippets directory.

    Returns
    -------
    list[Path]
        List of paths to Python snippet files, excluding __init__.py and conftest.py.
    """
    snippet_files = []
    for path in SNIPPETS_DIR.rglob("*.py"):
        # Skip __init__.py and conftest.py files
        if path.name in ("__init__.py", "conftest.py"):
            continue
        snippet_files.append(path)
    return sorted(snippet_files)


def _snippet_id(path):
    """Generate a readable test ID for a snippet file."""
    return str(path.relative_to(SNIPPETS_DIR))


@pytest.mark.parametrize("snippet_file", get_snippet_files(), ids=_snippet_id)
def test_snippet_executes(snippet_file):
    """Test that each snippet file executes without errors.

    This runs each snippet as a subprocess to ensure isolation between tests
    and to catch any import-time errors.

    Parameters
    ----------
    snippet_file : Path
        Path to the snippet file to test.
    """
    result = subprocess.run(
        [sys.executable, str(snippet_file)],
        capture_output=True,
        text=True,
        timeout=120,  # 2 minute timeout for optimization examples
        cwd=str(SNIPPETS_DIR),
    )

    # Provide helpful error message on failure
    if result.returncode != 0:
        error_msg = f"Snippet {snippet_file.name} failed to execute.\n"
        error_msg += f"stdout:\n{result.stdout}\n"
        error_msg += f"stderr:\n{result.stderr}"
        pytest.fail(error_msg)


@pytest.mark.parametrize("snippet_file", get_snippet_files(), ids=_snippet_id)
def test_snippet_imports(snippet_file):
    """Test that each snippet file can be imported as a module.

    This catches syntax errors and import-time errors in a more controlled way.

    Parameters
    ----------
    snippet_file : Path
        Path to the snippet file to test.
    """
    spec = importlib.util.spec_from_file_location(
        f"snippet_{snippet_file.stem}", snippet_file
    )
    if spec is None or spec.loader is None:
        pytest.fail(f"Could not load spec for {snippet_file}")

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        pytest.fail(f"Snippet {snippet_file.name} failed to import: {e}")
