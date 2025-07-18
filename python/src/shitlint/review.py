"""Adversarial design review using CLAUDE.md doctrine."""

from pathlib import Path
from typing import Dict, Optional
import re

from .llm import OpenAIProvider, AnthropicProvider, GeminiProvider
import os


def review_design(content: str, context: Optional[str] = None) -> str:
    """Adversarial design review using CLAUDE.md doctrine."""
    
    context_data = _parse_context(context) if context else {}
    
    prompt = f"""Apply CLAUDE.md doctrine to this proposal. Be brutally honest about architectural bullshit.

DOCTRINE:
- DRY + SOLID over wet spaghetti
- Decoupled + Extensible over tight ceremony  
- Pragmatic + Modular over monolithic monsters
- Auto-magical over manual ceremony
- Beautiful over bullshit
- Zero Line Philosophy: Every line must justify itself

CONTEXT: {_format_context(context_data)}

PROPOSAL:
{content}

FLAG THESE VIOLATIONS:
- Feature creep without users
- Over-engineering for imaginary scale
- Enterprise patterns in small teams
- Abstraction theatre (interfaces with one impl)
- Premature optimization
- Ceremony without purpose

OUTPUT FORMAT:
⏺ CRITICAL EVALUATION: [BRUTAL VERDICT]

⏺ Analysis
  ⎿ ☒ [Quantified problem with numbers]
  ⎿ ☒ [Another violation]

VERDICT: [One sentence brutal assessment]"""

    try:
        # Try providers in order: Gemini (cheapest), OpenAI, Anthropic
        for provider_class, env_var in [
            (GeminiProvider, "GEMINI_API_KEY"),
            (OpenAIProvider, "OPENAI_API_KEY"),
            (AnthropicProvider, "ANTHROPIC_API_KEY")
        ]:
            if api_key := os.getenv(env_var):
                provider = provider_class(api_key)
                response = provider._generate_simple(prompt)
                return response
        
        return "⏺ CRITICAL EVALUATION: NO API KEYS\n\nSet GEMINI_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY to get brutal AI assessment.\nReview manually using CLAUDE.md doctrine."
        
    except Exception as e:
        return f"⏺ CRITICAL EVALUATION: LLM FAILURE\n\nCouldn't roast your proposal: {e}\nReview it yourself using CLAUDE.md doctrine."


def _parse_context(context: str) -> Dict[str, str]:
    """Parse context string like 'team=2,users=47,perf=120ms'."""
    if not context:
        return {}
    
    result = {}
    for part in context.split(','):
        if '=' in part:
            key, value = part.split('=', 1)
            result[key.strip()] = value.strip()
    
    return result


def _format_context(context_data: Dict[str, str]) -> str:
    """Format context for prompt."""
    if not context_data:
        return "No context provided"
    
    formatted = []
    for key, value in context_data.items():
        formatted.append(f"{key}: {value}")
    
    return ", ".join(formatted)