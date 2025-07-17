"""Gemini provider."""

from typing import List
from .base import LLMProvider
from ..core import ShitLintResult


class GeminiProvider(LLMProvider):
    """Gemini-powered roasting (cheapest option)."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def roast(self, results: List[ShitLintResult], context: str) -> str:
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            
            violations = self._format_violations(results)
            
            response = model.generate_content(
                self._build_prompt(violations, context),
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=0.7
                )
            )
            
            usage = response.usage_metadata
            content = response.text
            
            return f"{content}\n\n💸 Gemini: {usage.prompt_token_count}+{usage.candidates_token_count}={usage.total_token_count} tokens"
            
        except Exception as e:
            return f"🤖 Gemini roasting failed: {str(e)}"
    
    def _format_violations(self, results: List[ShitLintResult]) -> str:
        if not results:
            return "No violations detected"
        
        return "\n".join(f"- {r.severity.upper()}: {r.file_path}:{r.line_number or '?'} - {r.message}" 
                        for r in results)
    
    def _build_prompt(self, violations: str, context: str) -> str:
        return f"""You are an expert software architect with zero tolerance for bullshit code. 

Analyze these code violations with brutal honesty and architectural insight:

CONTEXT: {context or 'Unknown codebase'}

VIOLATIONS:
{violations}

Your response should:
1. Be brutally honest about architectural problems
2. Focus on WHY these violations matter (maintainability, testability, coupling)
3. Provide specific, actionable recommendations
4. Use sharp, dry humor (not juvenile insults)
5. Reference architectural principles (SOLID, DRY, KISS)

Format as a roast session - be entertaining but constructive. Start with "🔥 ARCHITECTURAL ROAST SESSION" and end with concrete next steps."""