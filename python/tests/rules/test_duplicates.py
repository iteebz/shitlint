"""Tests for duplicate code rule violations."""

import ast
from pathlib import Path
import pytest
from shitlint.rules.duplicates import detect_duplicate_blocks, CrossFileAnalyzer
from shitlint.rules.base import Violation


def test_detect_duplicate_blocks_no_duplicates():
    """Test detection with no duplicate functions."""
    code = """
def function_one(a, b):
    return a + b

def function_two(a, b):
    return a * b
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {}
    
    violations = detect_duplicate_blocks(file_path, code, tree, thresholds)
    
    # Should not detect any violations
    assert len(violations) == 0


def test_detect_duplicate_blocks_with_duplicates():
    """Test detection with duplicate functions."""
    code = """
def add_numbers(a, b):
    result = a + b
    return result

def sum_values(x, y):
    result = x + y
    return result
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {}
    
    violations = detect_duplicate_blocks(file_path, code, tree, thresholds)
    
    # Should detect duplicate functions
    assert len(violations) == 1
    assert violations[0].rule == "duplicate_code"
    assert "add_numbers" in violations[0].message
    assert "sum_values" in violations[0].message


def test_detect_duplicate_blocks_non_python_file():
    """Test detection with non-Python file."""
    content = "This is not a Python file"
    file_path = Path("test.txt")
    thresholds = {}
    
    violations = detect_duplicate_blocks(file_path, content, None, thresholds)
    
    # Should not detect any violations
    assert len(violations) == 0


def test_cross_file_analyzer_no_duplicates():
    """Test cross-file analyzer with no duplicates."""
    code1 = """
def function_one(a, b):
    x = a + b
    y = x * 2
    return y
"""
    
    code2 = """
def function_two(a, b):
    x = a - b
    y = x * 2
    return y
"""
    
    tree1 = ast.parse(code1)
    tree2 = ast.parse(code2)
    file_path1 = Path("file1.py")
    file_path2 = Path("file2.py")
    
    analyzer = CrossFileAnalyzer()
    analyzer.collect_function_fingerprints(file_path1, tree1)
    analyzer.collect_function_fingerprints(file_path2, tree2)
    
    violations = analyzer.get_violations()
    
    # Should not detect any violations
    assert len(violations) == 0


def test_cross_file_analyzer_with_duplicates():
    """Test cross-file analyzer with duplicates."""
    code1 = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total
"""
    
    code2 = """
def compute_sum(products):
    result = 0
    for product in products:
        result += product.price * product.quantity
    return result
"""
    
    tree1 = ast.parse(code1)
    tree2 = ast.parse(code2)
    file_path1 = Path("file1.py")
    file_path2 = Path("file2.py")
    
    analyzer = CrossFileAnalyzer()
    analyzer.collect_function_fingerprints(file_path1, tree1)
    analyzer.collect_function_fingerprints(file_path2, tree2)
    
    violations = analyzer.get_violations()
    
    # Should detect cross-file duplicates
    assert len(violations) > 0
    assert violations[0].rule == "cross_file_duplicate"
    assert "duplicated across files" in violations[0].message


def test_cross_file_analyzer_tiny_functions():
    """Test cross-file analyzer ignores tiny functions."""
    code1 = """
def small_func(a):
    return a + 1
"""
    
    code2 = """
def another_small_func(b):
    return b + 1
"""
    
    tree1 = ast.parse(code1)
    tree2 = ast.parse(code2)
    file_path1 = Path("file1.py")
    file_path2 = Path("file2.py")
    
    analyzer = CrossFileAnalyzer()
    analyzer.collect_function_fingerprints(file_path1, tree1)
    analyzer.collect_function_fingerprints(file_path2, tree2)
    
    violations = analyzer.get_violations()
    
    # Should not detect any violations (tiny functions are ignored)
    assert len(violations) == 0