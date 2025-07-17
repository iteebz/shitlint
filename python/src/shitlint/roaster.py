"""Simple roaster - no agent ceremony, just LLM roasting."""

from typing import List
from .core import ShitLintResult


def format_violations(results: List[ShitLintResult]) -> str:
    """Format violations for LLM consumption."""
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
    """Generate architectural roast. For now, just format violations."""
    
    if not results:
        return f"""
🤨 SUSPICIOUSLY CLEAN CODE DETECTED

Either you're a fucking architectural genius, or you're hiding the bodies.

Context: {context or 'Unknown codebase'}

Possible explanations:
1. You actually know what you're doing (unlikely)
2. The code is too simple to fuck up (boring)
3. You haven't written enough code yet (give it time)
4. Our detection rules suck (probable)

Recommendation: Write more code, then come back for proper roasting.
"""
    
    violations_text = format_violations(results)
    
    return f"""
🔥 ARCHITECTURAL ROAST SESSION

Context: {context or 'Your beautiful disaster'}

{violations_text}

DOCTRINE ANALYSIS:
- Clarity over cleverness: Your code chose cleverness, lost clarity
- Simplicity over sophistication: You built a Rube Goldberg machine
- Directness over indirection: More layers than a wedding cake

VERDICT: Your architecture needs therapy.

Next steps:
1. Delete half of this shit
2. Simplify the other half  
3. Question your life choices
4. Repeat until maintainable

TODO: Add actual LLM integration here (users provide their own keys)
"""