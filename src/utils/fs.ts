/**
 * File system utilities for scanning and reading repos.
 */

import { readFileSync, statSync, existsSync } from "fs";
import { join, relative, extname } from "path";
import fg from "fast-glob";

export interface ScanOptions {
  include?: string[];
  exclude?: string[];
}

export interface ScannedFile {
  path: string;
  relativePath: string;
  extension: string;
  size: number;
  content: string;
  isTest: boolean;
  isDoc: boolean;
  isConfig: boolean;
}

const TEST_PATTERNS = [
  /test[_\-.]/, /\.test\./, /\.spec\./,
  /_test\./, /tests\//, /__tests__\//,
  /test_.*\.py$/,
];

const DOC_EXTENSIONS = [".md", ".mdx", ".rst", ".txt", ".adoc"];
const DOC_FILENAMES = ["readme", "contributing", "changelog", "license", "architecture", "api"];

const CONFIG_FILENAMES = [
  "package.json", "tsconfig.json", "pyproject.toml", "setup.py", "setup.cfg",
  "Cargo.toml", "go.mod", "Makefile", "Dockerfile", "docker-compose.yml",
  "docker-compose.yaml", ".env.example", ".env.sample", "requirements.txt",
  "Procfile", "vercel.json", "netlify.toml", "fly.toml",
];

export async function scanFiles(rootPath: string, options: ScanOptions = {}): Promise<ScannedFile[]> {
  const patterns = options.include ?? ["**/*"];
  const ignore = options.exclude ?? ["**/node_modules/**", "**/.git/**", "**/dist/**"];

  const paths = await fg(patterns, {
    cwd: rootPath,
    ignore,
    absolute: false,
    onlyFiles: true,
    dot: true,
  });

  const files: ScannedFile[] = [];

  for (const relPath of paths) {
    const fullPath = join(rootPath, relPath);

    try {
      const stat = statSync(fullPath);
      // Skip very large files (>500KB) to avoid memory issues
      if (stat.size > 500_000) continue;

      // Skip binary files
      const ext = extname(relPath).toLowerCase();
      if (isBinaryExtension(ext)) continue;

      const content = readFileSync(fullPath, "utf-8");
      const lowerPath = relPath.toLowerCase();

      files.push({
        path: fullPath,
        relativePath: relPath,
        extension: ext,
        size: stat.size,
        content,
        isTest: TEST_PATTERNS.some((p) => p.test(lowerPath)),
        isDoc: DOC_EXTENSIONS.includes(ext) || DOC_FILENAMES.some((n) => lowerPath.includes(n)),
        isConfig: CONFIG_FILENAMES.some((n) => lowerPath.endsWith(n)),
      });
    } catch {
      // Skip unreadable files
    }
  }

  return files;
}

export function readFileContent(path: string): string | null {
  try {
    return readFileSync(path, "utf-8");
  } catch {
    return null;
  }
}

export function fileExists(path: string): boolean {
  return existsSync(path);
}

function isBinaryExtension(ext: string): boolean {
  const binaryExts = new Set([
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".exe", ".dll", ".so", ".dylib", ".o",
    ".mp3", ".mp4", ".wav", ".avi", ".mov",
    ".sqlite", ".db", ".lock",
  ]);
  return binaryExts.has(ext);
}
