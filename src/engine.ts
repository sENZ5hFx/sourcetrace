/**
 * Core engine orchestrator.
 * Runs all analyzers against a target repo and assembles the source truth pack.
 */

import type { AnalyzerOptions, SourceTruthPack, PackMetadata } from "./types.js";
import { scanFiles } from "./utils/fs.js";
import { readTests } from "./analyzers/test-reader.js";
import { mapArchitecture } from "./analyzers/arch-mapper.js";
import { diffDocs } from "./analyzers/doc-differ.js";
import { detectFootguns } from "./analyzers/footgun-detector.js";
import { classifyEvidence } from "./analyzers/evidence-classifier.js";
import { mapGaps } from "./analyzers/gap-mapper.js";
import { extractQuickStart } from "./analyzers/quickstart-extractor.js";

export async function runEngine(options: AnalyzerOptions): Promise<SourceTruthPack> {
  const startTime = Date.now();

  if (options.verbose) {
    console.error("[sourcetrace] Scanning files...");
  }

  const files = await scanFiles(options.target, {
    include: options.include,
    exclude: options.exclude ?? ["**/node_modules/**", "**/.git/**", "**/dist/**", "**/build/**", "**/__pycache__/**"],
  });

  if (options.verbose) {
    console.error(`[sourcetrace] Found ${files.length} files`);
  }

  // Run analyzers in parallel where possible
  const [testResults, archResults, docResults, footgunResults] = await Promise.all([
    readTests(files, options),
    mapArchitecture(files, options),
    diffDocs(files, options),
    detectFootguns(files, options),
  ]);

  // Evidence classification depends on test + doc results
  const evidenceResults = classifyEvidence(
    testResults.data,
    docResults.data,
    archResults.data
  );

  // Gap mapping depends on all prior results
  const gapResults = mapGaps(
    testResults.data,
    archResults.data,
    docResults.data,
    footgunResults.data
  );

  // Quick start extraction
  const quickStart = await extractQuickStart(files, options);

  const duration = Date.now() - startTime;

  const metadata: PackMetadata = {
    analyzer_version: "0.1.0",
    analysis_duration_ms: duration,
    files_scanned: files.length,
    tests_found: testResults.data.length,
    llm_calls_made: 0, // TODO: track when LLM mode is implemented
  };

  const pack: SourceTruthPack = {
    source_truth_pack_version: "1.0",
    target: options.target,
    generated_at: new Date().toISOString(),
    architecture: archResults.data,
    guarantees: testResults.data,
    contradictions: docResults.data,
    footguns: footgunResults.data,
    evidence_tiers: evidenceResults,
    gaps: gapResults,
    quick_start: quickStart,
    metadata,
  };

  if (options.verbose) {
    console.error(`[sourcetrace] Analysis complete in ${duration}ms`);
    console.error(`[sourcetrace] Guarantees: ${pack.guarantees.length}`);
    console.error(`[sourcetrace] Contradictions: ${pack.contradictions.length}`);
    console.error(`[sourcetrace] Footguns: ${pack.footguns.length}`);
    console.error(`[sourcetrace] Gaps: ${pack.gaps.length}`);
  }

  return pack;
}
