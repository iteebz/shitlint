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
    
    for result in results:
        console.print(f"🚨 {result.message}", style="red")
        console.print(f"   📁 {result.file_path}\n")
    
    if brutal:
        console.print(Text("VERDICT: Your code looks like it was written during an earthquake", style="bold red"))
    else:
        console.print(Text("VERDICT: Your code needs work", style="yellow"))


if __name__ == "__main__":
    main()