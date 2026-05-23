/**
 * Quick Start Extractor
 *
 * Derives the actual setup/run commands from config files and scripts.
 * Not from what the README *says* — from what the system *needs*.
 */

import type { AnalyzerOptions, QuickStart, EnvVarEntry } from "../types.js";
import type { ScannedFile } from "../utils/fs.js";

export async function extractQuickStart(
  files: ScannedFile[],
  options: AnalyzerOptions
): Promise<QuickStart> {
  const prerequisites = detectPrerequisites(files);
  const setupCommands = deriveSetupCommands(files);
  const runCommand = deriveRunCommand(files);
  const testCommand = deriveTestCommand(files);
  const keyEnvVars = extractRequiredEnvVars(files);
  const firstThing = deriveFirstThing(files);

  return {
    prerequisites,
    setup_commands: setupCommands,
    run_command: runCommand,
    test_command: testCommand,
    key_env_vars: keyEnvVars,
    first_thing_to_know: firstThing,
  };
}

function detectPrerequisites(files: ScannedFile[]): string[] {
  const prereqs: string[] = [];

  const pkg = files.find((f) => f.relativePath === "package.json");
  if (pkg) {
    try {
      const parsed = JSON.parse(pkg.content);
      const engines = parsed.engines || {};
      if (engines.node) prereqs.push(`Node.js ${engines.node}`);
      if (engines.npm) prereqs.push(`npm ${engines.npm}`);
    } catch { /* skip */ }
    prereqs.push("npm (or equivalent package manager)");
  }

  const pyproject = files.find((f) => f.relativePath === "pyproject.toml");
  const requirements = files.find((f) => f.relativePath === "requirements.txt");
  if (pyproject || requirements) {
    prereqs.push("Python 3.8+");
    if (files.some((f) => f.content.includes("uv "))) {
      prereqs.push("uv (Python package manager)");
    } else {
      prereqs.push("pip");
    }
  }

  const docker = files.find((f) => f.relativePath.includes("docker-compose"));
  if (docker) {
    prereqs.push("Docker + Docker Compose");
  }

  const cargo = files.find((f) => f.relativePath === "Cargo.toml");
  if (cargo) {
    prereqs.push("Rust toolchain (rustc + cargo)");
  }

  return [...new Set(prereqs)];
}

function deriveSetupCommands(files: ScannedFile[]): string[] {
  const commands: string[] = [];

  // Check for .env.example
  if (files.some((f) => f.relativePath.includes(".env.example"))) {
    commands.push("cp .env.example .env  # Then fill in required values");
  }

  // Docker compose
  if (files.some((f) => f.relativePath.includes("docker-compose"))) {
    commands.push("docker compose up -d");
  }

  // Node.js
  const pkg = files.find((f) => f.relativePath === "package.json");
  if (pkg) {
    commands.push("npm install");

    try {
      const parsed = JSON.parse(pkg.content);
      const scripts = parsed.scripts || {};

      // Database setup
      if (scripts["db:push"]) commands.push("npm run db:push");
      if (scripts["db:migrate"]) commands.push("npm run db:migrate");
      if (scripts["prisma:migrate"]) commands.push("npm run prisma:migrate");

      // Build step if needed
      if (scripts["prepare"]) commands.push("npm run prepare");
    } catch { /* skip */ }
  }

  // Python
  const requirements = files.find((f) => f.relativePath === "requirements.txt");
  if (requirements) {
    if (files.some((f) => f.content.includes("uv "))) {
      commands.push("uv venv .venv && uv pip install -r requirements.txt");
    } else {
      commands.push("python -m venv .venv && pip install -r requirements.txt");
    }
  }

  return commands;
}

function deriveRunCommand(files: ScannedFile[]): string | undefined {
  const pkg = files.find((f) => f.relativePath === "package.json");
  if (pkg) {
    try {
      const parsed = JSON.parse(pkg.content);
      const scripts = parsed.scripts || {};
      if (scripts.dev) return "npm run dev";
      if (scripts.start) return "npm start";
      if (scripts.serve) return "npm run serve";
    } catch { /* skip */ }
  }

  // Python
  const procfile = files.find((f) => f.relativePath === "Procfile");
  if (procfile) {
    const webLine = procfile.content.split("\n").find((l) => l.startsWith("web:"));
    if (webLine) return webLine.replace("web:", "").trim();
  }

  return undefined;
}

function deriveTestCommand(files: ScannedFile[]): string | undefined {
  const pkg = files.find((f) => f.relativePath === "package.json");
  if (pkg) {
    try {
      const parsed = JSON.parse(pkg.content);
      if (parsed.scripts?.test) return "npm test";
    } catch { /* skip */ }
  }

  // Python tests
  if (files.some((f) => f.isTest && f.extension === ".py")) {
    // Find the test directory
    const testDirs = new Set(
      files.filter((f) => f.isTest && f.extension === ".py")
        .map((f) => f.relativePath.split("/").slice(0, -1).join("/"))
    );
    if (testDirs.size === 1) {
      return `pytest ${[...testDirs][0]}/ -v`;
    }
    return "pytest -v";
  }

  return undefined;
}

function extractRequiredEnvVars(files: ScannedFile[]): EnvVarEntry[] {
  const envVars: EnvVarEntry[] = [];
  const seen = new Set<string>();

  // From .env.example
  const envExample = files.find((f) =>
    f.relativePath.includes(".env.example") || f.relativePath.includes(".env.sample")
  );

  if (envExample) {
    const lines = envExample.content.split("\n");
    for (const line of lines) {
      const match = line.match(/^([A-Z][A-Z0-9_]+)\s*=/);
      if (match && !seen.has(match[1])) {
        seen.add(match[1]);
        const comment = line.includes("#") ? line.split("#")[1].trim() : "";
        envVars.push({
          name: match[1],
          description: comment || `Required by the application`,
          required: !line.includes("optional") && !line.includes("# optional"),
          source: envExample.relativePath,
        });
      }
    }
  }

  // From code (env vars accessed without defaults)
  for (const file of files) {
    if (file.isDoc || file.isConfig) continue;

    // process.env.X without fallback
    const matches = file.content.matchAll(/process\.env\.([A-Z][A-Z0-9_]+)(?!\s*\|\||\s*\?\?)/g);
    for (const match of matches) {
      if (!seen.has(match[1]) && !isCommonEnvVar(match[1])) {
        seen.add(match[1]);
        envVars.push({
          name: match[1],
          description: `Used in ${file.relativePath} without default value`,
          required: true,
          source: file.relativePath,
        });
      }
    }
  }

  return envVars;
}

function deriveFirstThing(files: ScannedFile[]): string {
  // The single most important thing a new developer needs to know
  const hasDocker = files.some((f) => f.relativePath.includes("docker-compose"));
  const hasEnvExample = files.some((f) => f.relativePath.includes(".env.example"));
  const hasPythonAndNode = files.some((f) => f.extension === ".py") && files.some((f) => f.extension === ".ts" || f.extension === ".js");

  if (hasPythonAndNode) {
    return "This is a polyglot project (TypeScript + Python). Both runtimes must be set up before anything works.";
  }
  if (hasDocker && hasEnvExample) {
    return "Copy .env.example to .env and run docker compose up before anything else. The app depends on external services.";
  }
  if (hasDocker) {
    return "Docker Compose must be running before the app starts. It depends on containerized services.";
  }
  if (hasEnvExample) {
    return "Copy .env.example to .env and fill in the required values before running the app.";
  }

  return "Check the README for setup instructions.";
}

function isCommonEnvVar(name: string): boolean {
  const common = new Set([
    "NODE_ENV", "PORT", "HOST", "HOME", "PATH", "USER",
    "DEBUG", "LOG_LEVEL", "TZ", "LANG", "CI",
  ]);
  return common.has(name);
}
