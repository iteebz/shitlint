"""Magic number and literal detection."""

from pathlib import Path
from typing import List, Dict, Set
import ast

from .base import Violation


def detect_magic_numbers(file_path: Path, content: str, tree: ast.AST, thresholds: Dict) -> List[Violation]:
    """Detect magic numbers and hardcoded values."""
    violations = []
    
    # Skip if not a Python file
    if tree is None:
        return violations
    
    # Common magic numbers to ignore (these are usually fine)
    allowed_numbers = {0, 1, -1, 2, 10, 100, 1000}
    
    # Add parent references to nodes
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            child.parent = parent
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant):
            # Check for magic numbers
            if isinstance(node.value, (int, float)) and node.value not in allowed_numbers:
                # Skip if it's in a constant assignment (NAME = VALUE)
                parent = getattr(node, 'parent', None)
                if isinstance(parent, ast.Assign) and len(parent.targets) == 1:
                    target = parent.targets[0]
                    if isinstance(target, ast.Name) and target.id.isupper():
                        continue  # Skip constants like MAX_SIZE = 500
                
                violations.append(Violation(
                    rule="magic_number",
                    file_path=str(file_path),
                    line_number=node.lineno,
                    severity="moderate",
                    message=f"Magic number {node.value} - extract to a named constant",
                    context={"value": node.value}
                ))
            
            # Check for hardcoded strings that smell like config
            elif isinstance(node.value, str) and len(node.value) > 3:
                suspicious_patterns = [
                    node.value.startswith(('http://', 'https://', 'ftp://')),
                    '/' in node.value and len(node.value) > 10,  # file paths
                    node.value.endswith(('.json', '.yaml', '.yml', '.xml', '.csv')),
                    '@' in node.value and '.' in node.value,  # emails
                    any(keyword in node.value.lower() for keyword in ['password', 'secret', 'key', 'token']),
                    node.value.startswith(('sk_', 'pk_', 'api_')),  # API keys
                    len(node.value) > 20 and node.value.replace('_', '').isalnum()  # Long alphanumeric strings
                ]
                
                if any(suspicious_patterns):
                    violations.append(Violation(
                        rule="hardcoded_string",
                        file_path=str(file_path),
                        line_number=node.lineno,
                        severity="moderate", 
                        message=f"Hardcoded string '{node.value[:50]}...' - extract to config",
                        context={"value": node.value}
                    ))
    
    return violations