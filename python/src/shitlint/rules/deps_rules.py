"""Dependencies audit - detect bloat, version chaos, and unused deps."""

import json
import re
from pathlib import Path
from typing import List, Dict
from .base import Violation


def detect_dependency_violations(file_path: Path, content: str, tree, thresholds: Dict) -> List[Violation]:
    """Detect dependency violations across package.json, requirements.txt, pyproject.toml."""
    violations = []
    
    # Find project root
    root = file_path.parent if file_path.is_file() else file_path
    while root != root.parent:
        if any((root / f).exists() for f in ['package.json', 'requirements.txt', 'pyproject.toml']):
            break
        root = root.parent
    
    # Check each dependency file
    for dep_file in ['package.json', 'requirements.txt', 'pyproject.toml']:
        path = root / dep_file
        if path.exists():
            violations.extend(_analyze_deps(path))
    
    return violations


def _analyze_deps(dep_file: Path) -> List[Violation]:
    """Analyze dependency file for violations."""
    violations = []
    
    try:
        if dep_file.name == 'package.json':
            data = json.loads(dep_file.read_text())
            deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
            ecosystem = 'npm'
        elif dep_file.name.startswith('requirements'):
            lines = [l.strip() for l in dep_file.read_text().split('\n') if l.strip() and not l.startswith('#')]
            deps = {re.split(r'[<>=!]', line)[0].strip(): line for line in lines}
            ecosystem = 'pip'
        elif dep_file.name == 'pyproject.toml':
            # Simple TOML parsing - just regex for deps
            content = dep_file.read_text()
            deps = {}
            for line in content.split('\n'):
                if '=' in line and any(section in content[:content.find(line)] for section in ['[tool.poetry.dependencies]', '[project]']):
                    name = line.split('=')[0].strip().strip('"')
                    if name not in ['python', 'name', 'version']:
                        deps[name] = line.split('=')[1].strip()
            ecosystem = 'pip'
        else:
            return violations
        
        # Check bloat
        total = len(deps)
        if total >= 50:
            violations.append(Violation("deps_bloat", str(dep_file), 1, "brutal", 
                f"Dependency hell: {total} packages (is this a black hole?)", {"total": total}))
        elif total >= 25:
            violations.append(Violation("deps_bloat", str(dep_file), 1, "moderate", 
                f"Package bloat: {total} dependencies", {"total": total}))
        
        # Check left-pad syndrome
        micro_deps = {
            'npm': ['left-pad', 'right-pad', 'is-odd', 'is-even', 'is-number', 'is-string', 'is-array'],
            'pip': ['six', 'future', 'enum34', 'pathlib2', 'typing-extensions', 'dataclasses']
        }
        
        for dep in deps:
            if dep.lower() in micro_deps.get(ecosystem, []):
                violations.append(Violation("deps_leftpad", str(dep_file), 1, "brutal",
                    f"Left-pad syndrome: '{dep}' (write 3 lines of code)", {"dep": dep}))
    
    except Exception:
        pass
    
    return violations