"""Gemini provider."""

from typing import List, Optional
from .base import LLMProvider, LLMAuthError, LLMRateLimitError, LLMContentBlockedError
from ..core import ShitLintResult, AnalysisContext
from .prompts import build_roast_prompt, format_violations


class GeminiProvider(LLMProvider):
    """Gemini-powered roasting (cheapest option)."""
    
    @property
    def provider_name(self) -> str:
        return "Gemini"
    
    @property
    def api_key_env_var(self) -> str:
        return "GEMINI_API_KEY"
    
    @property
    def install_command(self) -> str:
        return "pip install google-generativeai"
    
    def _generate_roast(self, results: List[ShitLintResult], context: str, analysis_context: Optional[AnalysisContext] = None) -> str:
        import google.generativeai as genai
        
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
        violations = format_violations(results)
        
        try:
            response = model.generate_content(
                build_roast_prompt(violations, context, analysis_context),
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=0.7
                )
            )
            
            usage = response.usage_metadata
            content = response.text
            
            return f"{content}\n\n💸 Gemini: {usage.prompt_token_count}+{usage.candidates_token_count}={usage.total_token_count} tokens"
            
        except genai.types.generation_types.StopCandidateException:
            raise LLMContentBlockedError("Response blocked by safety filters")
        except Exception as e:
            error_msg = str(e).lower()
            if "api key" in error_msg or "authentication" in error_msg:
                raise LLMAuthError(f"Authentication failed: {e}")
            elif "quota" in error_msg or "rate" in error_msg:
                raise LLMRateLimitError(f"Rate limit exceeded: {e}")
            else:
                raise
    
