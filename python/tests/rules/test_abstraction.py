"""Tests for abstraction rule violations."""

import ast
from pathlib import Path
import pytest
from shitlint.rules.abstraction import detect_over_abstraction
from shitlint.rules.base import Violation


def test_detect_god_abstraction():
    """Test detection of god abstractions with too many abstract methods."""
    code = """
class GodInterface:
    def method1(self): raise NotImplementedError()
    def method2(self): raise NotImplementedError()
    def method3(self): raise NotImplementedError()
    def method4(self): raise NotImplementedError()
    def method5(self): raise NotImplementedError()
    def method6(self): raise NotImplementedError()
    def method7(self): raise NotImplementedError()
    def method8(self): raise NotImplementedError()
    def method9(self): raise NotImplementedError()
    def method10(self): raise NotImplementedError()
    def method11(self): raise NotImplementedError()
    def method12(self): raise NotImplementedError()
    def method13(self): raise NotImplementedError()
    def method14(self): raise NotImplementedError()
    def method15(self): raise NotImplementedError()
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {}
    
    violations = detect_over_abstraction(file_path, code, tree, thresholds)
    
    # Should detect god abstraction (15 methods >= 10 threshold)
    assert any(v.rule == "god_abstraction" for v in violations)
    assert any("god abstraction" in v.message for v in violations)


def test_detect_wrapper_hell():
    """Test detection of wrapper classes that mostly delegate."""
    code = """
class Wrapper:
    def __init__(self, obj):
        self.obj = obj
        
    def method1(self, arg):
        return self.obj.method1(arg)
        
    def method2(self, arg1, arg2):
        return self.obj.method2(arg1, arg2)
        
    def method3(self):
        return self.obj.method3()
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {}
    
    violations = detect_over_abstraction(file_path, code, tree, thresholds)
    
    # Should detect wrapper hell
    assert any(v.rule == "wrapper_hell" for v in violations)
    assert any("wrapper hell" in v.message for v in violations)


def test_detect_inheritance_hell():
    """Test detection of deep inheritance chains."""
    code = """
class Base:
    pass
    
class Level1(Base):
    pass
    
class Level2(Level1):
    pass
    
class Level3(Level2):
    pass
    
class Level4(Level3):
    pass
    
class Level5(Level4):
    pass
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {}
    
    violations = detect_over_abstraction(file_path, code, tree, thresholds)
    
    # Should detect inheritance hell
    assert any(v.rule == "inheritance_hell" for v in violations)
    assert any("inheritance depth" in v.message for v in violations)


def test_detect_pointless_factory():
    """Test detection of pointless factory classes."""
    code = """
class UserFactory:
    def create_user(self, name, email):
        return User(name, email)
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {}
    
    violations = detect_over_abstraction(file_path, code, tree, thresholds)
    
    # Should detect pointless factory
    assert any(v.rule == "pointless_factory" for v in violations)
    assert any("pointless factory" in v.message for v in violations)


def test_detect_interface_overkill():
    """Test detection of interface overkill."""
    code = """
class AbstractService:
    def method1(self): raise NotImplementedError()
    def method2(self): raise NotImplementedError()
    def method3(self): raise NotImplementedError()
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {}
    
    violations = detect_over_abstraction(file_path, code, tree, thresholds)
    
    # Should detect interface overkill
    assert any(v.rule == "interface_overkill" for v in violations)
    assert any("might be overkill" in v.message for v in violations)


def test_no_violations_simple_class():
    """Test that simple, well-designed classes have no violations."""
    code = """
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        
    def get_display_name(self):
        return f"{self.name} <{self.email}>"
"""
    tree = ast.parse(code)
    file_path = Path("test.py")
    thresholds = {}
    
    violations = detect_over_abstraction(file_path, code, tree, thresholds)
    
    # Should not detect any violations
    assert len(violations) == 0