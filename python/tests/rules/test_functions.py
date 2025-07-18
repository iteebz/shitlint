"""Tests for function rule violations."""

import ast
from pathlib import Path
import pytest
from shitlint.rules.functions import detect_complex_functions, detect_parameter_hell
from shitlint.rules.base import Violation


def test_detect_complex_functions_simple():
    """Test detection with simple functions (no violations)."""
    code = """
def simple_function():
    return 42
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {
        "complexity": {"moderate": 5, "brutal": 10},
        "function_lines": {"moderate": 20, "brutal": 40}
    }
    
    violations = detect_complex_functions(file_path, code, tree, thresholds)
    
    # Should not detect any violations
    assert len(violations) == 0


def test_detect_complex_functions_moderate():
    """Test detection with moderately complex functions."""
    code = """
def moderate_function(x):
    if x > 0:
        if x > 10:
            return "large"
        else:
            return "medium"
    else:
        if x < -10:
            return "very negative"
        else:
            return "negative"
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {
        "complexity": {"moderate": 3, "brutal": 10},
        "function_lines": {"moderate": 20, "brutal": 40}
    }
    
    violations = detect_complex_functions(file_path, code, tree, thresholds)
    
    # Should detect moderate violation
    assert len(violations) == 1
    assert violations[0].severity == "moderate"
    assert "getting complex" in violations[0].message
    assert violations[0].context["complexity"] > 3


def test_detect_complex_functions_brutal():
    """Test detection with extremely complex functions."""
    code = """
def complex_function(x):
    result = 0
    if x > 0:
        if x > 10:
            if x > 100:
                result = x * 2
            else:
                result = x * 1.5
        else:
            for i in range(x):
                if i % 2 == 0:
                    result += i
                else:
                    result -= i
    else:
        if x < -10:
            try:
                result = -x * 2
            except:
                result = 0
        else:
            while x < 0:
                x += 1
                result -= 1
    return result
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {
        "complexity": {"moderate": 5, "brutal": 8},
        "function_lines": {"moderate": 20, "brutal": 40}
    }
    
    violations = detect_complex_functions(file_path, code, tree, thresholds)
    
    # Should detect brutal violation (complexity is 9 >= 8)
    assert len(violations) == 1
    assert violations[0].severity == "brutal"
    assert "complexity nightmare" in violations[0].message
    assert violations[0].context["complexity"] >= 8


def test_detect_complex_functions_long():
    """Test detection with long functions."""
    # Create a long function
    code = "def long_function():\n" + "\n".join([f"    print({i})" for i in range(50)])
    
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {
        "complexity": {"moderate": 5, "brutal": 10},
        "function_lines": {"moderate": 20, "brutal": 40}
    }
    
    violations = detect_complex_functions(file_path, code, tree, thresholds)
    
    # Should detect brutal violation due to length
    assert len(violations) == 1
    assert violations[0].severity == "brutal"
    assert violations[0].context["lines"] > 40


def test_detect_parameter_hell_few_params():
    """Test detection with few parameters (no violations)."""
    code = """
def good_function(a, b, c):
    return a + b + c
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {"parameters": {"moderate": 4, "brutal": 6}}
    
    violations = detect_parameter_hell(file_path, code, tree, thresholds)
    
    # Should not detect any violations
    assert len(violations) == 0


def test_detect_parameter_hell_moderate():
    """Test detection with moderate number of parameters."""
    code = """
def many_params(a, b, c, d, e):
    return a + b + c + d + e
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {"parameters": {"moderate": 4, "brutal": 6}}
    
    violations = detect_parameter_hell(file_path, code, tree, thresholds)
    
    # Should detect moderate violation
    assert len(violations) == 1
    assert violations[0].severity == "moderate"
    assert "consider refactoring" in violations[0].message
    assert violations[0].context["param_count"] == 5


def test_detect_parameter_hell_brutal():
    """Test detection with excessive parameters."""
    code = """
def parameter_hell(a, b, c, d, e, f, g, h):
    return a + b + c + d + e + f + g + h
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {"parameters": {"moderate": 4, "brutal": 6}}
    
    violations = detect_parameter_hell(file_path, code, tree, thresholds)
    
    # Should detect brutal violation
    assert len(violations) == 1
    assert violations[0].severity == "brutal"
    assert "parameter hell detected" in violations[0].message
    assert violations[0].context["param_count"] == 8


def test_detect_parameter_hell_method():
    """Test detection with methods (should exclude self)."""
    code = """
class MyClass:
    def method(self, a, b, c, d):
        return a + b + c + d
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {"parameters": {"moderate": 5, "brutal": 6}}
    
    violations = detect_parameter_hell(file_path, code, tree, thresholds)
    
    # Should not detect violations (4 params after excluding self < 5 moderate threshold)
    assert len(violations) == 0