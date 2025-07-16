import { Violation } from './base.js';

export function detectReactAntipatterns(filePath: string, content: string): Violation[] {
  if (!filePath.includes('tsx') && !filePath.includes('jsx')) {
    return [];
  }
  
  const violations: Violation[] = [];
  
  // Check for inline object/function creation in JSX
  const inlineObjectRegex = /\{\s*\{.*?\}\s*\}/g;
  const inlineArrowFunctionRegex = /\{\s*\(.*?\)\s*=>\s*.*?\}/g;
  
  let match;
  while ((match = inlineObjectRegex.exec(content)) !== null) {
    const lineNumber = content.substring(0, match.index).split('\n').length;
    violations.push({
      rule: 'react_inline_creation',
      filePath,
      lineNumber,
      severity: 'moderate',
      message: 'Inline object creation in JSX causes unnecessary re-renders',
      context: { type: 'object' }
    });
  }
  
  while ((match = inlineArrowFunctionRegex.exec(content)) !== null) {
    const lineNumber = content.substring(0, match.index).split('\n').length;
    violations.push({
      rule: 'react_inline_creation',
      filePath,
      lineNumber,
      severity: 'moderate',
      message: 'Inline function creation in JSX causes unnecessary re-renders',
      context: { type: 'function' }
    });
  }
  
  return violations;
}
