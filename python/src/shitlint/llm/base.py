"""Base LLM provider interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..core import ShitLintResult, AnalysisContext


class LLMProvider(ABC):
    """Base class for LLM providers."""
    
    @abstractmethod
    def roast(self, results: List[ShitLintResult], context: str, analysis_context: Optional[AnalysisContext] = None) -> str:
        """Generate roast from violations."""
        pass