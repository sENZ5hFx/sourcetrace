#!/usr/bin/env node

import { Command } from "commander";
import { resolve } from "path";
import { writeFileSync } from "fs";
import { runEngine } from "./engine.js";
import type { AnalyzerOptions } from "./types.js";

const program = new Command();

program
  .name("sourcetrace")
  .description(
    "Automated truth-extraction for any codebase. Reads your source and produces a structured reality map."
  )
  .version("0.1.0");

program
  .command("analyze")
  .description("Analyze a repository and produce a source truth pack")
  .argument("<target>", "Path to the repository to analyze")
  .option("-o, --output <path>", "Output file path (default: stdout)")
  .option("--no-llm", "Skip LLM-powered analysis (fast, local-only)")
  .option("-v, --verbose", "Verbose output", false)
  .option(
    "--include <patterns...>",
    "Glob patterns to include (default: all files)"
  )
  .option(
    "--exclude <patterns...>",
    "Glob patterns to exclude (default: node_modules, .git, dist)"
  )
  .action(async (target: string, opts) => {
    const options: AnalyzerOptions = {
      target: resolve(target),
      output: opts.output ? resolve(opts.output) : undefined,
      noLlm: opts.llm === false,
      verbose: opts.verbose,
      include: opts.include,
      exclude: opts.exclude,
    };

    if (options.verbose) {
      console.error(`[sourcetrace] Analyzing: ${options.target}`);
      console.error(`[sourcetrace] LLM: ${options.noLlm ? "disabled" : "enabled"}`);
    }

    try {
      const pack = await runEngine(options);
      const output = JSON.stringify(pack, null, 2);

      if (options.output) {
        writeFileSync(options.output, output, "utf-8");
        console.error(`[sourcetrace] Truth pack written to: ${options.output}`);
      } else {
        process.stdout.write(output);
      }
    } catch (err) {
      console.error(`[sourcetrace] Error: ${err instanceof Error ? err.message : err}`);
      process.exit(1);
    }
  });

program.parse();
