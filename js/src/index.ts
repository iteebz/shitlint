/**
 * Your code is shit. Here's why.
 */

export const version = "0.0.1";
export const author = "Tyson Chan";
export const email = "tyson.chan@proton.me";

export interface ShitLintResult {
  filePath: string;
  message: string;
  severity: "brutal" | "moderate" | "gentle";
  lineNumber?: number;
}

export function analyzeCode(filePath: string): ShitLintResult[] {
  return [
    {
      filePath,
      message: "Your code exists. That's already a problem.",
      severity: "brutal"
    }
  ];
}

export { analyzeCode as default };