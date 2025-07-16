import { Violation } from './base.js';

export function detectCallbackHell(filePath: string, content: string): Violation[] {
  const violations: Violation[] = [];
  
  // Count nested function expressions using braces
  const lines = content.split('\n');
  let maxNesting = 0;
  let currentNesting = 0;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // Look for function keywords and arrow functions
    if (line.includes('function') || line.includes('=>')) {
      currentNesting++;
      maxNesting = Math.max(maxNesting, currentNesting);
    }
    
    // Track closing braces
    const openBraces = (line.match(/\{/g) || []).length;
    const closeBraces = (line.match(/\}/g) || []).length;
    
    if (closeBraces > openBraces) {
      currentNesting = Math.max(0, currentNesting - (closeBraces - openBraces));
    }
  }
  
  if (maxNesting > 4) {
    let severity: 'brutal' | 'moderate' | 'gentle';
    let message: string;
    
    if (maxNesting > 7) {
      severity = 'brutal';
      message = `Callback hell detected: ${maxNesting} levels of nesting is async nightmare fuel`;
    } else {
      severity = 'moderate';
      message = `Nested callbacks: ${maxNesting} levels suggests promise refactoring needed`;
    }
    
    violations.push({
      rule: 'callback_hell',
      filePath,
      lineNumber: 1,
      severity,
      message,
      context: { maxNesting }
    });
  }
  
  return violations;
}

export function detectComplexFunctions(filePath: string, content: string): Violation[] {
  const violations: Violation[] = [];
  
  // Simple regex to find function declarations
  const functionRegex = /function\s+(\w+)\s*\(/g;
  let match;
  
  while ((match = functionRegex.exec(content)) !== null) {
    const funcName = match[1];
    const startIndex = match.index;
    const startLine = content.substring(0, startIndex).split('\n').length;
    
    // Find the function body
    const functionBody = extractFunctionBody(content, startIndex);
    if (!functionBody) continue;
    
    const functionLines = functionBody.split('\n').length;
    const complexity = calculateComplexity(functionBody);
    
    if (complexity > 10 || functionLines > 50) {
      violations.push(createComplexityViolation(filePath, startLine, funcName, complexity, functionLines));
    }
  }
  
  return violations;
}

function extractFunctionBody(content: string, startIndex: number): string | null {
  let braceCount = 0;
  let endIndex = startIndex;
  let foundStart = false;
  
  for (let i = startIndex; i < content.length; i++) {
    if (content[i] === '{') {
      braceCount++;
      foundStart = true;
    } else if (content[i] === '}') {
      braceCount--;
      if (braceCount === 0 && foundStart) {
        endIndex = i;
        break;
      }
    }
  }
  
  return foundStart ? content.substring(startIndex, endIndex) : null;
}

function calculateComplexity(functionBody: string): number {
  let complexity = 1;
  const decisionPoints = ['if', 'else', 'for', 'while', 'switch', 'case', 'try', 'catch'];
  
  for (const point of decisionPoints) {
    const regex = new RegExp(`\\b${point}\\b`, 'g');
    const matches = functionBody.match(regex);
    if (matches) {
      complexity += matches.length;
    }
  }
  
  return complexity;
}

function createComplexityViolation(filePath: string, lineNumber: number, funcName: string, complexity: number, functionLines: number): Violation {
  let severity: 'brutal' | 'moderate' | 'gentle';
  let message: string;
  
  if (complexity > 15 || functionLines > 80) {
    severity = 'brutal';
    message = `Function '${funcName}' is a complexity nightmare: ${complexity} branches, ${functionLines} lines`;
  } else {
    severity = 'moderate';
    message = `Function '${funcName}' is getting complex: ${complexity} branches, ${functionLines} lines`;
  }
  
  return {
    rule: 'complex_function',
    filePath,
    lineNumber,
    severity,
    message,
    context: { complexity, lines: functionLines }
  };
}
