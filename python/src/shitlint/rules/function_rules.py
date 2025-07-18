"""Function-level violation detection."""

from pathlib import Path
from typing import List, Dict
import ast

from .base import Violation


def detect_complex_functions(file_path: Path, content: str, tree: ast.AST, thresholds: Dict) -> List[Violation]:
    """Detect overly complex functions."""
    violations = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Count decision points
            complexity = 1
            
            for child in ast.walk(node):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                    complexity += 1
                elif isinstance(child, ast.BoolOp):
                    complexity += len(child.values) - 1
            
            # Count lines in function
            func_lines = len([line for line in content.split('\n')[node.lineno-1:node.end_lineno] if line.strip()])
            
            complexity_thresholds = thresholds["complexity"]
            line_thresholds = thresholds["function_lines"]
            
            if complexity > complexity_thresholds["moderate"] or func_lines > line_thresholds["moderate"]:
                if complexity > complexity_thresholds["brutal"] or func_lines > line_thresholds["brutal"]:
                    severity = "brutal"
                    message = f"Function '{node.name}' is a complexity nightmare: {complexity} branches, {func_lines} lines"
                else:
                    severity = "moderate"
                    message = f"Function '{node.name}' is getting complex: {complexity} branches, {func_lines} lines"
                
                violations.append(Violation(
                    rule="complex_function",
                    file_path=str(file_path),
                    line_number=node.lineno,
                    severity=severity,
                    message=message,
                    context={"complexity": complexity, "lines": func_lines}
                ))
    
    return violations