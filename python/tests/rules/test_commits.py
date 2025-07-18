"""Tests for commit message rule violations."""

import ast
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
from shitlint.rules.commits import detect_commit_violations
from shitlint.rules.base import Violation


@patch('shitlint.rules.commits.subprocess.run')
def test_detect_commit_violations_garbage(mock_run):
    """Test detection of garbage commit messages."""
    # Mock subprocess.run to return garbage commit messages
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = "fix\nupdate\nwip\ntemp\nfix stuff\nupdate things\nwtf\nasdf"
    mock_run.return_value = mock_process
    
    file_path = Path("test.py")
    content = "# Test file"
    thresholds = {}
    
    violations = detect_commit_violations(file_path, content, None, thresholds)
    
    # Should detect garbage commit messages
    assert len(violations) > 0
    assert any(v.rule == "commit_garbage" for v in violations)
    assert any("Garbage commit message" in v.message for v in violations)


@patch('shitlint.rules.commits.subprocess.run')
def test_detect_commit_violations_duplicates(mock_run):
    """Test detection of duplicate commit messages."""
    # Mock subprocess.run to return duplicate commit messages
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = "fix\nfix\nupdate\nupdate\nupdate"
    mock_run.return_value = mock_process
    
    file_path = Path("test.py")
    content = "# Test file"
    thresholds = {}
    
    violations = detect_commit_violations(file_path, content, None, thresholds)
    
    # Should detect duplicate commit messages
    assert any(v.rule == "commit_duplicates" for v in violations)
    assert any("Duplicate commit message" in v.message for v in violations)


@patch('shitlint.rules.commits.subprocess.run')
def test_detect_commit_violations_good_messages(mock_run):
    """Test that good commit messages are not flagged."""
    # Mock subprocess.run to return good commit messages
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = "feat: add new feature\nfix(core): resolve critical bug\ndocs: update README"
    mock_run.return_value = mock_process
    
    file_path = Path("test.py")
    content = "# Test file"
    thresholds = {}
    
    violations = detect_commit_violations(file_path, content, None, thresholds)
    
    # Should not detect any violations
    assert len(violations) == 0


@patch('shitlint.rules.commits.subprocess.run')
def test_detect_commit_violations_no_git(mock_run):
    """Test handling when git is not available."""
    # Mock subprocess.run to simulate git error
    mock_process = MagicMock()
    mock_process.returncode = 1
    mock_run.return_value = mock_process
    
    file_path = Path("test.py")
    content = "# Test file"
    thresholds = {}
    
    violations = detect_commit_violations(file_path, content, None, thresholds)
    
    # Should not crash and return empty list
    assert isinstance(violations, list)
    assert len(violations) == 0


@patch('shitlint.rules.commits.subprocess.run')
def test_detect_commit_violations_exception(mock_run):
    """Test handling when subprocess raises an exception."""
    # Mock subprocess.run to raise an exception
    mock_run.side_effect = Exception("Git error")
    
    file_path = Path("test.py")
    content = "# Test file"
    thresholds = {}
    
    violations = detect_commit_violations(file_path, content, None, thresholds)
    
    # Should not crash and return empty list
    assert isinstance(violations, list)
    assert len(violations) == 0