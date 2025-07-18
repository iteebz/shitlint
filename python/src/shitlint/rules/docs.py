"""Documentation audit - detect outdated/missing docs."""

import re
from pathlib import Path
from typing import List, Dict
from .base import Violation


def detect_documentation_violations(file_path: Path, content: str, tree, thresholds: Dict) -> List[Violation]:
    """Detect documentation violations in README and doc files."""
    violations = []
    
    # Skip if this is a Python file (tree will be provided)
    if tree is not None:
        return violations
    
    # If this is a documentation file, analyze it directly
    if file_path.is_file():
        doc_patterns = ['README', 'CHANGELOG', 'CONTRIBUTING', 'INSTALL', 'LICENSE', 'USAGE']
        name_upper = file_path.stem.upper()
        
        # Check if it's a documentation file
        if (any(pattern in name_upper for pattern in doc_patterns) or 
            file_path.suffix.lower() in ['.md', '.rst', '.txt']):
            violations.extend(_analyze_docs(file_path))
    
    # Also check project root for standard doc files (only once per scan)
    if file_path.is_dir():
        root = file_path
        doc_files = ['README.md', 'README.rst', 'README.txt', 'README', 'CHANGELOG.md', 'CONTRIBUTING.md']
        for doc_file in doc_files:
            path = root / doc_file
            if path.exists():
                violations.extend(_analyze_docs(path))
        
        # Check docs/ directory
        docs_dir = root / 'docs'
        if docs_dir.exists():
            for doc_path in docs_dir.rglob('*.md'):
                violations.extend(_analyze_docs(doc_path))
    
    return violations


def _analyze_docs(doc_file: Path) -> List[Violation]:
    """Analyze documentation file for violations."""
    violations = []
    
    try:
        content = doc_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Check for lazy placeholders
        lazy_patterns = [
            (r'TODO.*write.*doc', 'TODO: write docs (classic procrastination)'),
            (r'Coming soon', 'Coming soon (when?)'),
            (r'Under construction', 'Under construction (abandoned?)'),
            (r'Work in progress', 'Work in progress (forever?)'),
            (r'Description coming', 'Description coming (never?)'),
            (r'More info later', 'More info later (sure...)'),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, message in lazy_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    violations.append(Violation("docs_lazy", str(doc_file), i, "moderate", 
                        f"{message}: '{line.strip()}'", {"line": line.strip()}))
        
        # Check for dead/suspicious links
        url_pattern = r'https?://[^\s\)\]]+|www\.[^\s\)\]]+'
        urls = re.findall(url_pattern, content)
        
        suspicious_domains = ['localhost', '127.0.0.1', 'example.com', 'test.com', 'demo.com']
        for url in urls:
            for domain in suspicious_domains:
                if domain in url:
                    violations.append(Violation("docs_deadlink", str(doc_file), 1, "moderate",
                        f"Suspicious link: {url}", {"url": url}))
        
        # Check for outdated version references
        version_patterns = [
            r'python\s*2\.[0-9]',
            r'node\s*[0-9]\.',
            r'v?[0-9]\.[0-9]\.[0-9].*beta',
            r'v?[0-9]\.[0-9]\.[0-9].*alpha',
            r'v?[0-9]\.[0-9]\.[0-9].*rc',
        ]
        
        for pattern in version_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                match = re.search(pattern, content, re.IGNORECASE).group()
                violations.append(Violation("docs_oldversion", str(doc_file), 1, "moderate",
                    f"Outdated version reference: {match}", {"version": match}))
        
        # Check for empty/minimal README
        if doc_file.name.startswith('README') and len(content.strip()) < 100:
            violations.append(Violation("docs_empty", str(doc_file), 1, "brutal",
                "Empty README (tell us what this does)", {"length": len(content.strip())}))
        
        # Check for broken markdown links
        md_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        md_links = re.findall(md_link_pattern, content)
        for text, link in md_links:
            if link.startswith('#') and link.count('#') > 1:
                violations.append(Violation("docs_brokenlink", str(doc_file), 1, "moderate",
                    f"Broken anchor link: {link}", {"link": link}))
    
    except Exception:
        pass
    
    return violations