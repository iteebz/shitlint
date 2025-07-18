"""Tests for magic number rule violations."""

import ast
from pathlib import Path
import pytest
from shitlint.rules.magic import detect_magic_numbers
from shitlint.rules.base import Violation


def test_detect_magic_numbers_allowed():
    """Test detection with allowed numbers (no violations)."""
    code = """
x = 0
y = 1
z = -1
a = 2
b = 10
c = 100
d = 1000
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {}
    
    violations = detect_magic_numbers(file_path, code, tree, thresholds)
    
    # Should not detect any violations
    assert len(violations) == 0


def test_detect_magic_numbers_constants():
    """Test detection with constants (no violations)."""
    code = """
MAX_SIZE = 500
MIN_THRESHOLD = 42
DEFAULT_TIMEOUT = 3600
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {}
    
    violations = detect_magic_numbers(file_path, code, tree, thresholds)
    
    # Should not detect any violations
    assert len(violations) == 0


def test_detect_magic_numbers_violations():
    """Test detection with magic numbers (violations)."""
    code = """
def calculate_price(quantity):
    base_price = quantity * 42.99
    tax = base_price * 0.08
    return base_price + tax

timeout = 3600
retry_count = 5
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {}
    
    violations = detect_magic_numbers(file_path, code, tree, thresholds)
    
    # Should detect violations for 42.99, 0.08, 3600, 5
    assert len(violations) == 4
    assert any(v.context["value"] == 42.99 for v in violations)
    assert any(v.context["value"] == 0.08 for v in violations)
    assert any(v.context["value"] == 3600 for v in violations)
    assert any(v.context["value"] == 5 for v in violations)


def test_detect_hardcoded_urls():
    """Test detection of hardcoded URLs."""
    code = """
api_url = "https://api.example.com/v1/data"
response = fetch(api_url)
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {}
    
    violations = detect_magic_numbers(file_path, code, tree, thresholds)
    
    # Should detect hardcoded URL
    assert len(violations) == 1
    assert violations[0].rule == "hardcoded_string"
    assert "https://api.example.com" in violations[0].message


def test_detect_hardcoded_paths():
    """Test detection of hardcoded file paths."""
    code = """
config_path = "/etc/app/config.json"
data = load_config(config_path)
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {}
    
    violations = detect_magic_numbers(file_path, code, tree, thresholds)
    
    # Should detect hardcoded path
    assert len(violations) == 1
    assert violations[0].rule == "hardcoded_string"
    assert "/etc/app/config.json" in violations[0].message


def test_detect_hardcoded_secrets():
    """Test detection of hardcoded secrets."""
    code = """
api_key = "sk_test_abcdefghijklmnopqrstuvwxyz"
password = "super_secret_password123"
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {}
    
    violations = detect_magic_numbers(file_path, code, tree, thresholds)
    
    # Should detect hardcoded secrets
    assert len(violations) == 2
    assert any("password" in v.context["value"] for v in violations)
    assert any("sk_test" in v.context["value"] for v in violations)