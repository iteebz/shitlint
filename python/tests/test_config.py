"""Tests for config module."""

import tempfile
from pathlib import Path
import pytest

from shitlint.config import ShitLintConfig, load_config


def test_shitlint_config_initialization():
    """Test ShitLintConfig initialization."""
    config = ShitLintConfig()
    assert config.brutality == "professional"
    assert config.ignore_patterns == []
    assert config.max_file_size == 100000


def test_shitlint_config_custom_brutality():
    """Test ShitLintConfig with custom brutality."""
    config = ShitLintConfig(brutality="brutal")
    assert config.brutality == "brutal"


def test_load_config_from_file():
    """Test loading config from file."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_dir = Path(tmp_dir) / '.shitlint'
        config_dir.mkdir()
        config_file = config_dir / 'config.json'
        config_file.write_text('''
{
  "brutality": "brutal",
  "ignore_patterns": ["*.generated.py", "migrations/"]
}
''')
        
        config = load_config(Path(tmp_dir))
        assert config.brutality == "brutal"
        assert "*.generated.py" in config.ignore_patterns


def test_load_config_nonexistent_file():
    """Test loading config from non-existent directory."""
    config = load_config(Path("/nonexistent/"))
    assert config.brutality == "professional"  # default value


def test_config_validation():
    """Test config validation."""
    # Valid brutality levels
    for brutality in ["gentle", "professional", "moderate", "brutal"]:
        config = ShitLintConfig(brutality=brutality)
        assert config.brutality == brutality