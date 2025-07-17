"""Core ShitLint functionality - Heuristics + AST detection."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from .rules import RuleEngine, Violation


@dataclass
class ShitLintResult:
    """Result of ShitLint analysis."""
    
    file_path: str
    message: str
    severity: str = "brutal"
    line_number: Optional[int] = None
    rule: Optional[str] = None


def analyze_code(path: Path) -> List[ShitLintResult]:
    """Analyze code with heuristics + AST rules."""
    engine = RuleEngine()
    results = []
    
    if path.is_file() and path.suffix == '.py':
        violations = engine.analyze_file(path)
        results.extend(_violations_to_results(violations))
    elif path.is_dir():
        # Recursively analyze all Python files
        for file_path in path.glob('**/*.py'):
            if file_path.is_file():
                violations = engine.analyze_file(file_path)
                results.extend(_violations_to_results(violations))
    
    return results


def _violations_to_results(violations: List[Violation]) -> List[ShitLintResult]:
    """Convert violations to results."""
    return [
        ShitLintResult(
            file_path=v.file_path,
            message=v.message,
            severity=v.severity,
            line_number=v.line_number,
            rule=v.rule
        )
        for v in violations
    ]