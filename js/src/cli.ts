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
  .action((path: string, options: { brutal?: boolean }) => {
    console.log(chalk.red.bold("🔍 SHITLINT ANALYSIS"));
    console.log(chalk.italic("Your code is shit. Here's why.\n"));
    
    const results = analyzeCode(path);
    
    results.forEach(result => {
      console.log(chalk.red(`🚨 ${result.message}`));
      console.log(chalk.gray(`   📁 ${result.filePath}\n`));
    });
    
    if (options.brutal) {
      console.log(chalk.red.bold("VERDICT: Your code looks like it was written during an earthquake"));
    } else {
      console.log(chalk.yellow("VERDICT: Your code needs work"));
    }
  });

program.parse();