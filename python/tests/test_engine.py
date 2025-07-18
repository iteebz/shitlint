"""Tests for ShitLint rule engine."""

import tempfile
from pathlib import Path
import ast
import pytest
from shitlint.engine import RuleEngine


def test_rule_engine_initialization():
    """Test rule engine initialization with different brutality levels."""
    # Test default (professional) brutality
    engine = RuleEngine()
    assert engine.brutality == "professional"
    assert engine.thresholds["file_lines"]["brutal"] == 500
    
    # Test brutal level
    engine = RuleEngine(brutality="brutal")
    assert engine.brutality == "brutal"
    assert engine.thresholds["file_lines"]["brutal"] == 300
    
    # Test gentle level
    engine = RuleEngine(brutality="gentle")
    assert engine.brutality == "gentle"
    assert engine.thresholds["file_lines"]["brutal"] == 800


def test_rule_engine_config_filtering():
    """Test rule engine filters rules based on config."""
    # Only enable specific rules
    config = {
        "enabled_rules": {
            "giant_files": True,
            "import_ceremony": True,
            "duplicate_blocks": False,
            "complex_functions": False,
        }
    }
    
    engine = RuleEngine(config=config)
    # Should have fewer rules than default
    assert len(engine.rules) < 11


def test_analyze_file():
    """Test analyzing a file with violations."""
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w+') as f:
        # Create a file with multiple violations
        f.write("""
import os
import sys
import json
import time
import datetime
import requests
import numpy
import pandas
import matplotlib
import tensorflow

def process_data(data):
    # Magic number
    x = 42
    return data
""")
        f.flush()
        
        engine = RuleEngine(brutality="brutal")
        violations = engine.analyze_file(Path(f.name))
        
        # Should detect import ceremony
        assert any(v.rule == "import_ceremony" for v in violations)
        # Should detect magic number
        assert any(v.rule == "magic_number" for v in violations)
        # Should detect ceremony parameter
        assert any(v.rule == "ceremony_parameter" for v in violations)


def test_analyze_non_python_file():
    """Test analyzing a non-Python file."""
    with tempfile.NamedTemporaryFile(suffix='.md', mode='w+') as f:
        f.write("# Test Document\n\nThis is a test.")
        f.flush()
        
        engine = RuleEngine()
        violations = engine.analyze_file(Path(f.name))
        
        # Should not crash and return empty list
        assert isinstance(violations, list)
        assert len(violations) == 0


def test_cross_file_analysis():
    """Test cross-file analysis for duplicates."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create two files with duplicate code
        file1_path = Path(tmpdir) / "file1.py"
        file2_path = Path(tmpdir) / "file2.py"
        
        duplicate_code = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total
"""
        
        with open(file1_path, 'w') as f:
            f.write(duplicate_code)
        
        with open(file2_path, 'w') as f:
            f.write(duplicate_code)
        
        engine = RuleEngine()
        
        # Analyze both files
        engine.analyze_file(file1_path)
        engine.analyze_file(file2_path)
        
        # Get cross-file violations
        violations = engine.get_cross_file_violations()
        
        # Should detect duplicate code
        assert len(violations) > 0
        assert violations[0].rule == "cross_file_duplicate"