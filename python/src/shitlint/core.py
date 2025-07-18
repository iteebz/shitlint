"""Core ShitLint functionality - Heuristics + AST detection."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any
import pathspec
from .engine import RuleEngine
from .rules.base import Violation


@dataclass
class ShitLintResult:
    """Result of ShitLint analysis."""
    
    file_path: str
    message: str
    severity: str = "brutal"
    line_number: Optional[int] = None
    rule: Optional[str] = None


@dataclass
class AnalysisContext:
    """Context information for analysis."""
    
    tree_structure: Dict[str, Any]
    file_count: int
    file_types: Dict[str, int]
    naming_violations: List[str]


def analyze_code(path: Path, config=None) -> List[ShitLintResult]:
    """Analyze code with heuristics + AST rules."""
    brutality = config.brutality if config else "professional"
    engine = RuleEngine(brutality=brutality, config=config.__dict__ if config else None)
    results = []
    
    if path.is_file():
        violations = engine.analyze_file(path)
        results.extend(_violations_to_results(violations))
    elif path.is_dir():
        # Get all Python files first
        python_files = list(_get_python_files(path, config))
        
        # Analyze each file (collects cross-file patterns)
        for file_path in python_files:
            violations = engine.analyze_file(file_path)
            results.extend(_violations_to_results(violations))
        
        # Also analyze documentation files
        doc_files = list(_get_doc_files(path, config))
        for file_path in doc_files:
            violations = engine.analyze_file(file_path)
            results.extend(_violations_to_results(violations))
        
        # Generate cross-file violations after analyzing all files
        cross_file_violations = engine.get_cross_file_violations()
        results.extend(_violations_to_results(cross_file_violations))
    
    return results


def get_analysis_context(path: Path, config=None) -> AnalysisContext:
    """Get full context for tree structure analysis."""
    if path.is_file():
        return AnalysisContext(
            tree_structure={"file": str(path)},
            file_count=1,
            file_types={path.suffix: 1},
            naming_violations=[]
        )
    
    # Directory analysis
    tree = _build_tree_structure(path)
    python_files = list(_get_python_files(path, config))
    
    file_types = {}
    for file_path in python_files:
        ext = file_path.suffix
        file_types[ext] = file_types.get(ext, 0) + 1
    
    naming_violations = _detect_naming_violations(python_files)
    
    return AnalysisContext(
        tree_structure=tree,
        file_count=len(python_files),
        file_types=file_types,
        naming_violations=naming_violations
    )


def _get_python_files(path: Path, config=None) -> List[Path]:
    """Get all Python files, respecting .gitignore and config."""
    spec = _load_gitignore_spec(path, config)
    
    files = []
    for file_path in path.rglob('*.py'):
        if file_path.is_file():
            # Skip files too large
            if config and file_path.stat().st_size > config.max_file_size:
                continue
                
            # Get relative path for gitignore matching
            try:
                rel_path = file_path.relative_to(path)
                if not spec.match_file(str(rel_path)):
                    files.append(file_path)
            except ValueError:
                # File is outside the root path
                continue
    
    return files


def _get_doc_files(path: Path, config=None) -> List[Path]:
    """Get all documentation files, respecting .gitignore and config."""
    spec = _load_gitignore_spec(path, config)
    
    files = []
    doc_patterns = ['*.md', '*.rst', '*.txt']
    for pattern in doc_patterns:
        for file_path in path.rglob(pattern):
            if file_path.is_file():
                # Skip files too large
                if config and file_path.stat().st_size > config.max_file_size:
                    continue
                    
                # Get relative path for gitignore matching
                try:
                    rel_path = file_path.relative_to(path)
                    if not spec.match_file(str(rel_path)):
                        files.append(file_path)
                except ValueError:
                    # File is outside the root path
                    continue
    
    return files


def _load_gitignore_spec(path: Path, config=None) -> pathspec.PathSpec:
    """Load .gitignore patterns and create pathspec."""
    gitignore_patterns = []
    
    # Default ignores
    gitignore_patterns.extend([
        '.git/',
        '__pycache__/',
        '*.pyc',
        '.venv/',
        'venv/',
        '.pytest_cache/',
        'node_modules/',
        '.env.local',
        '.env.*.local',
        'dist/',
        'build/',
        '*.egg-info/',
    ])
    
    # Add config ignore patterns
    if config and config.ignore_patterns:
        gitignore_patterns.extend(config.ignore_patterns)
    
    # Read .gitignore if it exists
    gitignore_path = path / '.gitignore'
    if gitignore_path.exists():
        try:
            with open(gitignore_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        gitignore_patterns.append(line)
        except Exception:
            pass  # Ignore gitignore read errors
    
    return pathspec.PathSpec.from_lines('gitwildmatch', gitignore_patterns)


def _build_tree_structure(path: Path, max_depth: int = 3) -> Dict[str, Any]:
    """Build tree structure for context, respecting .gitignore."""
    spec = _load_gitignore_spec(path)
    
    def _build_tree(current_path: Path, depth: int = 0) -> Dict[str, Any]:
        if depth > max_depth:
            return {"...": "truncated"}
        
        tree = {}
        try:
            for item in current_path.iterdir():
                # Get relative path for gitignore matching
                try:
                    rel_path = item.relative_to(path)
                    if spec.match_file(str(rel_path)):
                        continue
                except ValueError:
                    continue
                
                # Skip hidden files except important ones
                if item.name.startswith('.') and item.name not in {'.env', '.gitignore'}:
                    continue
                
                if item.is_dir():
                    tree[f"{item.name}/"] = _build_tree(item, depth + 1)
                else:
                    tree[item.name] = None
        except PermissionError:
            pass
        
        return tree
    
    return _build_tree(path)


def _detect_naming_violations(files: List[Path]) -> List[str]:
    """Detect naming violations in file structure."""
    violations = []
    
    # File name patterns
    names = [f.stem for f in files]
    
    # Check for duplicates
    seen = set()
    for name in names:
        if name in seen:
            violations.append(f"Duplicate file name pattern: {name}")
        seen.add(name)
    
    # Check for vague names
    vague_names = {'utils', 'helpers', 'common', 'misc', 'stuff', 'base', 'core', 'main'}
    for name in names:
        if name in vague_names:
            violations.append(f"Vague file name: {name}.py")
    
    # Check for inconsistent patterns
    has_snake_case = any('_' in name for name in names)
    has_camel_case = any(name != name.lower() and '_' not in name for name in names)
    
    if has_snake_case and has_camel_case:
        violations.append("Inconsistent naming convention: mix of snake_case and camelCase")
    
    return violations


def _violations_to_results(violations: List[Violation]) -> List[ShitLintResult]:
    """Convert violations to results."""
    return [
        ShitLintResult(
            file_path=v.file_path,
            message=v.message,
            severity=v.severity,
            line_number=v.line_number,
            rule=v.rule
        )
        for v in violations
    ]