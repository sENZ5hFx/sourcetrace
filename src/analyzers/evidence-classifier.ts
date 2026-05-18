/**
 * Evidence Classifier
 *
 * Categorizes every claim about the system into three tiers:
 * - EVIDENCED: Backed by a passing test or verifiable assertion
 * - INFERRED: Reasonable based on code structure, but not explicitly tested
 * - UNKNOWN: No basis in code — could be true, could be a lie
 */

import type { EvidenceTiers, EvidenceEntry, Guarantee, Contradiction, ArchitectureMap } from "../types.js";

export function classifyEvidence(
  guarantees: Guarantee[],
  contradictions: Contradiction[],
  architecture: ArchitectureMap
): EvidenceTiers {
  const evidenced: EvidenceEntry[] = [];
  const inferred: EvidenceEntry[] = [];
  const unknown: EvidenceEntry[] = [];

  // Things proven by tests are EVIDENCED
  for (const guarantee of guarantees) {
    if (guarantee.confidence === "high") {
      evidenced.push({
        claim: guarantee.what_it_proves,
        source: `${guarantee.source_file}:${guarantee.source_line || "?"}`,
        reasoning: `Directly asserted in test: ${guarantee.description}`,
      });
    } else {
      inferred.push({
        claim: guarantee.what_it_proves,
        source: guarantee.source_file,
        reasoning: `Test exists but assertions are weak or unclear`,
      });
    }
  }

  // Architecture observations are INFERRED (we see the structure but don't have proof it works)
  for (const layer of architecture.layers) {
    inferred.push({
      claim: `Layer "${layer.name}" exists and contains ${layer.files.length} files`,
      source: "Architecture scan",
      reasoning: "File structure observed but correctness not verified by tests",
    });
  }

  for (const edge of architecture.data_flow) {
    inferred.push({
      claim: `${edge.from} communicates with ${edge.to} via ${edge.mechanism}`,
      source: edge.from,
      reasoning: "Code pattern detected but integration not explicitly tested",
    });
  }

  // Contradictions reveal things that are UNKNOWN (docs say one thing, code says another)
  for (const contradiction of contradictions) {
    unknown.push({
      claim: contradiction.doc_claim,
      source: contradiction.doc_source,
      reasoning: `Contradicted by code: ${contradiction.explanation}`,
    });
  }

  return { evidenced, inferred, unknown };
}
