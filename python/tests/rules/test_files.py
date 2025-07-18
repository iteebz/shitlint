"""Tests for file rule violations."""

import ast
from pathlib import Path
import pytest
from shitlint.rules.files import detect_giant_files
from shitlint.rules.base import Violation


def test_detect_giant_files_small():
    """Test detection of small files (no violations)."""
    # Create a small file content
    content = "\n".join([f"line {i}" for i in range(50)])
    file_path = Path("small_file.py")
    thresholds = {"file_lines": {"gentle": 200, "moderate": 300, "brutal": 500}}
    
    violations = detect_giant_files(file_path, content, None, thresholds)
    
    # Should not detect any violations
    assert len(violations) == 0


def test_detect_giant_files_gentle():
    """Test detection of medium files (gentle violations)."""
    # Create a medium file content
    content = "\n".join([f"line {i}" for i in range(250)])
    file_path = Path("medium_file.py")
    thresholds = {"file_lines": {"gentle": 200, "moderate": 300, "brutal": 500}}
    
    violations = detect_giant_files(file_path, content, None, thresholds)
    
    # Should detect gentle violation
    assert len(violations) == 1
    assert violations[0].severity == "gentle"
    assert "File getting chubby" in violations[0].message
    assert violations[0].context["line_count"] == 250


def test_detect_giant_files_moderate():
    """Test detection of large files (moderate violations)."""
    # Create a large file content
    content = "\n".join([f"line {i}" for i in range(400)])
    file_path = Path("large_file.py")
    thresholds = {"file_lines": {"gentle": 200, "moderate": 300, "brutal": 500}}
    
    violations = detect_giant_files(file_path, content, None, thresholds)
    
    # Should detect moderate violation
    assert len(violations) == 1
    assert violations[0].severity == "moderate"
    assert "Novel detected" in violations[0].message
    assert violations[0].context["line_count"] == 400


def test_detect_giant_files_brutal():
    """Test detection of massive files (brutal violations)."""
    # Create a massive file content
    content = "\n".join([f"line {i}" for i in range(600)])
    file_path = Path("massive_file.py")
    thresholds = {"file_lines": {"gentle": 200, "moderate": 300, "brutal": 500}}
    
    violations = detect_giant_files(file_path, content, None, thresholds)
    
    # Should detect brutal violation
    assert len(violations) == 1
    assert violations[0].severity == "brutal"
    assert "War crime detected" in violations[0].message
    assert violations[0].context["line_count"] == 600


def test_detect_giant_files_empty_lines():
    """Test that empty lines are not counted."""
    # Create content with empty lines
    content = "\n".join([f"line {i}" if i % 2 == 0 else "" for i in range(400)])
    file_path = Path("file_with_empty_lines.py")
    thresholds = {"file_lines": {"gentle": 200, "moderate": 300, "brutal": 500}}
    
    violations = detect_giant_files(file_path, content, None, thresholds)
    
    # Should detect gentle violation (200 non-empty lines)
    assert len(violations) == 1
    assert violations[0].severity == "gentle"
    assert violations[0].context["line_count"] == 200