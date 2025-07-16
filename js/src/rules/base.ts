export interface Violation {
  rule: string;
  filePath: string;
  lineNumber: number;
  severity: 'brutal' | 'moderate' | 'gentle';
  message: string;
  context?: Record<string, any>;
}

export type RuleFunction = (filePath: string, content: string) => Violation[];
