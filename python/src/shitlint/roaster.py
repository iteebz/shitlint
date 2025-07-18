"""Clean roaster - no ceremony, proper separation."""

import os
import json
from typing import List, Optional
from .core import ShitLintResult, AnalysisContext
from .llm import OpenAIProvider, AnthropicProvider, GeminiProvider


def format_violations(results: List[ShitLintResult]) -> str:
    """Format violations for display."""
    if not results:
        return "No violations found. Suspiciously clean code... 🤔"
    
    output = [f"🚨 VIOLATIONS DETECTED ({len(results)} issues)", ""]
    
    severity_groups = _group_by_severity(results)
    for severity_data in severity_groups:
        if severity_data["violations"]:
            output.extend(_format_severity_section(severity_data))
    
    return "\n".join(output)


def _group_by_severity(results: List[ShitLintResult]) -> List[dict]:
    """Group violations by severity with display metadata."""
    return [
        {"name": "💀 BRUTAL VIOLATIONS:", "violations": [r for r in results if r.severity == "brutal"]},
        {"name": "⚠️  MODERATE VIOLATIONS:", "violations": [r for r in results if r.severity == "moderate"]},
        {"name": "👀 GENTLE VIOLATIONS:", "violations": [r for r in results if r.severity == "gentle"]}
    ]


def _format_severity_section(severity_data: dict) -> List[str]:
    """Format a section for one severity level."""
    section = [severity_data["name"]]
    for result in severity_data["violations"]:
        section.append(f"  - {result.file_path}:{result.line_number or '?'} - {result.message}")
    section.append("")
    return section


def generate_roast(results: List[ShitLintResult], context: str = "", analysis_context: Optional[AnalysisContext] = None, config=None) -> str:
    """Generate brutal architectural roast via LLM."""
    
    if not results:
        return _clean_code_response(context)
    
    # Try LLM first, fallback to static
    if llm_roast := _try_llm_roast(results, context, analysis_context, config):
        return llm_roast
    
    # Static fallback
    return _static_roast(results, context, analysis_context)


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


def _try_llm_roast(results: List[ShitLintResult], context: str, analysis_context: Optional[AnalysisContext] = None, config=None) -> Optional[str]:
    """Try LLM roasting with user-provided API keys."""
    provider_preference = config.llm_provider if config else "auto"
    
    if provider_preference != "auto":
        return _try_specific_provider(provider_preference, results, context, analysis_context)
    
    return _try_auto_provider(results, context, analysis_context)


def _try_specific_provider(provider: str, results: List[ShitLintResult], context: str, analysis_context: Optional[AnalysisContext]) -> Optional[str]:
    """Try specific LLM provider."""
    providers = {
        "gemini": (GeminiProvider, "GEMINI_API_KEY"),
        "openai": (OpenAIProvider, "OPENAI_API_KEY"), 
        "anthropic": (AnthropicProvider, "ANTHROPIC_API_KEY")
    }
    
    if provider in providers:
        provider_class, env_var = providers[provider]
        if api_key := os.getenv(env_var):
            return provider_class(api_key).roast(results, context, analysis_context)
    
    return None


def _try_auto_provider(results: List[ShitLintResult], context: str, analysis_context: Optional[AnalysisContext]) -> Optional[str]:
    """Auto-detect provider (cheapest first)."""
    for provider_class, env_var in [
        (GeminiProvider, "GEMINI_API_KEY"),
        (OpenAIProvider, "OPENAI_API_KEY"),
        (AnthropicProvider, "ANTHROPIC_API_KEY")
    ]:
        if api_key := os.getenv(env_var):
            return provider_class(api_key).roast(results, context, analysis_context)
    
    return None


def _static_roast(results: List[ShitLintResult], context: str, analysis_context: Optional[AnalysisContext] = None) -> str:
    """Static roasting fallback."""
    violations_text = format_violations(results)
    
    tree_info = ""
    if analysis_context:
        tree_info = f"\n📁 Structure: {analysis_context.file_count} files, {len(analysis_context.file_types)} types"
        if analysis_context.naming_violations:
            tree_info += f"\n🔤 Naming violations: {', '.join(analysis_context.naming_violations[:3])}"
    
    return f"""
🔥 ARCHITECTURAL ROAST SESSION (Static Fallback)

Context: {context or 'Your beautiful disaster'}{tree_info}

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