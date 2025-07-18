"""Base classes for ShitLint violations."""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Violation:
    """A detected code violation."""
    rule: str
    file_path: str
    line_number: int
    severity: str
    message: str
    context: Dict = None