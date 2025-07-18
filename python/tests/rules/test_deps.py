"""Tests for dependency rule violations."""

import json
import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch, mock_open
from shitlint.rules.deps import detect_dependency_violations, _analyze_deps
from shitlint.rules.base import Violation


def test_analyze_deps_package_json_bloat():
    """Test detection of bloated package.json."""
    # Create a package.json with too many dependencies
    deps = {f"dep{i}": "^1.0.0" for i in range(30)}
    package_json = {
        "dependencies": deps
    }
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / 'package.json'
        path.write_text(json.dumps(package_json))
        violations = _analyze_deps(path)
        
        # Should detect dependency bloat
        assert any(v.rule == "deps_bloat" for v in violations)
        assert any("Package bloat" in v.message for v in violations)


def test_analyze_deps_requirements_txt_bloat():
    """Test detection of bloated requirements.txt."""
    # Create a requirements.txt with too many dependencies
    requirements = "\n".join([f"package{i}==1.0.0" for i in range(30)])
    
    with tempfile.NamedTemporaryFile(suffix='.txt') as f:
        path = Path(f.name)
        with patch('pathlib.Path.read_text', return_value=requirements):
            with patch('pathlib.Path.name', 'requirements.txt'):
                violations = _analyze_deps(path)
                
                # Should detect dependency bloat
                assert any(v.rule == "deps_bloat" for v in violations)
                assert any("Package bloat" in v.message for v in violations)


def test_analyze_deps_pyproject_toml_bloat():
    """Test detection of bloated pyproject.toml."""
    # Create a pyproject.toml with too many dependencies
    pyproject = """
[tool.poetry.dependencies]
python = "^3.8"
"""
    pyproject += "\n".join([f'package{i} = "^1.0.0"' for i in range(30)])
    
    with tempfile.NamedTemporaryFile(suffix='.toml') as f:
        path = Path(f.name)
        with patch('pathlib.Path.read_text', return_value=pyproject):
            with patch('pathlib.Path.name', 'pyproject.toml'):
                violations = _analyze_deps(path)
                
                # Should detect dependency bloat
                assert any(v.rule == "deps_bloat" for v in violations)
                assert any("Package bloat" in v.message for v in violations)


def test_analyze_deps_left_pad_npm():
    """Test detection of left-pad syndrome in npm."""
    package_json = {
        "dependencies": {
            "react": "^17.0.2",
            "left-pad": "^1.3.0",
            "lodash": "^4.17.21"
        }
    }
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / 'package.json'
        path.write_text(json.dumps(package_json))
        violations = _analyze_deps(path)
        
        # Should detect left-pad syndrome
        assert any(v.rule == "deps_leftpad" for v in violations)
        assert any("left-pad" in v.message for v in violations)


def test_analyze_deps_left_pad_pip():
    """Test detection of left-pad syndrome in pip."""
    requirements = """
requests==2.26.0
six==1.16.0
flask==2.0.1
"""
    
    with tempfile.NamedTemporaryFile(suffix='.txt') as f:
        path = Path(f.name)
        with patch('pathlib.Path.read_text', return_value=requirements):
            with patch('pathlib.Path.name', 'requirements.txt'):
                violations = _analyze_deps(path)
                
                # Should detect left-pad syndrome
                assert any(v.rule == "deps_leftpad" for v in violations)
                assert any("six" in v.message for v in violations)


@patch('pathlib.Path.exists')
@patch('pathlib.Path.parent')
def test_detect_dependency_violations_no_deps(mock_parent, mock_exists):
    """Test handling when no dependency files exist."""
    # Mock no dependency files
    mock_exists.return_value = False
    mock_parent.return_value = Path("/")
    
    file_path = Path("test.py")
    content = "# Test file"
    thresholds = {}
    
    violations = detect_dependency_violations(file_path, content, None, thresholds)
    
    # Should not detect any violations
    assert len(violations) == 0