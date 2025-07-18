"""OpenAI provider."""

from typing import List, Optional
from .base import LLMProvider, LLMAuthError, LLMRateLimitError
from ..core import ShitLintResult, AnalysisContext
from .prompts import build_roast_prompt, format_violations


class OpenAIProvider(LLMProvider):
    """OpenAI-powered roasting."""
    
    @property
    def provider_name(self) -> str:
        return "OpenAI"
    
    @property
    def api_key_env_var(self) -> str:
        return "OPENAI_API_KEY"
    
    @property
    def install_command(self) -> str:
        return "pip install openai"
    
    def _generate_roast(self, results: List[ShitLintResult], context: str, analysis_context: Optional[AnalysisContext] = None) -> str:
        import openai
        
        client = openai.OpenAI(api_key=self.api_key)
        violations = format_violations(results)
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": build_roast_prompt(violations, context, analysis_context)}],
                max_tokens=2000,
                temperature=0.7
            )
            
            usage = response.usage
            content = response.choices[0].message.content
            
            return f"{content}\n\n💸 OpenAI: {usage.prompt_tokens}+{usage.completion_tokens}={usage.total_tokens} tokens"
            
        except openai.AuthenticationError as e:
            raise LLMAuthError(f"Authentication failed: {e}")
        except openai.RateLimitError as e:
            raise LLMRateLimitError(f"Rate limit exceeded: {e}")
        except Exception:
            raise
    
