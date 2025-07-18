"""ShitLint CLI - Your code is shit. Here's why."""

import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from dotenv import load_dotenv

from .core import analyze_code, get_analysis_context
from .roaster import generate_roast
from .config import load_config, create_default_config
from .review import review_design

# Load .env file for API keys
load_dotenv()

console = Console()


@click.group()
def cli():
    """ShitLint: Brutally honest code analysis."""
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True), default='.')
@click.option('--context', help='Additional context about the codebase')
@click.option('--init', is_flag=True, help='Create default .shitlint/config.json')
@click.option('--brutality', type=click.Choice(['brutal', 'professional', 'gentle']), help='Override brutality level')
def main(path: str, context: str, init: bool, brutality: str):
    """ShitLint: Brutally honest code analysis. Usage: shitlint ."""
    path_obj = Path(path)
    
    # Handle config init
    if init:
        create_default_config(path_obj)
        console.print("✅ Created .shitlint/config.json", style="green")
        return
    
    # Load configuration
    config = load_config(path_obj)
    if brutality:
        config.brutality = brutality
    
    # Get analysis context for file count warning
    analysis_context = get_analysis_context(path_obj, config)
    
    # Warning for large directories
    if analysis_context.file_count > 50:
        console.print(f"⚠️  About to roast {analysis_context.file_count} Python files. This will cost API credits.", style="yellow")
        if not click.confirm("Continue?"):
            console.print("Aborted.", style="red")
            return
    
    console.print("🔥 Analyzing architectural disasters...")
    
    try:
        with console.status("[bold green]Detecting violations..."):
            results = analyze_code(path_obj, config)
        
        with console.status("[bold red]Generating roast..."):
            roast_content = generate_roast(results, context or "", analysis_context, config)
        
        console.print(Panel(
            f"\n{roast_content}\n",
            title="ARCHITECTURAL ROAST SESSION",
            style="white",
            expand=True
        ))
        
    except Exception as e:
        console.print(f"❌ Roasting failed: {e}", style="red")


@cli.command()
@click.option('--proposal', help='Design proposal text')
@click.option('--context', help='team=2,users=47,perf=120ms')
@click.argument('file', type=click.Path(exists=True), required=False)
def review(proposal: str, context: str, file: str):
    """Adversarial design review using CLAUDE.md doctrine."""
    
    if file:
        content = Path(file).read_text()
    elif proposal:
        content = proposal
    else:
        console.print("❌ Provide either --proposal text or a file path", style="red")
        return
    
    console.print("🔥 Applying CLAUDE.md doctrine...")
    
    try:
        with console.status("[bold red]Generating brutal assessment..."):
            assessment = review_design(content, context)
        
        console.print(Panel(
            f"\n{assessment}\n",
            title="DESIGN REVIEW",
            style="white",
            expand=True
        ))
        
    except Exception as e:
        console.print(f"❌ Review failed: {e}", style="red")


if __name__ == '__main__':
    cli()