"""Tests for core ShitLint functionality."""

import os
import tempfile
from pathlib import Path
import pytest
from shitlint.core import (
    analyze_code, 
    get_analysis_context, 
    _get_python_files,
    _get_doc_files,
    _load_gitignore_spec,
    _detect_naming_violations
)


def test_analyze_code_file():
    """Test analyzing a single file."""
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w+') as f:
        f.write('x = 123  # Magic number\n')
        f.flush()
        
        results = analyze_code(Path(f.name))
        
        assert len(results) > 0
        assert any(r.rule == "magic_number" for r in results)


def test_analyze_code_directory():
    """Test analyzing a directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a Python file with violations
        file_path = Path(tmpdir) / "test.py"
        with open(file_path, 'w') as f:
            f.write('def process_data(data):\n    return data\n')
        
        results = analyze_code(Path(tmpdir))
        
        assert len(results) > 0
        assert any(r.rule == "ceremony_parameter" for r in results)


def test_get_python_files():
    """Test getting Python files with gitignore patterns."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create Python files
        file1 = Path(tmpdir) / "file1.py"
        file2 = Path(tmpdir) / "file2.py"
        ignored = Path(tmpdir) / "ignored.py"
        
        for file in [file1, file2, ignored]:
            with open(file, 'w') as f:
                f.write('# Test\n')
        
        # Create .gitignore
        gitignore = Path(tmpdir) / ".gitignore"
        with open(gitignore, 'w') as f:
            f.write('ignored.py\n')
        
        # Get Python files
        files = _get_python_files(Path(tmpdir))
        
        # Should find 2 files, not the ignored one
        assert len(files) == 2
        assert any(f.name == "file1.py" for f in files)
        assert any(f.name == "file2.py" for f in files)
        assert not any(f.name == "ignored.py" for f in files)


def test_get_doc_files():
    """Test getting documentation files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create doc files
        readme = Path(tmpdir) / "README.md"
        docs = Path(tmpdir) / "docs.rst"
        notes = Path(tmpdir) / "notes.txt"
        code = Path(tmpdir) / "code.py"
        
        for file in [readme, docs, notes, code]:
            with open(file, 'w') as f:
                f.write('# Test\n')
        
        # Get doc files
        files = _get_doc_files(Path(tmpdir))
        
        # Should find 3 doc files, not the Python file
        assert len(files) == 3
        assert any(f.name == "README.md" for f in files)
        assert any(f.name == "docs.rst" for f in files)
        assert any(f.name == "notes.txt" for f in files)
        assert not any(f.name == "code.py" for f in files)


def test_load_gitignore_spec():
    """Test loading gitignore patterns."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create .gitignore
        gitignore = Path(tmpdir) / ".gitignore"
        with open(gitignore, 'w') as f:
            f.write('*.log\n')
            f.write('temp/\n')
            f.write('# Comment\n')
            f.write('secret.txt\n')
        
        # Load gitignore spec
        spec = _load_gitignore_spec(Path(tmpdir))
        
        # Test matching
        assert spec.match_file("file.log")
        assert spec.match_file("temp/file.txt")
        assert spec.match_file("secret.txt")
        assert not spec.match_file("file.py")
        assert not spec.match_file("README.md")


def test_detect_naming_violations():
    """Test detection of naming violations in file structure."""
    # Test duplicate names
    files = [Path("file1.py"), Path("file2.py"), Path("file1.py")]
    violations = _detect_naming_violations(files)
    assert "Duplicate file name pattern: file1" in violations
    
    # Test vague names
    files = [Path("utils.py"), Path("helpers.py")]
    violations = _detect_naming_violations(files)
    assert "Vague file name: utils.py" in violations
    assert "Vague file name: helpers.py" in violations
    
    # Test inconsistent naming
    files = [Path("snake_case.py"), Path("camelCase.py")]
    violations = _detect_naming_violations(files)
    assert "Inconsistent naming convention: mix of snake_case and camelCase" in violations