"""Base LLM provider interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..core import ShitLintResult, AnalysisContext


class LLMError(Exception):
    """Base LLM error."""
    pass


class LLMAuthError(LLMError):
    """Authentication failed."""
    pass


class LLMRateLimitError(LLMError):
    """Rate limit exceeded."""
    pass


class LLMContentBlockedError(LLMError):
    """Content blocked by provider."""
    pass


class LLMProvider(ABC):
    """Base class for LLM providers."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def roast(self, results: List[ShitLintResult], context: str, analysis_context: Optional[AnalysisContext] = None) -> str:
        """Generate roast from violations with unified error handling."""
        try:
            return self._generate_roast(results, context, analysis_context)
        except LLMAuthError:
            return f"🤖 {self.provider_name} auth failed: Check your {self.api_key_env_var}"
        except LLMRateLimitError:
            return f"🤖 {self.provider_name} rate limited: Try again later or use different provider"
        except LLMContentBlockedError:
            return f"🤖 {self.provider_name} blocked response (too brutal). Try again or use different provider."
        except ImportError:
            return f"🤖 {self.provider_name} unavailable: {self.install_command}"
        except Exception as e:
            return f"🤖 {self.provider_name} roasting failed: {str(e)}"
    
    @abstractmethod
    def _generate_roast(self, results: List[ShitLintResult], context: str, analysis_context: Optional[AnalysisContext] = None) -> str:
        """Generate roast - implement in subclass."""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Provider name for error messages."""
        pass
    
    @property
    @abstractmethod
    def api_key_env_var(self) -> str:
        """Environment variable name for API key."""
        pass
    
    @property
    @abstractmethod
    def install_command(self) -> str:
        """Installation command for provider."""
        pass