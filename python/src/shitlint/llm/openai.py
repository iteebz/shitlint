"""OpenAI provider."""

from typing import List, Optional
from .base import LLMProvider
from ..core import ShitLintResult, AnalysisContext
from .prompts import build_roast_prompt, format_violations


class OpenAIProvider(LLMProvider):
    """OpenAI-powered roasting."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def roast(self, results: List[ShitLintResult], context: str, analysis_context: Optional[AnalysisContext] = None) -> str:
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            violations = format_violations(results)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": build_roast_prompt(violations, context, analysis_context)}],
                max_tokens=2000,
                temperature=0.7
            )
            
            usage = response.usage
            content = response.choices[0].message.content
            
            return f"{content}\n\n💸 OpenAI: {usage.prompt_tokens}+{usage.completion_tokens}={usage.total_tokens} tokens"
            
        except Exception as e:
            return f"🤖 OpenAI roasting failed: {str(e)}"
    
