"""ShitLint CLI - Your code is shit. Here's why."""

import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .core import analyze_code
from .roaster import generate_roast

console = Console()


@click.group()
@click.version_option()
def main():
    """ShitLint: Brutally honest code analysis."""
    pass


@main.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--brutal', is_flag=True, help='Extra brutal mode (not for sensitive developers)')
@click.option('--watch', is_flag=True, help='Watch for changes and roast in real-time')
def analyze(path: str, brutal: bool, watch: bool):
    """Analyze code for architectural bullshit."""
    if watch:
        console.print("👀 Watching for changes... (Ctrl+C to stop)")
        # TODO: Implement watch mode
        return
    
    console.print(f"🔍 Analyzing: {path}")
    
    results = analyze_code(Path(path))
    
    if not results:
        console.print(Panel(
            "No violations found. Suspiciously clean... 🤔",
            title="Analysis Complete",
            style="green"
        ))
        return
    
    # Display results
    for result in results:
        severity_colors = {
            "brutal": "red",
            "moderate": "yellow", 
            "gentle": "blue"
        }
        
        color = severity_colors.get(result.severity, "white")
        
        console.print(Panel(
            f"{result.message}\n\nFile: {result.file_path}\nLine: {result.line_number or 'Unknown'}",
            title=f"{result.severity.upper()} VIOLATION",
            style=color
        ))


@main.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--context', help='Additional context about the codebase')
def roast(path: str, context: str):
    """Roast your codebase with architectural doctrine."""
    console.print("🔥 Analyzing architectural disasters...")
    
    try:
        with console.status("[bold green]Detecting violations..."):
            results = analyze_code(Path(path))
        
        with console.status("[bold red]Generating roast..."):
            roast_content = generate_roast(results, context or "")
        
        console.print(Panel(
            roast_content,
            title="🔥 ARCHITECTURAL ROAST SESSION",
            style="red"
        ))
        
    except Exception as e:
        console.print(f"❌ Roasting failed: {e}", style="red")


@main.command()
def self_roast():
    """The meta moment: ShitLint analyzes itself."""
    console.print("🪞 Time for some self-reflection...")
    console.print("🔥 ShitLint roasting its own codebase\n")
    
    try:
        with console.status("[bold yellow]Discovering our own architectural sins..."):
            results = analyze_code(Path("./src/shitlint"))
        
        with console.status("[bold magenta]Generating self-roast..."):
            roast_content = generate_roast(results, "ShitLint's own codebase - time for brutal honesty")
        
        console.print(Panel(
            roast_content,
            title="🔥 SELF-ROAST: DISCOVERING OUR OWN BULLSHIT",
            style="magenta"
        ))
        
    except Exception as e:
        console.print(f"❌ Self-roasting failed: {e}", style="red")


@main.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
def compare(paths):
    """Compare architectural quality across multiple codebases."""
    if len(paths) < 2:
        console.print("❌ Need at least 2 paths to compare", style="red")
        return
    
    console.print("🥊 CODEBASE BATTLE ROYALE\n")
    
    try:
        results = {}
        for path in paths:
            console.print(f"🔍 Analyzing {path}...")
            with console.status(f"[bold blue]Roasting {path}..."):
                violations = analyze_code(Path(path))
                roast = generate_roast(violations, f"Part of comparison analysis")
            results[path] = roast
        
        # Simple comparison output
        comparison = "🏆 ARCHITECTURAL BATTLE RESULTS\n\n"
        for i, (path, roast) in enumerate(results.items(), 1):
            comparison += f"=== #{i}: {path} ===\n{roast}\n\n"
        
        comparison += "TODO: Add LLM-based comparison ranking here"
        
        console.print(Panel(
            comparison,
            title="🏆 ARCHITECTURAL BATTLE RESULTS",
            style="cyan"
        ))
        
    except Exception as e:
        console.print(f"❌ Comparison failed: {e}", style="red")


if __name__ == '__main__':
    main()