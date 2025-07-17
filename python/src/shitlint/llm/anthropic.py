"""Anthropic provider."""

from typing import List
from .base import LLMProvider
from ..core import ShitLintResult


class AnthropicProvider(LLMProvider):
    """Anthropic-powered roasting."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def roast(self, results: List[ShitLintResult], context: str) -> str:
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            violations = self._format_violations(results)
            
            response = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": self._build_prompt(violations, context)}]
            )
            
            usage = response.usage
            content = response.content[0].text
            
            return f"{content}\n\n💸 Anthropic: {usage.input_tokens}+{usage.output_tokens}={usage.input_tokens + usage.output_tokens} tokens"
            
        except Exception as e:
            return f"🤖 Anthropic roasting failed: {str(e)}"
    
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