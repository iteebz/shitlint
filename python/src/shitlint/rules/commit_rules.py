"""Commit message violation detection."""

import subprocess
import re
from pathlib import Path
from typing import List, Dict
from .base import Violation


def detect_commit_violations(file_path: Path, content: str, tree, thresholds: Dict) -> List[Violation]:
    """Detect garbage commit messages in git history."""
    violations = []
    
    try:
        # Get last 20 commit messages
        result = subprocess.run(
            ['git', 'log', '--oneline', '-20', '--format=%s'],
            cwd=file_path.parent if file_path.is_file() else file_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return violations  # Not a git repo or no commits
            
        commit_messages = result.stdout.strip().split('\n')
        if not commit_messages or commit_messages == ['']:
            return violations
            
        # Garbage patterns to detect
        garbage_patterns = [
            # Single word laziness
            r'^(fix|update|wip|temp|asdf|test|done|ok|minor|changes?)$',
            # Vague bullshit
            r'^(fix stuff|update things|minor changes|small fix|quick fix|updates?)$',
            # Emotional commits
            r'^(fuck|shit|damn|wtf|why|arghhh|grr|ugh)',
            # Keyboard mashing
            r'^(\.{3,}|_{3,}|-{3,}|={3,}|123|asdf|qwerty)',
            # Too short but not conventional
            r'^[a-z]{1,3}$',
        ]
        
        # Good patterns to ignore (conventional commits)
        good_patterns = [
            r'^(feat|fix|docs|style|refactor|test|chore|build|ci|perf|revert)(\(.+\))?: .+',
            r'^.{10,}',  # Reasonably long messages
        ]
        
        message_counts = {}
        for i, message in enumerate(commit_messages):
            if not message:
                continue
                
            # Skip if it's a good conventional commit
            is_good = any(re.match(pattern, message, re.IGNORECASE) for pattern in good_patterns)
            if is_good:
                continue
                
            # Count duplicate messages
            message_counts[message] = message_counts.get(message, 0) + 1
            
            # Check for garbage patterns
            for pattern in garbage_patterns:
                if re.match(pattern, message, re.IGNORECASE):
                    severity = "brutal" if i < 5 else "moderate"  # Recent commits are more brutal
                    violations.append(Violation(
                        rule="commit_garbage",
                        file_path=str(file_path),
                        line_number=1,
                        severity=severity,
                        message=f"Garbage commit message: '{message}'",
                        context={"commit_message": message, "pattern": pattern}
                    ))
                    break
        
        # Flag duplicate commit messages
        for message, count in message_counts.items():
            if count > 1:
                violations.append(Violation(
                    rule="commit_duplicates",
                    file_path=str(file_path),
                    line_number=1,
                    severity="moderate",
                    message=f"Duplicate commit message used {count} times: '{message}'",
                    context={"commit_message": message, "count": count}
                ))
                
    except Exception:
        # Git not available or other error - skip commit analysis
        pass
        
    return violations