import { readFileSync } from 'fs';
import { RuleFunction } from './base.js';
import { detectGiantFiles } from './giant-files.js';
import { detectImportCeremony } from './imports.js';
import { detectCallbackHell, detectComplexFunctions } from './complexity.js';
import { detectReactAntipatterns } from './react.js';

export { Violation } from './base.js';

export class RuleEngine {
  private rules: RuleFunction[];

  constructor() {
    this.rules = [
      detectGiantFiles,
      detectImportCeremony,
      detectCallbackHell,
      detectComplexFunctions,
      detectReactAntipatterns,
    ];
  }

  analyzeFile(filePath: string): Array<ReturnType<RuleFunction>[0]> {
    try {
      const content = readFileSync(filePath, 'utf-8');
      const violations = [];
      
      for (const rule of this.rules) {
        violations.push(...rule(filePath, content));
      }
      
      return violations;
    } catch (error) {
      return [];
    }
  }
}
