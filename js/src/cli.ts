#!/usr/bin/env node

/**
 * ShitLint CLI - Your code is shit. Here's why.
 */

import { Command } from "commander";
import chalk from "chalk";
import { analyzeCode } from "./index.js";

const program = new Command();

program
  .name("shitlint")
  .description("Your code is shit. Here's why.")
  .version("0.0.1");

program
  .argument("<path>", "Path to analyze")
  .option("--brutal", "Extra brutal mode")
  .action(async (path: string, options: { brutal?: boolean }) => {
    console.log(chalk.red.bold("🔍 SHITLINT ANALYSIS"));
    console.log(chalk.italic("Your code is shit. Here's why.\\n"));
    
    const results = await analyzeCode(path);
    
    if (results.length === 0) {
      console.log(chalk.green("✅ No violations found. Your code doesn't completely suck."));
      return;
    }
    
    results.forEach(result => {
      const emoji = result.severity === 'brutal' ? '💀' : 
                   result.severity === 'moderate' ? '⚠️' : '🟡';
      const style = result.severity === 'brutal' ? chalk.red.bold : 
                   result.severity === 'moderate' ? chalk.yellow : chalk.dim.yellow;
      
      console.log(style(`${emoji} ${result.message}`));
      console.log(chalk.gray(`   📁 ${result.filePath}`));
      if (result.lineNumber) {
        console.log(chalk.gray(`   📊 Line: ${result.lineNumber}`));
      }
      if (result.rule) {
        console.log(chalk.gray(`   🔍 Rule: ${result.rule}\\n`));
      }
    });
    
    // Summary stats
    const brutalCount = results.filter(r => r.severity === 'brutal').length;
    const moderateCount = results.filter(r => r.severity === 'moderate').length;
    const gentleCount = results.length - brutalCount - moderateCount;
    
    console.log(chalk.bold("📈 DAMAGE REPORT:"));
    console.log(`   💀 War crimes: ${brutalCount}`);
    console.log(`   ⚠️  Code smells: ${moderateCount}`);
    console.log(`   🟡 Minor issues: ${gentleCount}`);
    
    if (brutalCount > 0) {
      console.log(chalk.red.bold("\\nVERDICT: Your code looks like it was written during an earthquake"));
    } else if (moderateCount > 0) {
      console.log(chalk.yellow("\\nVERDICT: Your code needs architectural liposuction"));
    } else {
      console.log(chalk.dim.yellow("\\nVERDICT: Minor bloat detected. Time for a code diet."));
    }
  });

program.parse();