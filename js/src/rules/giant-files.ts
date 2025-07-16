import { Violation } from './base.js';

export function detectGiantFiles(filePath: string, content: string): Violation[] {
  const lines = content.split('\n').filter(line => line.trim());
  const lineCount = lines.length;
  
  if (lineCount < 200) {
    return [];
  }
  
  let severity: 'brutal' | 'moderate' | 'gentle';
  let message: string;
  
  if (lineCount >= 500) {
    severity = 'brutal';
    message = `Architectural war crime: ${lineCount} lines of JavaScript chaos`;
  } else if (lineCount >= 300) {
    severity = 'moderate';
    message = `JavaScript novel detected: ${lineCount} lines of callback spaghetti`;
  } else {
    severity = 'gentle';
    message = `File bloat detected: ${lineCount} lines need refactoring`;
  }
  
  return [{
    rule: 'giant_file',
    filePath,
    lineNumber: lineCount,
    severity,
    message,
    context: { lineCount }
  }];
}
