"""Test fixtures for shitlint tests."""

import tempfile
from pathlib import Path
import pytest
import ast


@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w+') as f:
        yield f


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def default_thresholds():
    """Default thresholds for testing rules."""
    return {
        "file_lines": {"gentle": 200, "moderate": 300, "brutal": 500},
        "imports": {"moderate": 10, "brutal": 15},
        "complexity": {"moderate": 8, "brutal": 12},
        "function_lines": {"moderate": 30, "brutal": 50},
        "parameters": {"moderate": 4, "brutal": 6},
        "name_length": 25,
        "enable_loop_var_check": True
    }


@pytest.fixture
def parse_code():
    """Helper to parse Python code into AST."""
    def _parse(code):
        return ast.parse(code)
    return _parse