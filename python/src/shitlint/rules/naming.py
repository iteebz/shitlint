"""Naming violation detection."""

from pathlib import Path
from typing import List, Dict
import ast

from .base import Violation


def detect_naming_violations(file_path: Path, content: str, tree: ast.AST, thresholds: Dict) -> List[Violation]:
    """Detect naming violations."""
    violations = []
    
    # Skip if not a Python file
    if tree is None:
        return violations
    
    ceremony_vars = {
        'data', 'result', 'temp', 'obj', 'item', 'val', 'thing', 'stuff', 
        'var', 'x', 'y', 'z', 'i', 'j', 'k', 'value', 'element', 'node',
        'info', 'content', 'payload', 'response', 'request', 'params', 'args'
    }
    
    ceremony_classes = {
        'Manager', 'Handler', 'Processor', 'Utility', 'Helper', 'Service',
        'Factory', 'Builder', 'Provider', 'Controller', 'Adapter', 'Wrapper'
    }
    
    max_length = thresholds["name_length"]
    enable_loop_check = thresholds["enable_loop_var_check"]
    
    class NameCollector(ast.NodeVisitor):
        def __init__(self):
            self.violations = []
            self.current_function = None
            
        def visit_FunctionDef(self, node):
            self.current_function = node.name
            
            # Check function parameters
            for arg in node.args.args:
                if arg.arg in ceremony_vars:
                    self.violations.append(Violation(
                        rule="ceremony_parameter",
                        file_path=str(file_path),
                        line_number=node.lineno,
                        severity="moderate",
                        message=f"Function '{node.name}' has ceremony parameter: '{arg.arg}' - be specific",
                        context={"function": node.name, "parameter": arg.arg}
                    ))
            
            # Check function name length
            if len(node.name) > max_length:
                self.violations.append(Violation(
                    rule="ai_generated_name",
                    file_path=str(file_path),
                    line_number=node.lineno,
                    severity="moderate", 
                    message=f"Function '{node.name}' looks AI-generated: {len(node.name)} chars - simplify",
                    context={"function": node.name, "length": len(node.name)}
                ))
            
            self.generic_visit(node)
            self.current_function = None
            
        def visit_ClassDef(self, node):
            # Check for ceremony class names
            if any(ceremony in node.name for ceremony in ceremony_classes):
                self.violations.append(Violation(
                    rule="ceremony_class",
                    file_path=str(file_path),
                    line_number=node.lineno,
                    severity="moderate",
                    message=f"Class '{node.name}' is ceremony - what does it actually do?",
                    context={"class": node.name}
                ))
            
            # Check class name length
            if len(node.name) > max_length:
                self.violations.append(Violation(
                    rule="ai_generated_name",
                    file_path=str(file_path),
                    line_number=node.lineno,
                    severity="moderate",
                    message=f"Class '{node.name}' looks AI-generated: {len(node.name)} chars - simplify",
                    context={"class": node.name, "length": len(node.name)}
                ))
            
            self.generic_visit(node)
            
        def visit_Assign(self, node):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    
                    if var_name in ceremony_vars:
                        # Skip loop variables unless brutal mode
                        if not enable_loop_check and var_name in {'i', 'j', 'k', 'x', 'y', 'z'}:
                            continue
                            
                        func_context = f" in {self.current_function}" if self.current_function else ""
                        self.violations.append(Violation(
                            rule="ceremony_variable",
                            file_path=str(file_path),
                            line_number=node.lineno,
                            severity="gentle",
                            message=f"Variable '{var_name}'{func_context} is ceremony - be descriptive",
                            context={"variable": var_name, "function": self.current_function}
                        ))
                    
                    # Check for AI monstrosities
                    if len(var_name) > max_length:
                        func_context = f" in {self.current_function}" if self.current_function else ""
                        self.violations.append(Violation(
                            rule="ai_generated_name",
                            file_path=str(file_path),
                            line_number=node.lineno,
                            severity="moderate",
                            message=f"Variable '{var_name}'{func_context} looks AI-generated: {len(var_name)} chars",
                            context={"variable": var_name, "length": len(var_name)}
                        ))
            
            self.generic_visit(node)
            
        def visit_For(self, node):
            """Check for ceremony loop variables."""
            if isinstance(node.target, ast.Name):
                var_name = node.target.id
                
                if var_name in ceremony_vars and enable_loop_check:
                    func_context = f" in {self.current_function}" if self.current_function else ""
                    self.violations.append(Violation(
                        rule="ceremony_variable",
                        file_path=str(file_path),
                        line_number=node.lineno,
                        severity="gentle",
                        message=f"Loop variable '{var_name}'{func_context} is ceremony - be descriptive",
                        context={"variable": var_name, "function": self.current_function}
                    ))
            
            self.generic_visit(node)
    
    collector = NameCollector()
    collector.visit(tree)
    violations.extend(collector.violations)
    
    return violations