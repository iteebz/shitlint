"""Over-abstraction and architectural bloat detection."""

from pathlib import Path
from typing import List, Dict, Set
import ast

from .base import Violation


def detect_over_abstraction(file_path: Path, content: str, tree: ast.AST, thresholds: Dict) -> List[Violation]:
    """Detect unnecessary abstraction layers and architectural bloat."""
    violations = []
    
    # Skip if not a Python file
    if tree is None:
        return violations
    
    # Track inheritance chains and class relationships
    class_info = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_info[node.name] = {
                'node': node,
                'bases': [base.id for base in node.bases if isinstance(base, ast.Name)],
                'methods': [n for n in node.body if isinstance(n, ast.FunctionDef)],
                'abstract_methods': [],
                'delegation_methods': 0,
                'total_methods': 0
            }
            
            # Analyze methods
            for method in class_info[node.name]['methods']:
                class_info[node.name]['total_methods'] += 1
                
                # Check for abstract methods (only raise NotImplementedError)
                if len(method.body) == 1 and isinstance(method.body[0], ast.Raise):
                    exc = method.body[0].exc
                    if isinstance(exc, ast.Name) and exc.id == 'NotImplementedError':
                        class_info[node.name]['abstract_methods'].append(method.name)
                    elif isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name) and exc.func.id == 'NotImplementedError':
                        class_info[node.name]['abstract_methods'].append(method.name)
                
                # Check for pure delegation
                if _is_pure_delegation(method):
                    class_info[node.name]['delegation_methods'] += 1
    
    # Detect violations
    for class_name, info in class_info.items():
        node = info['node']
        
        # 1. God abstractions - too many abstract methods
        if len(info['abstract_methods']) >= 10:
            violations.append(Violation(
                rule="god_abstraction",
                file_path=str(file_path),
                line_number=node.lineno,
                severity="brutal",
                message=f"Class '{class_name}' is a god abstraction with {len(info['abstract_methods'])} abstract methods",
                context={"abstract_count": len(info['abstract_methods'])}
            ))
        
        # 2. Wrapper hell - classes that mostly delegate
        if info['total_methods'] > 1 and info['delegation_methods'] >= info['total_methods'] * 0.7:
            violations.append(Violation(
                rule="wrapper_hell",
                file_path=str(file_path),
                line_number=node.lineno,
                severity="brutal",
                message=f"Class '{class_name}' is wrapper hell - {info['delegation_methods']}/{info['total_methods']} methods just delegate",
                context={"delegation_ratio": info['delegation_methods'] / info['total_methods']}
            ))
        
        # 3. Inheritance depth check
        depth = _calculate_inheritance_depth(class_name, class_info, set())
        if depth > 4:
            violations.append(Violation(
                rule="inheritance_hell",
                file_path=str(file_path),
                line_number=node.lineno,
                severity="brutal",
                message=f"Class '{class_name}' has inheritance depth of {depth} - delete some layers",
                context={"depth": depth}
            ))
        elif depth > 3:
            violations.append(Violation(
                rule="inheritance_hell",
                file_path=str(file_path),
                line_number=node.lineno,
                severity="moderate",
                message=f"Class '{class_name}' has inheritance depth of {depth} - consider flattening",
                context={"depth": depth}
            ))
        
        # 4. Pointless factory detection
        if _is_pointless_factory(class_name, info):
            violations.append(Violation(
                rule="pointless_factory",
                file_path=str(file_path),
                line_number=node.lineno,
                severity="moderate",
                message=f"Class '{class_name}' is a pointless factory - just use direct instantiation",
                context={}
            ))
        
        # 5. Interface overkill - abstract class with only one concrete implementation
        if info['abstract_methods'] and len(info['abstract_methods']) >= 3:
            # This would need cross-file analysis to be fully accurate
            # For now, flag classes with many abstract methods in single file
            violations.append(Violation(
                rule="interface_overkill",
                file_path=str(file_path),
                line_number=node.lineno,
                severity="moderate",
                message=f"Class '{class_name}' defines {len(info['abstract_methods'])} abstract methods - might be overkill",
                context={"abstract_count": len(info['abstract_methods'])}
            ))
    
    return violations


def _is_pure_delegation(method: ast.FunctionDef) -> bool:
    """Check if method is pure delegation (just calls same method on internal object)."""
    if len(method.body) != 1:
        return False
    
    stmt = method.body[0]
    if not isinstance(stmt, ast.Return):
        return False
    
    # Check for pattern: return self.obj.method_name(args)
    if isinstance(stmt.value, ast.Call):
        call = stmt.value
        if isinstance(call.func, ast.Attribute):
            # Check if it's calling same method name on an attribute
            if call.func.attr == method.name:
                # Check if the object being called is an attribute of self
                if isinstance(call.func.value, ast.Attribute) and isinstance(call.func.value.value, ast.Name):
                    if call.func.value.value.id == 'self':
                        return True
    
    return False


def _calculate_inheritance_depth(class_name: str, class_info: Dict, visited: Set[str]) -> int:
    """Calculate inheritance depth for a class."""
    if class_name in visited or class_name not in class_info:
        return 0
    
    visited.add(class_name)
    bases = class_info[class_name]['bases']
    
    if not bases:
        return 1
    
    max_depth = 0
    for base in bases:
        depth = _calculate_inheritance_depth(base, class_info, visited.copy())
        max_depth = max(max_depth, depth)
    
    return max_depth + 1


def _is_pointless_factory(class_name: str, info: Dict) -> bool:
    """Detect pointless factory classes."""
    methods = info['methods']
    
    # Must have exactly one non-init method
    non_init_methods = [m for m in methods if m.name != '__init__']
    if len(non_init_methods) != 1:
        return False
    
    method = non_init_methods[0]
    
    # Method name should suggest factory pattern
    if not any(keyword in method.name.lower() for keyword in ['create', 'build', 'make', 'new']):
        return False
    
    # Check if method body is just simple instantiation without complex logic
    if len(method.body) == 1 and isinstance(method.body[0], ast.Return):
        ret = method.body[0]
        if isinstance(ret.value, ast.Call):
            # If it's just calling a constructor with passed args, it's probably pointless
            return True
    
    return False