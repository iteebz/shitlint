"""Tests for documentation rule violations."""

import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch, mock_open
from shitlint.rules.docs import detect_documentation_violations, _analyze_docs
from shitlint.rules.base import Violation


def test_analyze_docs_lazy_placeholders():
    """Test detection of lazy documentation placeholders."""
    content = """
# Project Title

## Introduction
TODO: write documentation for this section

## Features
Coming soon

## Installation
Under construction

## Usage
Work in progress
"""
    
    with tempfile.NamedTemporaryFile(suffix='.md') as f:
        path = Path(f.name)
        with patch('pathlib.Path.read_text', return_value=content):
            violations = _analyze_docs(path)
            
            # Should detect lazy placeholders
            assert len(violations) >= 4
            assert any("TODO: write docs" in v.message for v in violations)
            assert any("Coming soon" in v.message for v in violations)
            assert any("Under construction" in v.message for v in violations)
            assert any("Work in progress" in v.message for v in violations)


def test_analyze_docs_suspicious_links():
    """Test detection of suspicious links in documentation."""
    content = """
# Project Title

## API Reference
The API is available at http://localhost:8000/api

## Demo
Check out our demo at https://example.com/demo

## Test
For testing, use http://127.0.0.1:5000
"""
    
    with tempfile.NamedTemporaryFile(suffix='.md') as f:
        path = Path(f.name)
        with patch('pathlib.Path.read_text', return_value=content):
            violations = _analyze_docs(path)
            
            # Should detect suspicious links
            assert len(violations) >= 3
            assert any("localhost" in v.context["url"] for v in violations)
            assert any("example.com" in v.context["url"] for v in violations)
            assert any("127.0.0.1" in v.context["url"] for v in violations)


def test_analyze_docs_outdated_versions():
    """Test detection of outdated version references."""
    content = """
# Project Title

## Requirements
- Python 2.7
- Node 8.x
- Version 1.2.3-beta

## Installation
For Python 2.7, run:
```
pip install package
```
"""
    
    with tempfile.NamedTemporaryFile(suffix='.md') as f:
        path = Path(f.name)
        with patch('pathlib.Path.read_text', return_value=content):
            violations = _analyze_docs(path)
            
            # Should detect outdated versions
            assert len(violations) >= 3
            assert any("Python 2.7" in v.context["version"] for v in violations)
            assert any("Node 8" in v.context["version"] for v in violations)
            assert any("1.2.3-beta" in v.context["version"] for v in violations)


def test_analyze_docs_empty_readme():
    """Test detection of empty README."""
    content = "# Project\n\nA project."
    
    with tempfile.NamedTemporaryFile(suffix='.md') as f:
        path = Path(f.name)
        with patch('pathlib.Path.read_text', return_value=content):
            with patch('pathlib.Path.name', 'README.md'):
                violations = _analyze_docs(path)
                
                # Should detect empty README
                assert any(v.rule == "docs_empty" for v in violations)
                assert any("Empty README" in v.message for v in violations)


def test_analyze_docs_broken_markdown_links():
    """Test detection of broken markdown links."""
    content = """
# Project Title

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Broken Link](#this-heading-doesnt-exist)
- [Another Broken](#another##broken)
"""
    
    with tempfile.NamedTemporaryFile(suffix='.md') as f:
        path = Path(f.name)
        with patch('pathlib.Path.read_text', return_value=content):
            violations = _analyze_docs(path)
            
            # Should detect broken markdown links
            assert any(v.rule == "docs_brokenlink" for v in violations)
            assert any("another##broken" in v.context["link"] for v in violations)


@patch('pathlib.Path.exists')
def test_detect_documentation_violations_directory(mock_exists):
    """Test detection of documentation violations in a directory."""
    # Mock directory structure with README
    mock_exists.return_value = True
    
    with patch('pathlib.Path.is_dir', return_value=True):
        with patch('pathlib.Path.is_file', return_value=False):
            with patch('pathlib.Path.read_text', return_value="# Empty README"):
                file_path = Path("project_dir")
                content = ""
                thresholds = {}
                
                violations = detect_documentation_violations(file_path, content, None, thresholds)
                
                # Should detect violations in README
                assert len(violations) > 0