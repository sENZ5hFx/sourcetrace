/**
 * Test Reader Analyzer
 *
 * Reads test files and extracts what the system actually guarantees.
 * This is the most valuable analyzer — tests are the truth map to correctness.
 */

import type { AnalyzerOptions, AnalyzerResult, Guarantee } from "../types.js";
import type { ScannedFile } from "../utils/fs.js";

interface TestFileAnalysis {
  file: string;
  framework: "vitest" | "jest" | "pytest" | "mocha" | "unknown";
  tests: ExtractedTest[];
}

interface ExtractedTest {
  name: string;
  line: number;
  assertions: string[];
  description: string;
}

export async function readTests(
  files: ScannedFile[],
  options: AnalyzerOptions
): Promise<AnalyzerResult<Guarantee[]>> {
  const startTime = Date.now();
  const testFiles = files.filter((f) => f.isTest);
  const guarantees: Guarantee[] = [];
  const filesRead: string[] = [];

  for (const file of testFiles) {
    filesRead.push(file.relativePath);
    const analysis = analyzeTestFile(file);

    for (const test of analysis.tests) {
      guarantees.push({
        id: `guarantee-${guarantees.length + 1}`,
        description: test.name,
        source_file: file.relativePath,
        source_line: test.line,
        assertion_type: inferAssertionType(test, file),
        what_it_proves: test.description || inferProof(test),
        confidence: test.assertions.length > 0 ? "high" : "medium",
      });
    }
  }

  return {
    data: guarantees,
    files_read: filesRead,
    duration_ms: Date.now() - startTime,
  };
}

function analyzeTestFile(file: ScannedFile): TestFileAnalysis {
  const framework = detectFramework(file);
  const tests = extractTests(file, framework);

  return {
    file: file.relativePath,
    framework,
    tests,
  };
}

function detectFramework(file: ScannedFile): TestFileAnalysis["framework"] {
  const content = file.content;

  if (content.includes("from 'vitest'") || content.includes("from \"vitest\"") || (content.includes("import {") && content.includes("vitest"))) {
    return "vitest";
  }
  if (content.includes("@jest") || content.includes("jest.mock")) {
    return "jest";
  }
  if (file.extension === ".py" && (content.includes("def test_") || content.includes("import pytest"))) {
    return "pytest";
  }
  if (content.includes("describe(") || content.includes("it(")) {
    return "mocha";
  }
  return "unknown";
}

function extractTests(file: ScannedFile, framework: string): ExtractedTest[] {
  const tests: ExtractedTest[] = [];
  const lines = file.content.split("\n");

  if (framework === "pytest") {
    return extractPythonTests(lines);
  }

  return extractJSTests(lines);
}

function extractPythonTests(lines: string[]): ExtractedTest[] {
  const tests: ExtractedTest[] = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const match = line.match(/^(?:async\s+)?def\s+(test_\w+)/);

    if (match) {
      const name = match[1];
      const assertions = extractPythonAssertions(lines, i);
      const docstring = extractPythonDocstring(lines, i);

      tests.push({
        name,
        line: i + 1,
        assertions,
        description: docstring || inferFromTestName(name),
      });
    }
  }

  return tests;
}

function extractJSTests(lines: string[]): ExtractedTest[] {
  const tests: ExtractedTest[] = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    // Match it("...", ...) or test("...", ...)
    const match = line.match(/(?:it|test)\s*\(\s*["'`]([^"'`]+)["'`]/);

    if (match) {
      const name = match[1];
      const assertions = extractJSAssertions(lines, i);

      tests.push({
        name,
        line: i + 1,
        assertions,
        description: name,
      });
    }
  }

  return tests;
}

function extractPythonAssertions(lines: string[], startLine: number): string[] {
  const assertions: string[] = [];
  const indentMatch = lines[startLine].match(/^(\s*)/);
  const baseIndent = indentMatch ? indentMatch[1].length : 0;

  for (let i = startLine + 1; i < lines.length; i++) {
    const line = lines[i];
    const lineIndent = line.match(/^(\s*)/)?.[1].length ?? 0;

    // Stop at dedent
    if (line.trim() && lineIndent <= baseIndent) break;

    if (line.includes("assert ") || line.includes("assertEqual") || line.includes("assertRaises")) {
      assertions.push(line.trim());
    }
  }

  return assertions;
}

function extractJSAssertions(lines: string[], startLine: number): string[] {
  const assertions: string[] = [];
  let braceDepth = 0;

  for (let i = startLine; i < lines.length; i++) {
    const line = lines[i];
    braceDepth += (line.match(/\{/g) || []).length;
    braceDepth -= (line.match(/\}/g) || []).length;

    if (braceDepth <= 0 && i > startLine) break;

    if (line.includes("expect(") || line.includes("assert") || line.includes("toBe") || line.includes("toEqual")) {
      assertions.push(line.trim());
    }
  }

  return assertions;
}

function extractPythonDocstring(lines: string[], startLine: number): string {
  for (let i = startLine + 1; i < Math.min(startLine + 5, lines.length); i++) {
    const line = lines[i].trim();
    if (line.startsWith('"""') || line.startsWith("'''")) {
      const content = line.replace(/^(?:"""|''')|(?:"""|''')$/g, "").trim();
      if (content) return content;
      // Multi-line docstring
      for (let j = i + 1; j < lines.length; j++) {
        if (lines[j].includes('"""') || lines[j].includes("'''")) {
          return lines.slice(i + 1, j).map((l) => l.trim()).join(" ").trim();
        }
      }
    }
  }
  return "";
}

function inferFromTestName(name: string): string {
  return name
    .replace(/^test_/, "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c);
}

function inferAssertionType(test: ExtractedTest, file: ScannedFile): Guarantee["assertion_type"] {
  const path = file.relativePath.toLowerCase();
  const name = test.name.toLowerCase();

  if (path.includes("contract") || name.includes("contract")) return "contract";
  if (path.includes("integration") || name.includes("integration") || name.includes("e2e")) return "integration";
  if (name.includes("invariant") || name.includes("must") || name.includes("always")) return "invariant";
  return "unit";
}

function inferProof(test: ExtractedTest): string {
  if (test.assertions.length === 0) return `Test exists but contains no visible assertions`;

  // Try to derive meaning from assertion content
  const firstAssertion = test.assertions[0];
  if (firstAssertion.includes("==")) {
    const parts = firstAssertion.split("==").map((p) => p.trim());
    return `Verifies that ${parts[0]} equals ${parts[1]}`;
  }

  return `Verifies ${test.assertions.length} assertion(s) about: ${test.name}`;
}
