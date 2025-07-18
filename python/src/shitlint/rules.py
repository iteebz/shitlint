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
    
    def __init__(self, brutality: str = "professional"):
        self.brutality = brutality
        self.rules = [
            self._detect_giant_files,
            self._detect_import_ceremony,
            self._detect_duplicate_blocks,
            self._detect_complex_functions,
            self._detect_naming_violations,
        ]
        
        # Brutality-based thresholds
        self.thresholds = self._get_brutality_thresholds(brutality)
    
    def _get_brutality_thresholds(self, brutality: str) -> Dict:
        """Get detection thresholds based on brutality level."""
        if brutality == "brutal":
            # Harsh - catch everything
            return {
                "file_lines": {"gentle": 150, "moderate": 200, "brutal": 300},
                "imports": {"moderate": 10, "brutal": 15},
                "complexity": {"moderate": 8, "brutal": 12},
                "function_lines": {"moderate": 30, "brutal": 50},
                "name_length": 20,
                "enable_loop_var_check": True
            }
        elif brutality == "gentle":
            # Relaxed - only catch obvious problems
            return {
                "file_lines": {"gentle": 300, "moderate": 500, "brutal": 800},
                "imports": {"moderate": 20, "brutal": 35},
                "complexity": {"moderate": 15, "brutal": 25},
                "function_lines": {"moderate": 80, "brutal": 120},
                "name_length": 35,
                "enable_loop_var_check": False
            }
        else:  # professional (default)
            # Balanced - current thresholds
            return {
                "file_lines": {"gentle": 200, "moderate": 300, "brutal": 500},
                "imports": {"moderate": 15, "brutal": 25},
                "complexity": {"moderate": 10, "brutal": 15},
                "function_lines": {"moderate": 50, "brutal": 80},
                "name_length": 25,
                "enable_loop_var_check": False
            }
    
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
        
        thresholds = self.thresholds["file_lines"]
        
        if line_count < thresholds["gentle"]:
            return []
        
        if line_count >= thresholds["brutal"]:
            severity = "brutal"
            message = f"War crime detected: {line_count} lines of architectural violence"
        elif line_count >= thresholds["moderate"]:
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
        
        thresholds = self.thresholds["imports"]
        
        if import_count < thresholds["moderate"]:
            return []
        
        if import_count >= thresholds["brutal"]:
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
                
                complexity_thresholds = self.thresholds["complexity"]
                line_thresholds = self.thresholds["function_lines"]
                
                if complexity > complexity_thresholds["moderate"] or func_lines > line_thresholds["moderate"]:
                    if complexity > complexity_thresholds["brutal"] or func_lines > line_thresholds["brutal"]:
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
    
    def _detect_naming_violations(self, file_path: Path, content: str, tree: ast.AST) -> List[Violation]:
        """Detect bullshit variable and function names."""
        violations = []
        
        # Ceremony variable names that say nothing
        ceremony_vars = {
            'data', 'result', 'temp', 'obj', 'item', 'val', 'thing', 'stuff', 
            'var', 'x', 'y', 'z', 'i', 'j', 'k', 'value', 'element', 'node',
            'info', 'content', 'payload', 'response', 'request', 'params', 'args'
        }
        
        # AI-generated monstrosities (too long)
        max_reasonable_length = self.thresholds["name_length"]
        enable_loop_var_check = self.thresholds["enable_loop_var_check"]
        
        # Class name ceremony 
        ceremony_classes = {
            'Manager', 'Handler', 'Processor', 'Utility', 'Helper', 'Service',
            'Factory', 'Builder', 'Provider', 'Controller', 'Adapter', 'Wrapper'
        }
        
        class NameCollector(ast.NodeVisitor):
            def __init__(self):
                self.violations = []
                self.current_function = None
                
            def visit_FunctionDef(self, node):
                self.current_function = node.name
                
                # Check function parameters for ceremony
                for arg in node.args.args:
                    if arg.arg in ceremony_vars:
                        self.violations.append(Violation(
                            rule="ceremony_parameter",
                            file_path=str(file_path),
                            line_number=node.lineno,
                            severity="moderate",
                            message=f"Function '{node.name}' has ceremony parameter: '{arg.arg}' - be specific",
                            context={"function": node.name, "parameter": arg.arg}
                        ))
                
                # Check function name length (AI monstrosity)
                if len(node.name) > max_reasonable_length:
                    self.violations.append(Violation(
                        rule="ai_generated_name",
                        file_path=str(file_path),
                        line_number=node.lineno,
                        severity="moderate", 
                        message=f"Function '{node.name}' looks AI-generated: {len(node.name)} chars - simplify",
                        context={"function": node.name, "length": len(node.name)}
                    ))
                
                self.generic_visit(node)
                self.current_function = None
                
            def visit_ClassDef(self, node):
                # Check for ceremony class names (substring match)
                if any(ceremony in node.name for ceremony in ceremony_classes):
                    self.violations.append(Violation(
                        rule="ceremony_class",
                        file_path=str(file_path),
                        line_number=node.lineno,
                        severity="moderate",
                        message=f"Class '{node.name}' is ceremony bullshit - what does it actually do?",
                        context={"class": node.name}
                    ))
                
                # Check class name length
                if len(node.name) > max_reasonable_length:
                    self.violations.append(Violation(
                        rule="ai_generated_name",
                        file_path=str(file_path),
                        line_number=node.lineno,
                        severity="moderate",
                        message=f"Class '{node.name}' looks AI-generated: {len(node.name)} chars - simplify",
                        context={"class": node.name, "length": len(node.name)}
                    ))
                
                self.generic_visit(node)
                
            def visit_Assign(self, node):
                # Check variable assignments for ceremony
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        
                        if var_name in ceremony_vars:
                            # Skip loop variables unless brutal mode
                            if not enable_loop_var_check and var_name in {'i', 'j', 'k', 'x', 'y', 'z'}:
                                continue
                                
                            func_context = f" in {self.current_function}" if self.current_function else ""
                            self.violations.append(Violation(
                                rule="ceremony_variable",
                                file_path=str(file_path),
                                line_number=node.lineno,
                                severity="gentle",
                                message=f"Variable '{var_name}'{func_context} is ceremony - be descriptive",
                                context={"variable": var_name, "function": self.current_function}
                            ))
                        
                        # Check for AI monstrosities
                        if len(var_name) > max_reasonable_length:
                            func_context = f" in {self.current_function}" if self.current_function else ""
                            self.violations.append(Violation(
                                rule="ai_generated_name",
                                file_path=str(file_path),
                                line_number=node.lineno,
                                severity="moderate",
                                message=f"Variable '{var_name}'{func_context} looks AI-generated: {len(var_name)} chars",
                                context={"variable": var_name, "length": len(var_name)}
                            ))
                
                self.generic_visit(node)
        
        collector = NameCollector()
        collector.visit(tree)
        violations.extend(collector.violations)
        
        return violations