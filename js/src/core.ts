/**
 * Core ShitLint functionality for JavaScript/TypeScript.
 */

import { readFileSync, statSync } from 'fs';
import { join, extname } from 'path';
import { glob } from 'glob';
import { RuleEngine, Violation } from './rules/index.js';

export interface ShitLintResult {
  filePath: string;
  message: string;
  severity: 'brutal' | 'moderate' | 'gentle';
  lineNumber?: number;
  rule?: string;
}

export async function analyzeCode(path: string): Promise<ShitLintResult[]> {
  const engine = new RuleEngine();
  const results: ShitLintResult[] = [];
  
  const stats = statSync(path);
  
  if (stats.isFile()) {
    const ext = extname(path);
    if (['.js', '.jsx', '.ts', '.tsx', '.py'].includes(ext)) {
      const violations = engine.analyzeFile(path);
      results.push(...violationsToResults(violations));
    }
  } else if (stats.isDirectory()) {
    // Find all supported files
    const files = await glob('**/*.{js,jsx,ts,tsx,py}', { 
      cwd: path,
      absolute: true,
      ignore: ['**/node_modules/**', '**/dist/**', '**/.git/**']
    });
    
    for (const file of files) {
      const violations = engine.analyzeFile(file);
      results.push(...violationsToResults(violations));
    }
  }
  
  return results;
}

function violationsToResults(violations: Violation[]): ShitLintResult[] {
  return violations.map(v => ({
    filePath: v.filePath,
    message: v.message,
    severity: v.severity,
    lineNumber: v.lineNumber,
    rule: v.rule
  }));
}
