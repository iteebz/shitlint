"""Configuration management for ShitLint."""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ShitLintConfig:
    """ShitLint configuration."""
    
    brutality: str = "professional"  # brutal, professional, gentle
    ignore_patterns: List[str] = None
    max_file_size: int = 100000  # Skip files larger than this
    llm_provider: str = "auto"  # auto, gemini, openai, anthropic
    custom_rules: Dict[str, Any] = None
    enabled_rules: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.ignore_patterns is None:
            self.ignore_patterns = []
        if self.custom_rules is None:
            self.custom_rules = {}
        if self.enabled_rules is None:
            self.enabled_rules = {}


def load_config(project_root: Path) -> ShitLintConfig:
    """Load configuration from .shitlint/config.json."""
    config_path = project_root / ".shitlint" / "config.json"
    
    if not config_path.exists():
        return ShitLintConfig()
    
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        return ShitLintConfig(
            brutality=data.get("brutality", "professional"),
            ignore_patterns=data.get("ignore_patterns", []),
            max_file_size=data.get("max_file_size", 100000),
            llm_provider=data.get("llm_provider", "auto"),
            custom_rules=data.get("custom_rules", {}),
            enabled_rules=data.get("enabled_rules", {})
        )
    except (json.JSONDecodeError, FileNotFoundError):
        return ShitLintConfig()


def create_default_config(project_root: Path) -> None:
    """Create default .shitlint/config.json."""
    config_dir = project_root / ".shitlint"
    config_dir.mkdir(exist_ok=True)
    
    config_path = config_dir / "config.json"
    
    default_config = {
        "brutality": "professional",
        "ignore_patterns": [
            "tests/",
            "test_*.py",
            "*_test.py",
            ".venv/",
            "node_modules/",
            "dist/",
            "build/"
        ],
        "max_file_size": 100000,
        "llm_provider": "auto",
        "custom_rules": {}
    }
    
    with open(config_path, 'w') as f:
        json.dump(default_config, f, indent=2)