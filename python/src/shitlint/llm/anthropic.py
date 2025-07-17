"""Anthropic provider."""

from typing import List, Optional
from .base import LLMProvider
from ..core import ShitLintResult, AnalysisContext
from .prompts import build_roast_prompt, format_violations


class AnthropicProvider(LLMProvider):
    """Anthropic-powered roasting."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def roast(self, results: List[ShitLintResult], context: str, analysis_context: Optional[AnalysisContext] = None) -> str:
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            violations = format_violations(results)
            
            response = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": build_roast_prompt(violations, context, analysis_context)}]
            )
            
            usage = response.usage
            content = response.content[0].text
            
            return f"{content}\n\n💸 Anthropic: {usage.input_tokens}+{usage.output_tokens}={usage.input_tokens + usage.output_tokens} tokens"
            
        except Exception as e:
            return f"🤖 Anthropic roasting failed: {str(e)}"
    
