"""Core ShitLint functionality."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class ShitLintResult:
    """Result of ShitLint analysis."""
    
    file_path: str
    message: str
    severity: str = "brutal"
    line_number: Optional[int] = None


def analyze_code(path: Path) -> List[ShitLintResult]:
    """Analyze code and return brutal truth."""
    return [
        ShitLintResult(
            file_path=str(path),
            message="Your code exists. That's already a problem.",
            severity="brutal"
        )
    ]