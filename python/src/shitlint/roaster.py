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
    """Static roasting fallback - BRUTAL and scannable."""
    
    # Group violations by severity
    brutal = [r for r in results if r.severity == "brutal"]
    moderate = [r for r in results if r.severity == "moderate"]
    gentle = [r for r in results if r.severity == "gentle"]
    
    output = ["🚨 BULLSHIT DETECTED - IMMEDIATE ACTION REQUIRED", ""]
    
    # Critical violations first
    if brutal:
        output.append("🔥 CRITICAL BULLSHIT:")
        for r in brutal:
            output.append(f"- {r.file_path}:{r.line_number or '?'} - {r.message} - DELETE THIS")
        output.append("")
    
    # Moderate violations 
    if moderate:
        output.append("⚠️  CEREMONY DETECTED:")
        for r in moderate:
            output.append(f"- {r.file_path}:{r.line_number or '?'} - {r.message} - FIX THIS")
        output.append("")
    
    # Gentle violations
    if gentle:
        output.append("👀 IMPROVEMENT NEEDED:")
        for r in gentle:
            output.append(f"- {r.file_path}:{r.line_number or '?'} - {r.message} - REFACTOR")
        output.append("")
    
    # Quick context
    if analysis_context:
        output.append(f"📁 Context: {context} ({analysis_context.file_count} files)")
        if analysis_context.naming_violations:
            output.append(f"🔤 Naming: {', '.join(analysis_context.naming_violations[:2])}")
        output.append("")
    
    # Actions
    output.extend([
        "IMMEDIATE ACTIONS:",
        "1. Fix CRITICAL violations first",  
        "2. Eliminate ceremony",
        "3. Apply Zero Line Philosophy",
        "",
        "💡 Set GEMINI_API_KEY for brutal LLM roasting"
    ])
    
    return "\n".join(output)