import { Violation } from './base.js';

export function detectImportCeremony(filePath: string, content: string): Violation[] {
  const imports: string[] = [];
  
  // Simple regex to find import statements
  const importRegex = /^import\s+.*?from\s+['"].*?['"];?$/gm;
  let match;
  
  while ((match = importRegex.exec(content)) !== null) {
    imports.push(match[0]);
  }
  
  // Also check for require statements
  const requireRegex = /require\s*\(['"].*?['"]\)/g;
  while ((match = requireRegex.exec(content)) !== null) {
    imports.push(match[0]);
  }
  
  const importCount = imports.length;
  
  if (importCount < 15) {
    return [];
  }
  
  let severity: 'brutal' | 'moderate' | 'gentle';
  let message: string;
  
  if (importCount >= 25) {
    severity = 'brutal';
    message = `Import addiction detected: ${importCount} dependencies is npm dependency hell`;
  } else {
    severity = 'moderate';
    message = `Import ceremony: ${importCount} imports suggests tight coupling`;
  }
  
  return [{
    rule: 'import_ceremony',
    filePath,
    lineNumber: 1,
    severity,
    message,
    context: { importCount, imports }
  }];
}
