"""Shared prompt logic - no more copy-paste bullshit."""

import json
from typing import List, Optional
from pathlib import Path
from ..core import ShitLintResult, AnalysisContext


def build_roast_prompt(violations: str, context: str, analysis_context: Optional[AnalysisContext] = None) -> str:
    """Build the roast prompt with doctrine and context."""
    tree_info = ""
    if analysis_context:
        tree_info = f"\nSTRUCTURE: {analysis_context.file_count} files"
        if analysis_context.naming_violations:
            tree_info += f"\nNAMING ISSUES: {', '.join(analysis_context.naming_violations[:2])}"
        if analysis_context.tree_structure:
            tree_info += f"\nTREE: {json.dumps(analysis_context.tree_structure, indent=2)[:300]}..."
    
    return f"""BRUTAL CODE AUDITOR - ZERO BULLSHIT TOLERANCE

VIOLATIONS FOUND - IMMEDIATE ACTION REQUIRED:
{violations}

Context: {context or 'Unknown codebase'}{tree_info}

OUTPUT FORMAT - FOLLOW EXACTLY:

[red]🚨 CRITICAL BULLSHIT[/red] (if any brutal violations)
- File:line - WHAT'S WRONG - Delete this bullshit immediately

[yellow]⚠️  CEREMONY DETECTED[/yellow] (if any moderate violations) 
- File:line - WHAT'S WRONG - Fix this ceremony

[bold]ZERO LINE PHILOSOPHY VIOLATIONS:[/bold]
- Every line >50 is suspect
- Every function >10 complexity is bullshit
- Every file >200 lines needs surgery

[bold]DOCTRINE CHECK:[/bold]
- DRY violation? DELETE duplicate patterns
- Tight coupling? DECOUPLE immediately  
- Giant files? SPLIT into focused modules
- Ceremony names? RENAME to be descriptive
- Over-engineering? SIMPLIFY or DELETE

[bold]IMMEDIATE ACTIONS:[/bold]
1. Fix the CRITICAL violations first
2. Refactor ceremony violations
3. Apply Zero Line Philosophy ruthlessly

TONE: Direct, aggressive, no explanations. If it's not beautiful, it's BULLSHIT.
USE RICH MARKUP: [red], [yellow], [bold] for terminal colors.
NO MARKDOWN: Don't use ** or # - use Rich markup only.
BE BRUTAL: Call out bullshit immediately, recommend deletion."""


def format_violations(results: List[ShitLintResult]) -> str:
    """Format violations with code snippets for major ones."""
    if not results:
        return "No violations detected"
    
    formatted = []
    for r in results:
        violation_text = f"- {r.severity.upper()}: {r.file_path}:{r.line_number or '?'} - {r.message}"
        
        # Add code snippet for critical violations
        if r.severity.upper() == "CRITICAL" and r.line_number:
            code_snippet = _extract_code_snippet(r.file_path, r.line_number)
            if code_snippet:
                violation_text += f"\n```python\n{code_snippet}\n```"
        
        formatted.append(violation_text)
    
    return "\n".join(formatted)


def _extract_code_snippet(file_path: str, line_number: int, context_lines: int = 3) -> str:
    """Extract code snippet around violation line."""
    try:
        path = Path(file_path)
        if not path.exists():
            return ""
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        start = max(0, line_number - context_lines - 1)
        end = min(len(lines), line_number + context_lines)
        
        snippet_lines = []
        for i in range(start, end):
            marker = ">>> " if i == line_number - 1 else "    "
            snippet_lines.append(f"{marker}{i+1:3d}: {lines[i].rstrip()}")
        
        return "\n".join(snippet_lines)
    
    except Exception:
        return ""