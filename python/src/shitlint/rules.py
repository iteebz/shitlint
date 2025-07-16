"""Deterministic code violation detection rules."""

from pathlib import Path
from typing import List, Dict, Set
from dataclasses import dataclass
import ast
import hashlib


@dataclass
class Violation:
    """A detected code violation."""
    rule: str
    file_path: str
    line_number: int
    severity: str
    message: str
    context: Dict = None


class RuleEngine:
    """Apply deterministic rules to detect code violations."""
    
    def __init__(self):
        self.rules = [
            self._detect_giant_files,
            self._detect_import_ceremony,
            self._detect_duplicate_blocks,
            self._detect_complex_functions,
        ]
    
    def analyze_file(self, file_path: Path) -> List[Violation]:
        """Run all rules against a file."""
        violations = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content)
            
            for rule in self.rules:
                violations.extend(rule(file_path, content, tree))
                
        except (SyntaxError, UnicodeDecodeError):
            # Skip files that can't be parsed
            pass
            
        return violations
    
    def _detect_giant_files(self, file_path: Path, content: str, tree: ast.AST) -> List[Violation]:
        """Detect files that are too damn long."""
        lines = [line for line in content.split('\n') if line.strip()]
        line_count = len(lines)
        
        if line_count < 200:
            return []
        
        if line_count >= 500:
            severity = "brutal"
            message = f"War crime detected: {line_count} lines of architectural violence"
        elif line_count >= 300:
            severity = "moderate" 
            message = f"Novel detected: {line_count} lines of unnecessary complexity"
        else:
            severity = "gentle"
            message = f"File getting chubby: {line_count} lines need a diet"
        
        return [Violation(
            rule="giant_file",
            file_path=str(file_path),
            line_number=line_count,
            severity=severity,
            message=message,
            context={"line_count": line_count}
        )]
    
    def _detect_import_ceremony(self, file_path: Path, content: str, tree: ast.AST) -> List[Violation]:
        """Detect import addiction."""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                imports.extend([alias.name for alias in node.names])
        
        import_count = len(imports)
        
        if import_count < 15:
            return []
        
        if import_count >= 25:
            severity = "brutal"
            message = f"Import addiction detected: {import_count} dependencies is architectural heroin"
        else:
            severity = "moderate"
            message = f"Import ceremony: {import_count} imports suggests tight coupling"
        
        return [Violation(
            rule="import_ceremony",
            file_path=str(file_path),
            line_number=1,
            severity=severity,
            message=message,
            context={"import_count": import_count, "imports": imports}
        )]
    
    def _detect_duplicate_blocks(self, file_path: Path, content: str, tree: ast.AST) -> List[Violation]:
        """Detect copy-paste violations."""
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Create a simple hash of the function structure
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
    
    def _detect_complex_functions(self, file_path: Path, content: str, tree: ast.AST) -> List[Violation]:
        """Detect overly complex functions."""
        violations = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Count decision points (if, for, while, try, etc.)
                complexity = 1  # Base complexity
                
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                        complexity += 1
                    elif isinstance(child, ast.BoolOp):
                        complexity += len(child.values) - 1
                
                # Count lines in function
                func_lines = len([line for line in content.split('\n')[node.lineno-1:node.end_lineno] if line.strip()])
                
                if complexity > 10 or func_lines > 50:
                    if complexity > 15 or func_lines > 80:
                        severity = "brutal"
                        message = f"Function '{node.name}' is a complexity nightmare: {complexity} branches, {func_lines} lines"
                    else:
                        severity = "moderate"
                        message = f"Function '{node.name}' is getting complex: {complexity} branches, {func_lines} lines"
                    
                    violations.append(Violation(
                        rule="complex_function",
                        file_path=str(file_path),
                        line_number=node.lineno,
                        severity=severity,
                        message=message,
                        context={"complexity": complexity, "lines": func_lines}
                    ))
        
        return violations