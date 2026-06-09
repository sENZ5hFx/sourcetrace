/**
 * Architecture Mapper Analyzer
 *
 * Builds the real architecture graph from imports, routes, and function calls.
 * Not from someone's outdated diagram — from the actual code.
 */

import type { AnalyzerOptions, AnalyzerResult, ArchitectureMap, ArchitectureLayer, DataFlowEdge, EntryPoint, TechStackEntry } from "../types.js";
import type { ScannedFile } from "../utils/fs.js";
import { basename, dirname } from "path";

export async function mapArchitecture(
  files: ScannedFile[],
  options: AnalyzerOptions
): Promise<AnalyzerResult<ArchitectureMap>> {
  const startTime = Date.now();
  const filesRead: string[] = [];

  const layers = detectLayers(files);
  const dataFlow = traceDataFlow(files);
  const entryPoints = findEntryPoints(files);
  const techStack = detectTechStack(files);

  for (const f of files) {
    filesRead.push(f.relativePath);
  }

  return {
    data: {
      layers,
      data_flow: dataFlow,
      entry_points: entryPoints,
      tech_stack: techStack,
    },
    files_read: filesRead,
    duration_ms: Date.now() - startTime,
  };
}

function detectLayers(files: ScannedFile[]): ArchitectureLayer[] {
  const dirMap = new Map<string, ScannedFile[]>();

  for (const file of files) {
    const parts = file.relativePath.split("/");
    const topDir = parts.length > 1 ? parts[0] : ".";

    dirMap.get(topDir)!.push(file);
  }

  const layers: ArchitectureLayer[] = [];

  for (const [dir, dirFiles] of dirMap) {
    const layer = classifyLayer(dir, dirFiles);
    if (layer) layers.push(layer);
  }

  return layers;
}

function classifyLayer(dir: string, files: ScannedFile[]): ArchitectureLayer | null {
  const lowerDir = dir.toLowerCase();
  const filePaths = files.map((f) => f.relativePath);

  // Client/Frontend layer
  if (lowerDir.match(/^(client|frontend|app|src\/app|web|ui|pages)/)) {
    return {
      name: "Client",
      description: inferLayerDescription(files, "client"),
      files: filePaths,
      dependencies: extractDependencies(files),
    };
  }

  // Server/Backend layer
  if (lowerDir.match(/^(server|backend|api|src\/server|routes)/)) {
    return {
      name: "Server",
      description: inferLayerDescription(files, "server"),
      files: filePaths,
      dependencies: extractDependencies(files),
    };
  }

  // Shared/Common layer
  if (lowerDir.match(/^(shared|common|lib|utils|packages)/)) {
    return {
      name: "Shared",
      description: "Cross-cutting utilities and type definitions shared between layers",
      files: filePaths,
      dependencies: extractDependencies(files),
    };
  }

  // Test layer
  if (lowerDir.match(/^(test|tests|__tests__|spec)/)) {
    return {
      name: "Tests",
      description: "Test suites and validation logic",
      files: filePaths,
      dependencies: extractDependencies(files),
    };
  }

  // Config/Infrastructure
  if (lowerDir.match(/^(config|infra|deploy|\.github|scripts)/)) {
    return {
      name: "Infrastructure",
      description: "Configuration, deployment, and CI/CD",
      files: filePaths,
      dependencies: [],
    };
  }

  // Docs
  if (lowerDir.match(/^(docs|documentation)/)) {
    return {
      name: "Documentation",
      description: "Project documentation and guides",
      files: filePaths,
      dependencies: [],
    };
  }

  // Root files
  if (dir === ".") {
    return {
      name: "Root",
      description: "Root configuration and project metadata",
      files: filePaths,
      dependencies: [],
    };
  }

  return {
    name: dir,
    description: `Module: ${dir}`,
    files: filePaths,
    dependencies: extractDependencies(files),
  };
}

function inferLayerDescription(files: ScannedFile[], type: string): string {
  const hasReact = files.some((f) => f.content.includes("import React") || f.content.includes("from 'react'"));
  const hasExpress = files.some((f) => f.content.includes("express") && f.content.includes("app."));
  const hasFastAPI = files.some((f) => f.content.includes("FastAPI") || f.content.includes("@app."));

  if (type === "client") {
    if (hasReact) return "React-based frontend application";
    return "Client-side application layer";
  }
  if (type === "server") {
    if (hasExpress) return "Express.js API server";
    if (hasFastAPI) return "FastAPI backend service";
    return "Server-side application layer";
  }
  return "Application layer";
}

function traceDataFlow(files: ScannedFile[]): DataFlowEdge[] {
  const edges: DataFlowEdge[] = [];
  const seen = new Set<string>();

  for (const file of files) {
    // Detect subprocess spawning
    if (file.content.includes("spawn(") || file.content.includes("exec(") || file.content.includes("subprocess")) {
      const key = `${file.relativePath}->subprocess`;
      if (!seen.has(key)) {
        edges.push({
          from: file.relativePath,
          to: "subprocess",
          mechanism: "spawn",
          description: "Spawns child process",
        });
        seen.add(key);
      }
    }

    // Detect HTTP calls
    if (file.content.includes("fetch(") || file.content.includes("axios") || file.content.includes("requests.")) {
      const key = `${file.relativePath}->http`;
      if (!seen.has(key)) {
        edges.push({
          from: file.relativePath,
          to: "external",
          mechanism: "http",
          description: "Makes HTTP request",
        });
        seen.add(key);
      }
    }

    // Detect filesystem writes
    if (file.content.includes("writeFile") || file.content.includes("writeFileSync") || file.content.includes("open(") && file.content.includes("'w'")) {
      const key = `${file.relativePath}->fs`;
      if (!seen.has(key)) {
        edges.push({
          from: file.relativePath,
          to: "filesystem",
          mechanism: "filesystem",
          description: "Writes to filesystem",
        });
        seen.add(key);
      }
    }

    // Detect queue/job usage
    if (file.content.includes("BullMQ") || file.content.includes("Queue(") || file.content.includes("addJob")) {
      const key = `${file.relativePath}->queue`;
      if (!seen.has(key)) {
        edges.push({
          from: file.relativePath,
          to: "job_queue",
          mechanism: "queue",
          description: "Enqueues async job",
        });
        seen.add(key);
      }
    }
  }

  return edges;
}

function findEntryPoints(files: ScannedFile[]): EntryPoint[] {
  const entryPoints: EntryPoint[] = [];

  for (const file of files) {
    // CLI entrypoints
    if (file.content.includes("#!/usr/bin/env") || file.content.includes("if __name__")) {
      entryPoints.push({
        type: "cli",
        path: file.relativePath,
        description: `CLI entrypoint: ${basename(file.relativePath)}`,
      });
    }

    // HTTP server entrypoints
    if (file.content.includes("app.listen") || file.content.includes("createServer") || file.content.includes("uvicorn.run")) {
      entryPoints.push({
        type: "http",
        path: file.relativePath,
        description: `HTTP server: ${basename(file.relativePath)}`,
      });
    }
  }

  return entryPoints;
}

function detectTechStack(files: ScannedFile[]): TechStackEntry[] {
  const stack: TechStackEntry[] = [];
  const seen = new Set<string>();

  for (const file of files) {
    if (file.relativePath === "package.json") {
      try {
        const pkg = JSON.parse(file.content);
        const deps = { ...pkg.dependencies, ...pkg.devDependencies };
        for (const [name, version] of Object.entries(deps)) {
          if (!seen.has(name)) {
            stack.push({
              category: "framework",
              name,
              version: String(version),
              source: file.relativePath,
            });
            seen.add(name);
          }
        }
      } catch { /* skip malformed */ }
    }

    if (file.relativePath === "requirements.txt") {
      const lines = file.content.split("\n").filter((l) => l.trim() && !l.startsWith("#"));
      for (const line of lines) {
        const name = line.split(/[>=<!\[]/)[0].trim();
        if (name && !seen.has(name)) {
          stack.push({
            category: "framework",
            name,
            source: file.relativePath,
          });
          seen.add(name);
        }
      }
    }
  }

  // Detect languages from file extensions
  const extCounts = new Map<string, number>();
  for (const file of files) {
    if (!file.isConfig && !file.isDoc) {
      extCounts.set(file.extension, (extCounts.get(file.extension) || 0) + 1);
    }
  }

  const langMap: Record<string, string> = {
    ".ts": "TypeScript", ".tsx": "TypeScript (React)", ".js": "JavaScript",
    ".py": "Python", ".rs": "Rust", ".go": "Go", ".rb": "Ruby",
    ".java": "Java", ".kt": "Kotlin", ".swift": "Swift",
  };

  for (const [ext, count] of extCounts) {
    if (langMap[ext] && count > 0 && !seen.has(langMap[ext])) {
      stack.push({
        category: "language",
        name: langMap[ext],
        source: `${count} files with ${ext} extension`,
      });
      seen.add(langMap[ext]);
    }
  }

  return stack;
}

function extractDependencies(files: ScannedFile[]): string[] {
  const deps = new Set<string>();

  for (const file of files) {
    // JS/TS imports
    const jsImports = file.content.matchAll(/(?:import|require)\s*\(?["']([^"'./][^"']*)["']/g);
    for (const match of jsImports) {
      deps.add(match[1].split("/")[0]);
    }

    // Python imports
    const pyImports = file.content.matchAll(/(?:from|import)\s+(\w+)/g);
    for (const match of pyImports) {
      if (!["os", "sys", "re", "json", "typing", "pathlib", "unittest", "pytest"].includes(match[1])) {
        deps.add(match[1]);
      }
    }
  }

  return [...deps].slice(0, 50); // Cap at 50 to avoid noise
}
