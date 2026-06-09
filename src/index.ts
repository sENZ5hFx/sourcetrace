/**
 * sourcetrace - Automated truth-extraction for any codebase.
 *
 * Public API for programmatic usage.
 */

export { runEngine } from "./engine.js";
export type {
  SourceTruthPack,
  AnalyzerOptions,
  Guarantee,
  Contradiction,
  Footgun,
  Gap,
  EvidenceTiers,
  ArchitectureMap,
  QuickStart,
  PackMetadata,
} from "./types.js";
