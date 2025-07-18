"""Duplicate code detection - single file and cross-file."""

from pathlib import Path
from typing import List, Dict
import ast
import hashlib

from .base import Violation


def detect_duplicate_blocks(file_path: Path, content: str, tree: ast.AST, thresholds: Dict) -> List[Violation]:
    """Detect copy-paste violations within a single file."""
    # Skip if not a Python file
    if tree is None:
        return []
    
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_hash = hashlib.md5(ast.dump(node).encode()).hexdigest()
            functions.append((node.name, node.lineno, func_hash))
    
    # Find duplicates
    hash_counts = {}
    for name, line, func_hash in functions:
        if func_hash not in hash_counts:
            hash_counts[func_hash] = []
        hash_counts[func_hash].append((name, line))
    
    violations = []
    for func_hash, occurrences in hash_counts.items():
        if len(occurrences) > 1:
            names = [name for name, line in occurrences]
            lines = [line for name, line in occurrences]
            
            violations.append(Violation(
                rule="duplicate_code",
                file_path=str(file_path),
                line_number=min(lines),
                severity="moderate",
                message=f"Copy-paste detected: {', '.join(names)} are identical",
                context={"duplicates": occurrences}
            ))
    
    return violations


class CrossFileAnalyzer:
    """Analyzes structural similarity across multiple files."""
    
    def __init__(self):
        self._function_fingerprints = {}  # signature -> [(file_path, func_name, line_no)]
    
    def collect_function_fingerprints(self, file_path: Path, tree: ast.AST):
        """Collect function structural fingerprints."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip tiny functions
                if len(node.body) < 3:
                    continue
                    
                fingerprint = self._normalize_function_structure(node)
                
                if fingerprint not in self._function_fingerprints:
                    self._function_fingerprints[fingerprint] = []
                
                self._function_fingerprints[fingerprint].append((
                    str(file_path), 
                    node.name, 
                    node.lineno
                ))
    
    def _normalize_function_structure(self, node: ast.FunctionDef) -> str:
        """Extract structural fingerprint, ignoring variable names."""
        
        class StructureNormalizer(ast.NodeTransformer):
            def __init__(self):
                self.var_counter = 0
                self.var_map = {}
            
            def visit_Name(self, node):
                if node.id not in self.var_map:
                    self.var_map[node.id] = f"VAR_{self.var_counter}"
                    self.var_counter += 1
                node.id = self.var_map[node.id]
                return node
            
            def visit_arg(self, node):
                if node.arg not in self.var_map:
                    self.var_map[node.arg] = f"PARAM_{len(self.var_map)}"
                node.arg = self.var_map[node.arg]
                return node
        
        # Clone and normalize
        normalized = StructureNormalizer().visit(ast.copy_location(
            ast.FunctionDef(
                name="FUNC",
                args=node.args,
                body=node.body,
                decorator_list=[],
                returns=None,
                type_comment=None
            ), node
        ))
        
        return hashlib.md5(ast.dump(normalized, annotate_fields=False).encode()).hexdigest()
    
    def get_violations(self) -> List[Violation]:
        """Generate violations for cross-file duplicates."""
        violations = []
        
        for fingerprint, occurrences in self._function_fingerprints.items():
            if len(occurrences) > 1:
                # Only flag cross-file duplicates
                files = set(file_path for file_path, _, _ in occurrences)
                if len(files) > 1:
                    file_names = [Path(fp).name for fp, _, _ in occurrences]
                    
                    for file_path, func_name, line_no in occurrences:
                        violations.append(Violation(
                            rule="cross_file_duplicate",
                            file_path=file_path,
                            line_number=line_no,
                            severity="moderate",
                            message=f"Function '{func_name}' duplicated across files: {', '.join(file_names)}",
                            context={
                                "duplicates": occurrences,
                                "fingerprint": fingerprint[:8]
                            }
                        ))
        
        return violations