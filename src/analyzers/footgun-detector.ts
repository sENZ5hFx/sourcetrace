/**
 * Footgun Detector Analyzer
 *
 * Surfaces implicit constraints that will break developers:
 * - Path hacks (sys.path.insert, __dirname tricks)
 * - Undocumented env vars required at runtime
 * - "Must run from root" constraints
 * - Magic constants
 * - Platform-specific assumptions
 */

import type { AnalyzerOptions, AnalyzerResult, Footgun } from "../types.js";
import type { ScannedFile } from "../utils/fs.js";

export async function detectFootguns(
  files: ScannedFile[],
  options: AnalyzerOptions
): Promise<AnalyzerResult<Footgun[]>> {
  const startTime = Date.now();
  const footguns: Footgun[] = [];
  const filesRead: string[] = [];

  for (const file of files) {
    if (file.isDoc) continue;
    filesRead.push(file.relativePath);

    const detected = [
      ...detectPathHacks(file),
      ...detectImplicitEnvVars(file, files),
      ...detectRunOrderConstraints(file),
      ...detectMagicConstants(file),
      ...detectPlatformAssumptions(file),
    ];

    footguns.push(...detected);
  }

  return {
    data: footguns,
    files_read: filesRead,
    duration_ms: Date.now() - startTime,
  };
}

function detectPathHacks(file: ScannedFile): Footgun[] {
  const footguns: Footgun[] = [];
  const lines = file.content.split("\n");

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Python sys.path manipulation
    if (line.includes("sys.path.insert") || line.includes("sys.path.append")) {
      const parentMatch = line.match(/parents\[(\d+)\]/);
      const depth = parentMatch ? parseInt(parentMatch[1]) : null;

      footguns.push({
        id: `footgun-path-${file.relativePath}-${i}`,
        description: `sys.path manipulation${depth !== null ? ` (goes ${depth} levels up)` : ""}`,
        source_file: file.relativePath,
        source_line: i + 1,
        category: "path-hack",
        impact: depth !== null
          ? `This file must be run from a specific directory (${depth} levels above the file). Running from the wrong directory will cause all imports to fail.`
          : "Path manipulation may cause import failures depending on working directory.",
        mitigation: "Run commands from the repository root, or convert to proper package with __init__.py and pip install -e .",
      });
    }

    // Node.js __dirname hacks
    if (line.includes("__dirname") && (line.includes("..") || line.includes("resolve"))) {
      if (line.includes("../../../") || (line.match(/\.\.\//g) || []).length >= 3) {
        footguns.push({
          id: `footgun-path-${file.relativePath}-${i}`,
          description: "Deep relative path traversal from __dirname",
          source_file: file.relativePath,
          source_line: i + 1,
          category: "path-hack",
          impact: "Fragile path resolution that breaks if the file is moved. Deep traversal (3+ levels) suggests the file's location in the tree is load-bearing.",
        });
      }
    }

    // process.cwd() dependency
    if (line.includes("process.cwd()") && !file.isTest) {
      footguns.push({
        id: `footgun-cwd-${file.relativePath}-${i}`,
        description: "Relies on process.cwd() — behavior changes based on where you run it from",
        source_file: file.relativePath,
        source_line: i + 1,
        category: "implicit-constraint",
        impact: "This code assumes it's being run from a specific directory. Running from a different directory will produce different (likely broken) results.",
      });
    }
  }

  return footguns;
}

function detectImplicitEnvVars(file: ScannedFile, allFiles: ScannedFile[]): Footgun[] {
  const footguns: Footgun[] = [];

  // Find env vars used in code
  const envVarPatterns = [
    /process\.env\.([A-Z][A-Z0-9_]+)/g,
    /os\.environ\[["']([A-Z][A-Z0-9_]+)["']\]/g,
    /os\.getenv\(["']([A-Z][A-Z0-9_]+)["']\)/g,
    /env\(["']([A-Z][A-Z0-9_]+)["']\)/g,
  ];

  const usedEnvVars = new Set<string>();

  for (const pattern of envVarPatterns) {
    for (const match of file.content.matchAll(pattern)) {
      usedEnvVars.add(match[1]);
    }
  }

  // Check which ones are documented in .env.example or README
  const envExamples = allFiles.filter(
    (f) => f.relativePath.includes(".env.example") || f.relativePath.includes(".env.sample")
  );
  const docFiles = allFiles.filter((f) => f.isDoc);

  const documentedVars = new Set<string>();
  for (const envFile of [...envExamples, ...docFiles]) {
    for (const envVar of usedEnvVars) {
      if (envFile.content.includes(envVar)) {
        documentedVars.add(envVar);
      }
    }
  }

  // Flag undocumented env vars
  for (const envVar of usedEnvVars) {
    if (!documentedVars.has(envVar) && !isCommonEnvVar(envVar)) {
      footguns.push({
        id: `footgun-env-${file.relativePath}-${envVar}`,
        description: `Undocumented env var: ${envVar}`,
        source_file: file.relativePath,
        category: "undocumented-env",
        impact: `The code requires ${envVar} but it's not documented in any .env.example or README. New developers will discover this only at runtime.`,
        mitigation: `Add ${envVar} to .env.example with a description of its purpose and valid values.`,
      });
    }
  }

  return footguns;
}

function detectRunOrderConstraints(file: ScannedFile): Footgun[] {
  const footguns: Footgun[] = [];
  const lines = file.content.split("\n");

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Database migration dependencies
    if (line.match(/db:push|migrate|prisma|drizzle.*push/) && file.isConfig) {
      // Check if there's a dependency chain
      footguns.push({
        id: `footgun-order-${file.relativePath}-${i}`,
        description: "Database schema push/migration step detected",
        source_file: file.relativePath,
        source_line: i + 1,
        category: "run-order",
        impact: "This command must be run before the application starts. Running the app without pushing the schema will cause runtime crashes.",
      });
    }
  }

  return footguns;
}

function detectMagicConstants(file: ScannedFile): Footgun[] {
  const footguns: Footgun[] = [];
  const lines = file.content.split("\n");

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Version pinning that's not obvious
    if (line.match(/version.*==.*["']\d+\.\d+["']/) && !file.isConfig) {
      footguns.push({
        id: `footgun-magic-${file.relativePath}-${i}`,
        description: "Hardcoded version check in application code",
        source_file: file.relativePath,
        source_line: i + 1,
        category: "magic-constant",
        impact: "Version pinning in application code (not config) is easy to miss during upgrades. This assertion will fail silently if the version constant is updated elsewhere.",
      });
    }

    // Hardcoded ports that aren't in config
    if (line.match(/:\s*(3000|5000|8000|8080|9090)/) && !file.isConfig && !file.isDoc && !file.isTest) {
      const portMatch = line.match(/:\s*(\d{4,5})/);
      if (portMatch && !line.includes("process.env")) {
        footguns.push({
          id: `footgun-port-${file.relativePath}-${i}`,
          description: `Hardcoded port ${portMatch[1]}`,
          source_file: file.relativePath,
          source_line: i + 1,
          category: "magic-constant",
          impact: `Port ${portMatch[1]} is hardcoded rather than configurable. Will fail in environments where this port is already in use.`,
        });
      }
    }
  }

  return footguns;
}

function detectPlatformAssumptions(file: ScannedFile): Footgun[] {
  const footguns: Footgun[] = [];
  const lines = file.content.split("\n");

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Unix-specific paths in non-config files
    if (line.includes("/usr/") || line.includes("/tmp/") || line.includes("/etc/")) {
      if (!file.isConfig && !file.isDoc && !file.isTest) {
        footguns.push({
          id: `footgun-platform-${file.relativePath}-${i}`,
          description: "Unix-specific path in application code",
          source_file: file.relativePath,
          source_line: i + 1,
          category: "platform-specific",
          impact: "This path won't exist on Windows or in containerized environments with different mount points.",
        });
      }
    }
  }

  return footguns;
}

function isCommonEnvVar(name: string): boolean {
  const common = new Set([
    "NODE_ENV", "PORT", "HOST", "HOME", "PATH", "USER",
    "DATABASE_URL", "REDIS_URL", "API_URL", "BASE_URL",
    "DEBUG", "LOG_LEVEL", "TZ", "LANG",
  ]);
  return common.has(name);
}
