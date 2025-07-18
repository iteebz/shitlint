"""Tests for naming rule violations."""

import ast
from pathlib import Path
import pytest
from shitlint.rules.naming import detect_naming_violations
from shitlint.rules.base import Violation


def test_ceremony_parameter():
    """Test detection of ceremony parameters."""
    code = """
def process_data(data):
    return data
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {"name_length": 25, "enable_loop_var_check": True}
    
    violations = detect_naming_violations(file_path, code, tree, thresholds)
    
    assert any(v.rule == "ceremony_parameter" for v in violations)
    assert any(v.message == "Function 'process_data' has ceremony parameter: 'data' - be specific" for v in violations)


def test_ceremony_class():
    """Test detection of ceremony class names."""
    code = """
class DataProcessor:
    pass

class UserManager:
    pass
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {"name_length": 25, "enable_loop_var_check": True}
    
    violations = detect_naming_violations(file_path, code, tree, thresholds)
    
    assert any(v.rule == "ceremony_class" for v in violations)
    assert any("UserManager" in v.message for v in violations)


def test_ceremony_variable():
    """Test detection of ceremony variable names."""
    code = """
def some_function():
    data = get_data()
    result = process(data)
    return result
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {"name_length": 25, "enable_loop_var_check": True}
    
    violations = detect_naming_violations(file_path, code, tree, thresholds)
    
    assert any(v.rule == "ceremony_variable" and v.context["variable"] == "data" for v in violations)
    assert any(v.rule == "ceremony_variable" and v.context["variable"] == "result" for v in violations)


def test_ai_generated_name():
    """Test detection of AI-generated long names."""
    code = """
def calculate_comprehensive_statistical_analysis_with_normalization(x):
    return x

very_long_descriptive_variable_name_that_explains_everything = 42
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {"name_length": 25, "enable_loop_var_check": True}
    
    violations = detect_naming_violations(file_path, code, tree, thresholds)
    
    assert any(v.rule == "ai_generated_name" and "function" in v.context for v in violations)
    assert any(v.rule == "ai_generated_name" and "variable" in v.context for v in violations)


def test_loop_variable_check():
    """Test loop variable check with different brutality levels."""
    code = """
for i in range(10):
    print(i)
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    
    # With loop check enabled (brutal mode)
    thresholds = {"name_length": 25, "enable_loop_var_check": True}
    violations_brutal = detect_naming_violations(file_path, code, tree, thresholds)
    
    # With loop check disabled (professional/gentle mode)
    thresholds = {"name_length": 25, "enable_loop_var_check": False}
    violations_gentle = detect_naming_violations(file_path, code, tree, thresholds)
    
    # Should flag in brutal mode but not in gentle mode
    assert any(v.rule == "ceremony_variable" and v.context["variable"] == "i" for v in violations_brutal)
    assert not any(v.rule == "ceremony_variable" and v.context["variable"] == "i" for v in violations_gentle)