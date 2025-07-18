"""Tests for import rule violations."""

import ast
from pathlib import Path
import pytest
from shitlint.rules.imports import detect_import_ceremony
from shitlint.rules.base import Violation


def test_detect_import_ceremony_few_imports():
    """Test detection with few imports (no violations)."""
    code = """
import os
import sys
from pathlib import Path
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {"imports": {"moderate": 10, "brutal": 15}}
    
    violations = detect_import_ceremony(file_path, code, tree, thresholds)
    
    # Should not detect any violations
    assert len(violations) == 0


def test_detect_import_ceremony_moderate():
    """Test detection with moderate number of imports."""
    code = """
import os
import sys
import json
import time
import datetime
import requests
import numpy
import pandas
import matplotlib
import re
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {"imports": {"moderate": 10, "brutal": 15}}
    
    violations = detect_import_ceremony(file_path, code, tree, thresholds)
    
    # Should detect moderate violation
    assert len(violations) == 1
    assert violations[0].severity == "moderate"
    assert "Import ceremony" in violations[0].message
    assert violations[0].context["import_count"] == 10


def test_detect_import_ceremony_brutal():
    """Test detection with excessive imports."""
    code = """
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
import torch
import sklearn
import scipy
import seaborn
import plotly
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {"imports": {"moderate": 10, "brutal": 15}}
    
    violations = detect_import_ceremony(file_path, code, tree, thresholds)
    
    # Should detect brutal violation
    assert len(violations) == 1
    assert violations[0].severity == "brutal"
    assert "Import addiction" in violations[0].message
    assert violations[0].context["import_count"] == 15


def test_detect_import_ceremony_from_imports():
    """Test detection with from imports."""
    code = """
from os import path
from sys import argv
from datetime import datetime, timedelta
from collections import defaultdict, Counter, deque
from itertools import chain, combinations
from functools import partial, reduce
from typing import List, Dict, Optional, Union, Any
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {"imports": {"moderate": 10, "brutal": 15}}
    
    violations = detect_import_ceremony(file_path, code, tree, thresholds)
    
    # Should detect brutal violation (16 imports >= 15 brutal threshold)
    assert len(violations) == 1
    assert violations[0].severity == "brutal"
    assert "Import addiction" in violations[0].message
    assert violations[0].context["import_count"] == 16


def test_detect_import_ceremony_non_python_file():
    """Test detection with non-Python file."""
    content = "This is not a Python file"
    file_path = Path("test.txt")
    thresholds = {"imports": {"moderate": 10, "brutal": 15}}
    
    violations = detect_import_ceremony(file_path, content, None, thresholds)
    
    # Should not detect any violations
    assert len(violations) == 0