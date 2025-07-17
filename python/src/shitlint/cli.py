"""ShitLint CLI - Your code is shit. Here's why."""

import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from dotenv import load_dotenv

from .core import analyze_code, get_analysis_context
from .roaster import generate_roast

# Load .env file for API keys
load_dotenv()

console = Console()


@click.command()
@click.argument('path', type=click.Path(exists=True), default='.')
@click.option('--context', help='Additional context about the codebase')
def main(path: str, context: str):
    """ShitLint: Brutally honest code analysis. Usage: shitlint ."""
    path_obj = Path(path)
    
    # Get analysis context for file count warning
    analysis_context = get_analysis_context(path_obj)
    
    # Warning for large directories
    if analysis_context.file_count > 50:
        console.print(f"⚠️  About to roast {analysis_context.file_count} Python files. This will cost API credits.", style="yellow")
        if not click.confirm("Continue?"):
            console.print("Aborted.", style="red")
            return
    
    console.print("🔥 Analyzing architectural disasters...")
    
    try:
        with console.status("[bold green]Detecting violations..."):
            results = analyze_code(path_obj)
        
        with console.status("[bold red]Generating roast..."):
            roast_content = generate_roast(results, context or "", analysis_context)
        
        console.print(Panel(
            f"\n{roast_content}\n",
            title="ARCHITECTURAL ROAST SESSION",
            style="white",
            expand=True
        ))
        
    except Exception as e:
        console.print(f"❌ Roasting failed: {e}", style="red")




if __name__ == '__main__':
    main()