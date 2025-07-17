"""Gemini provider."""

from typing import List, Optional
from .base import LLMProvider
from ..core import ShitLintResult, AnalysisContext
from .prompts import build_roast_prompt, format_violations


class GeminiProvider(LLMProvider):
    """Gemini-powered roasting (cheapest option)."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def roast(self, results: List[ShitLintResult], context: str, analysis_context: Optional[AnalysisContext] = None) -> str:
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            
            violations = format_violations(results)
            
            response = model.generate_content(
                build_roast_prompt(violations, context, analysis_context),
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,  # Removed arbitrary limit
                    temperature=0.7
                )
            )
            
            usage = response.usage_metadata
            content = response.text
            
            return f"{content}\n\n💸 Gemini: {usage.prompt_token_count}+{usage.candidates_token_count}={usage.total_token_count} tokens"
            
        except Exception as e:
            return f"🤖 Gemini roasting failed: {str(e)}"
    
