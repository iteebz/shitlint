"""Import-related violation detection."""

from pathlib import Path
from typing import List, Dict
import ast

from .base import Violation


def detect_import_ceremony(file_path: Path, content: str, tree: ast.AST, thresholds: Dict) -> List[Violation]:
    """Detect import addiction."""
    # Skip if not a Python file
    if tree is None:
        return []
    
    imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend([alias.name for alias in node.names])
        elif isinstance(node, ast.ImportFrom):
            # Count each individual import from the module
            imports.extend([alias.name for alias in node.names])
    
    import_count = len(imports)
    import_thresholds = thresholds["imports"]
    
    if import_count < import_thresholds["moderate"]:
        return []
    
    if import_count >= import_thresholds["brutal"]:
        severity = "brutal"
        message = f"Import addiction detected: {import_count} dependencies is architectural heroin"
    else:
        severity = "moderate"
        message = f"Import ceremony: {import_count} imports suggests tight coupling"
    
    return [Violation(
        rule="import_ceremony",
        file_path=str(file_path),
        line_number=1,
        severity=severity,
        message=message,
        context={"import_count": import_count, "imports": imports}
    )]