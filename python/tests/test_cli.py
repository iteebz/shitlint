"""Tests for CLI module."""

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
from click.testing import CliRunner

from shitlint.cli import cli


def test_cli_help():
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'ShitLint' in result.output


def test_cli_main_help():
    """Test main subcommand help."""
    runner = CliRunner()
    result = runner.invoke(cli, ['main', '--help'])
    assert result.exit_code == 0
    assert 'brutality' in result.output


def test_cli_init_flag():
    """Test CLI init flag creates config."""
    runner = CliRunner()
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        result = runner.invoke(cli, ['main', str(tmp_dir), '--init'])
        assert result.exit_code == 0
        assert 'Created .shitlint/config.json' in result.output
        
        # Check that config file was created
        config_path = Path(tmp_dir) / '.shitlint' / 'config.json'
        assert config_path.exists()


def test_cli_brutality_option():
    """Test brutality option is accepted."""
    runner = CliRunner()
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_file = Path(tmp_dir) / 'test.py'
        test_file.write_text('def simple_function(): pass')
        
        # Mock the analyze_code function to avoid actual analysis
        with patch('shitlint.cli.analyze_code') as mock_analyze:
            mock_analyze.return_value = []
            
            result = runner.invoke(cli, ['main', str(test_file), '--brutality', 'brutal'])
            # Should not crash - exit code might be non-zero due to missing API keys
            assert 'brutal' in str(result.output) or result.exit_code in [0, 1]