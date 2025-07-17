"""Clean roaster - no ceremony, proper separation."""

import os
from typing import List, Optional
from .core import ShitLintResult
from .llm import OpenAIProvider, AnthropicProvider, GeminiProvider


def format_violations(results: List[ShitLintResult]) -> str:
    """Format violations for display."""
    if not results:
        return "No violations found. Suspiciously clean code... 🤔"
    
    output = []
    output.append(f"🚨 VIOLATIONS DETECTED ({len(results)} issues)")
    output.append("")
    
    # Group by severity
    brutal = [r for r in results if r.severity == "brutal"]
    moderate = [r for r in results if r.severity == "moderate"]
    gentle = [r for r in results if r.severity == "gentle"]
    
    if brutal:
        output.append("💀 BRUTAL VIOLATIONS:")
        for result in brutal:
            output.append(f"  - {result.file_path}:{result.line_number or '?'} - {result.message}")
        output.append("")
    
    if moderate:
        output.append("⚠️  MODERATE VIOLATIONS:")
        for result in moderate:
            output.append(f"  - {result.file_path}:{result.line_number or '?'} - {result.message}")
        output.append("")
    
    if gentle:
        output.append("👀 GENTLE VIOLATIONS:")
        for result in gentle:
            output.append(f"  - {result.file_path}:{result.line_number or '?'} - {result.message}")
    
    return "\n".join(output)


def generate_roast(results: List[ShitLintResult], context: str = "") -> str:
    """Generate brutal architectural roast via LLM."""
    
    if not results:
        return _clean_code_response(context)
    
    # Try LLM first, fallback to static
    if llm_roast := _try_llm_roast(results, context):
        return llm_roast
    
    # Static fallback
    return _static_roast(results, context)


def _clean_code_response(context: str) -> str:
    """Response for clean code."""
    return f"""
🤨 SUSPICIOUSLY CLEAN CODE DETECTED

Either you're an architectural genius, or you're hiding the bodies.

Context: {context or 'Unknown codebase'}

Possible explanations:
1. You actually know what you're doing (unlikely)
2. The code is too simple to mess up (boring)
3. You haven't written enough code yet (give it time)
4. Our detection rules suck (probable)

Recommendation: Write more code, then come back for proper roasting.
"""


def _try_llm_roast(results: List[ShitLintResult], context: str) -> Optional[str]:
    """Try LLM roasting with user-provided API keys."""
    
    # Check for Gemini API key first (cheapest)
    if gemini_key := os.getenv("GEMINI_API_KEY"):
        return GeminiProvider(gemini_key).roast(results, context)
    
    # Check for OpenAI API key
    if openai_key := os.getenv("OPENAI_API_KEY"):
        return OpenAIProvider(openai_key).roast(results, context)
    
    # Check for Anthropic API key
    if anthropic_key := os.getenv("ANTHROPIC_API_KEY"):
        return AnthropicProvider(anthropic_key).roast(results, context)
    
    return None


def _static_roast(results: List[ShitLintResult], context: str) -> str:
    """Static roasting fallback."""
    violations_text = format_violations(results)
    
    return f"""
🔥 ARCHITECTURAL ROAST SESSION (Static Fallback)

Context: {context or 'Your beautiful disaster'}

{violations_text}

DOCTRINE ANALYSIS:
- Clarity over cleverness: Your code chose cleverness, lost clarity
- Simplicity over sophistication: You built a Rube Goldberg machine
- Directness over indirection: More layers than a wedding cake

VERDICT: Your architecture needs therapy.

Next steps:
1. Delete half of this
2. Simplify the other half  
3. Question your life choices
4. Repeat until maintainable

💡 Tip: Set GEMINI_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY for brutal LLM roasting
"""