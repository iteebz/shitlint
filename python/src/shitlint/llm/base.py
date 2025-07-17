"""Base LLM provider interface."""

from abc import ABC, abstractmethod
from typing import List
from ..core import ShitLintResult


class LLMProvider(ABC):
    """Base class for LLM providers."""
    
    @abstractmethod
    def roast(self, results: List[ShitLintResult], context: str) -> str:
        """Generate roast from violations."""
        pass