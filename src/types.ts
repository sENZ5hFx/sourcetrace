/**
 * Core types for the sourcetrace engine.
 * The Source Truth Pack is the canonical output artifact.
 */

export interface SourceTruthPack {
  source_truth_pack_version: string;
  target: string;
  generated_at: string;
  architecture: ArchitectureMap;
  guarantees: Guarantee[];
  contradictions: Contradiction[];
  footguns: Footgun[];
  evidence_tiers: EvidenceTiers;
  gaps: Gap[];
  quick_start: QuickStart;
  metadata: PackMetadata;
}

export interface ArchitectureMap {
  layers: ArchitectureLayer[];
  data_flow: DataFlowEdge[];
  entry_points: EntryPoint[];
  tech_stack: TechStackEntry[];
}

export interface ArchitectureLayer {
  name: string;
  description: string;
  files: string[];
  dependencies: string[];
}

export interface DataFlowEdge {
  from: string;
  to: string;
  mechanism: string; // "import" | "http" | "spawn" | "ipc" | "filesystem" | "queue"
  description?: string;
}

export interface EntryPoint {
  type: "cli" | "http" | "worker" | "script" | "test";
  path: string;
  command?: string;
  description?: string;
}

export interface TechStackEntry {
  category: "language" | "framework" | "database" | "tool" | "service";
  name: string;
  version?: string;
  source: string; // file where this was detected
}

export interface Guarantee {
  id: string;
  description: string;
  source_file: string;
  source_line?: number;
  assertion_type: "unit" | "integration" | "contract" | "invariant";
  what_it_proves: string;
  confidence: "high" | "medium" | "low";
}

export interface Contradiction {
  id: string;
  doc_claim: string;
  doc_source: string;
  code_reality: string;
  code_source: string;
  severity: "critical" | "misleading" | "stale";
  explanation: string;
}

export interface Footgun {
  id: string;
  description: string;
  source_file: string;
  source_line?: number;
  category: "path-hack" | "implicit-constraint" | "undocumented-env" | "magic-constant" | "run-order" | "platform-specific" | "other";
  impact: string;
  mitigation?: string;
}

export interface EvidenceTiers {
  evidenced: EvidenceEntry[];
  inferred: EvidenceEntry[];
  unknown: EvidenceEntry[];
}

export interface EvidenceEntry {
  claim: string;
  source?: string;
  reasoning?: string;
}

export interface Gap {
  id: string;
  area: string;
  description: string;
  severity: "critical" | "significant" | "minor";
  recommendation?: string;
}

export interface QuickStart {
  prerequisites: string[];
  setup_commands: string[];
  run_command?: string;
  test_command?: string;
  key_env_vars: EnvVarEntry[];
  first_thing_to_know: string;
}

export interface EnvVarEntry {
  name: string;
  description: string;
  required: boolean;
  source: string; // where we found this
}

export interface PackMetadata {
  analyzer_version: string;
  analysis_duration_ms: number;
  files_scanned: number;
  tests_found: number;
  llm_calls_made: number;
}

export interface AnalyzerOptions {
  target: string;
  output?: string;
  noLlm: boolean;
  verbose: boolean;
  include?: string[];
  exclude?: string[];
}

export interface AnalyzerResult<T> {
  data: T;
  files_read: string[];
  duration_ms: number;
}
