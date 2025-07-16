"""ShitLint CLI - Your code is shit. Here's why."""

import click
from pathlib import Path
from rich.console import Console
from rich.text import Text

from .core import analyze_code


console = Console()


@click.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.option("--brutal", is_flag=True, help="Extra brutal mode")
def main(path: Path, brutal: bool) -> None:
    """Your code is shit. Here's why."""
    
    console.print(Text("🔍 SHITLINT ANALYSIS", style="bold red"))
    console.print(Text("Your code is shit. Here's why.\n", style="italic"))
    
    results = analyze_code(path)
    
    if not results:
        console.print(Text("✅ No giant files found. Your code doesn't completely suck.", style="green"))
        return
    
    for result in results:
        # Choose emoji and color based on severity
        if result.severity == "brutal":
            emoji, style = "💀", "bold red"
        elif result.severity == "moderate":
            emoji, style = "⚠️", "yellow"
        else:
            emoji, style = "🟡", "dim yellow"
        
        console.print(f"{emoji} {result.message}", style=style)
        console.print(f"   📁 {result.file_path}")
        if result.line_number:
            console.print(f"   📊 Line: {result.line_number}")
        if result.rule:
            console.print(f"   🔍 Rule: {result.rule}\n")
    
    # Summary stats
    brutal_count = sum(1 for r in results if r.severity == "brutal")
    moderate_count = sum(1 for r in results if r.severity == "moderate")
    
    console.print(Text(f"\n📈 DAMAGE REPORT:", style="bold"))
    console.print(f"   💀 War crimes: {brutal_count}")
    console.print(f"   ⚠️  Novellas: {moderate_count}")
    console.print(f"   🟡 Chubby files: {len(results) - brutal_count - moderate_count}")
    
    if brutal_count > 0:
        console.print(Text("\nVERDICT: Your code looks like it was written during an earthquake", style="bold red"))
    elif moderate_count > 0:
        console.print(Text("\nVERDICT: Your code needs some architectural liposuction", style="yellow"))
    else:
        console.print(Text("\nVERDICT: Minor bloat detected. Time for a code diet.", style="dim yellow"))


if __name__ == "__main__":
    main()