"""File-level violation detection."""

from pathlib import Path
from typing import List, Dict
import ast

from .base import Violation


def detect_giant_files(file_path: Path, content: str, tree: ast.AST, thresholds: Dict) -> List[Violation]:
    """Detect files that are too damn long."""
    lines = [line for line in content.split('\n') if line.strip()]
    line_count = len(lines)
    
    file_thresholds = thresholds["file_lines"]
    
    if line_count < file_thresholds["gentle"]:
        return []
    
    if line_count >= file_thresholds["brutal"]:
        severity = "brutal"
        message = f"War crime detected: {line_count} lines of architectural violence"
    elif line_count >= file_thresholds["moderate"]:
        severity = "moderate" 
        message = f"Novel detected: {line_count} lines of unnecessary complexity"
    else:
        severity = "gentle"
        message = f"File getting chubby: {line_count} lines need a diet"
    
    return [Violation(
        rule="giant_file",
        file_path=str(file_path),
        line_number=line_count,
        severity=severity,
        message=message,
        context={"line_count": line_count}
    )]