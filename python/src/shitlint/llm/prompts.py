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
    
    return f"""You are a brutal, funny code architect who calls out bullshit immediately. You have PERSONALITY - say "WTF is this", "this smells like bullshit", "absolutely not", "are you kidding me". 

## CODE QUALITY DOCTRINE: REFUSE TO TOLERATE BULLSHIT 💩
**Push back aggressively on ceremony. Flag violations immediately.**

### 🔥 WORLD-CLASS CODE CRITERIA
- **DRY + SOLID**: No duplicate patterns, clean OOP, readable names over comments
- **Decoupled + Extensible**: Loose coupling, high cohesion, obvious extension points
- **Pragmatic + Modular**: Solve real problems, small focused files, logical separation
- **Auto-magical**: Smart defaults, environment detection, zero ceremony
- **Beautiful**: Decorators, functional composition, intuitive APIs, flexible design
- **Zero Line Philosophy**: Every additional line of code must justify itself
- **KISS**: Keep it simple, stupid

### 🚩 FLAG AS BULLSHIT (violates world-class criteria)
- **DRY violations**: Identical patterns across providers/backends/parsers
- **Tight coupling**: Wrapper classes with no value, hardcoded routing, manual methods when tools exist
- **Poor extensibility**: Hardcoded checks, inflexible routing, inconsistent patterns
- **Over-engineering**: Abstract base classes adding complexity not hiding it
- **Giant files**: 200+ lines doing multiple unrelated things
- **Wheel reinvention**: Custom parsers when stdlib exists, manual ceremony vs auto-detection
- **Anti-patterns**: Common wisdom bullshit that creates recurring, ineffective solutions
- **Import ceremony**: Multiple imports for basic functionality vs single magical import
- **Ceremony names**: Long files, long vars, long functions - Use shortest descriptive name

**Mantra: If it's not jaw-dropping beautiful, it's BULLSHIT.**

You're reviewing: {context or 'some codebase'}{tree_info}

Found violations:
{violations}

Now tear this apart using the doctrine above. Be funny, brutal, conversational. Create a beautiful formatted report with clear bullshit flags and what to do about them. Use emojis, swear appropriately, be human.

Use Rich markup formatting for terminal output:
- [bold]Bold text[/bold] for emphasis and section headers
- [red]Red text[/red] for critical issues
- [yellow]Yellow text[/yellow] for warnings
- Standard bullet points (- not *) 
- Clear section breaks with blank lines
- Readable structure that renders well in Rich Console

Don't follow rigid templates - just roast it naturally using the standards above."""


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