"""Rule engine for coordinating all violation detection."""

from pathlib import Path
from typing import List, Dict
import ast

from .base import Violation
from .file_rules import detect_giant_files
from .import_rules import detect_import_ceremony
from .function_rules import detect_complex_functions, detect_parameter_hell
from .naming_rules import detect_naming_violations
from .duplicate_rules import detect_duplicate_blocks, CrossFileAnalyzer
from .magic_rules import detect_magic_numbers
from .abstraction_rules import detect_over_abstraction


class RuleEngine:
    """Apply deterministic rules to detect code violations."""
    
    def __init__(self, brutality: str = "professional"):
        self.brutality = brutality
        self.thresholds = self._get_brutality_thresholds(brutality)
        self.cross_file_analyzer = CrossFileAnalyzer()
        
        # File-level rules
        self.rules = [
            detect_giant_files,
            detect_import_ceremony, 
            detect_duplicate_blocks,
            detect_complex_functions,
            detect_parameter_hell,
            detect_naming_violations,
            detect_magic_numbers,
            detect_over_abstraction,
        ]
    
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
            tree = ast.parse(content)
            
            # Collect for cross-file analysis
            self.cross_file_analyzer.collect_function_fingerprints(file_path, tree)
            
            # Run all rules
            for rule in self.rules:
                violations.extend(rule(file_path, content, tree, self.thresholds))
                
        except (SyntaxError, UnicodeDecodeError):
            pass
            
        return violations
    
    def get_cross_file_violations(self) -> List[Violation]:
        """Generate violations for cross-file duplicates."""
        return self.cross_file_analyzer.get_violations()