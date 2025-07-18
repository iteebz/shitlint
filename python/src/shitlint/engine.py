"""Rule engine for coordinating all violation detection."""

from pathlib import Path
from typing import List, Dict
import ast

from .rules.base import Violation
from .rules.files import detect_giant_files
from .rules.imports import detect_import_ceremony
from .rules.functions import detect_complex_functions, detect_parameter_hell
from .rules.naming import detect_naming_violations
from .rules.duplicates import detect_duplicate_blocks, CrossFileAnalyzer
from .rules.magic import detect_magic_numbers
from .rules.abstraction import detect_over_abstraction
from .rules.commits import detect_commit_violations
from .rules.deps import detect_dependency_violations
from .rules.docs import detect_documentation_violations


class RuleEngine:
    """Apply deterministic rules to detect code violations."""
    
    def __init__(self, brutality: str = "professional", config: Dict = None):
        self.brutality = brutality
        self.thresholds = self._get_brutality_thresholds(brutality)
        self.cross_file_analyzer = CrossFileAnalyzer()
        
        # All available rules
        all_rules = {
            "giant_files": detect_giant_files,
            "import_ceremony": detect_import_ceremony,
            "duplicate_blocks": detect_duplicate_blocks,
            "complex_functions": detect_complex_functions,
            "parameter_hell": detect_parameter_hell,
            "naming_violations": detect_naming_violations,
            "magic_numbers": detect_magic_numbers,
            "over_abstraction": detect_over_abstraction,
            "commit_violations": detect_commit_violations,
            "dependency_violations": detect_dependency_violations,
            "documentation_violations": detect_documentation_violations,
        }
        
        # Filter rules based on config
        if config and "enabled_rules" in config:
            enabled = config["enabled_rules"]
            self.rules = [rule for name, rule in all_rules.items() if enabled.get(name, True)]
        else:
            self.rules = list(all_rules.values())
    
    def _get_brutality_thresholds(self, brutality: str) -> Dict:
        """Get detection thresholds based on brutality level."""
        if brutality == "brutal":
            return {
                "file_lines": {"gentle": 150, "moderate": 200, "brutal": 300},
                "imports": {"moderate": 10, "brutal": 15},
                "complexity": {"moderate": 8, "brutal": 12},
                "function_lines": {"moderate": 30, "brutal": 50},
                "parameters": {"moderate": 3, "brutal": 5},
                "name_length": 20,
                "enable_loop_var_check": True
            }
        elif brutality == "gentle":
            return {
                "file_lines": {"gentle": 300, "moderate": 500, "brutal": 800},
                "imports": {"moderate": 20, "brutal": 35},
                "complexity": {"moderate": 15, "brutal": 25},
                "function_lines": {"moderate": 80, "brutal": 120},
                "parameters": {"moderate": 6, "brutal": 8},
                "name_length": 35,
                "enable_loop_var_check": False
            }
        else:  # professional (default)
            return {
                "file_lines": {"gentle": 200, "moderate": 300, "brutal": 500},
                "imports": {"moderate": 15, "brutal": 25},
                "complexity": {"moderate": 10, "brutal": 15},
                "function_lines": {"moderate": 50, "brutal": 80},
                "parameters": {"moderate": 4, "brutal": 6},
                "name_length": 25,
                "enable_loop_var_check": False
            }
    
    def analyze_file(self, file_path: Path) -> List[Violation]:
        """Run all rules against a file."""
        violations = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = None
            
            # Only parse Python files with AST
            if file_path.suffix == '.py':
                try:
                    tree = ast.parse(content)
                    # Collect for cross-file analysis
                    self.cross_file_analyzer.collect_function_fingerprints(file_path, tree)
                except SyntaxError:
                    pass
            
            # Run all rules
            for rule in self.rules:
                violations.extend(rule(file_path, content, tree, self.thresholds))
                
        except UnicodeDecodeError:
            pass
            
        return violations
    
    def get_cross_file_violations(self) -> List[Violation]:
        """Generate violations for cross-file duplicates."""
        return self.cross_file_analyzer.get_violations()