/**
 * Gap Mapper Analyzer
 *
 * Finds what's undocumented, untested, or silently assumed.
 * The voids in the system that nobody talks about.
 */

import type { Gap, Guarantee, ArchitectureMap, Contradiction, Footgun } from "../types.js";

export function mapGaps(
  guarantees: Guarantee[],
  architecture: ArchitectureMap,
  contradictions: Contradiction[],
  footguns: Footgun[]
): Gap[] {
  const gaps: Gap[] = [];

  // Find untested layers
  const testedFiles = new Set(guarantees.map((g) => g.source_file));
  for (const layer of architecture.layers) {
    if (layer.name === "Documentation" || layer.name === "Infrastructure") continue;

    const layerFiles = layer.files.filter((f) => !f.endsWith(".md") && !f.endsWith(".json"));
    const untestedFiles = layerFiles.filter((f) => {
      // A file is "tested" if any test references it or shares its module
      return !testedFiles.has(f);
    });

    const coverage = layerFiles.length > 0
      ? ((layerFiles.length - untestedFiles.length) / layerFiles.length * 100).toFixed(0)
      : "0";

    if (untestedFiles.length > 0 && parseInt(coverage) < 50) {
      gaps.push({
        id: `gap-coverage-${layer.name}`,
        area: `Test coverage: ${layer.name}`,
        description: `${untestedFiles.length} of ${layerFiles.length} source files have no corresponding tests (${coverage}% coverage by file count)`,
        severity: parseInt(coverage) < 20 ? "critical" : "significant",
        recommendation: `Add tests for the ${layer.name} layer, particularly: ${untestedFiles.slice(0, 5).join(", ")}`,
      });
    }
  }

  // Find undocumented entry points
  for (const entry of architecture.entry_points) {
    gaps.push({
      id: `gap-entry-${entry.path}`,
      area: "Entry point documentation",
      description: `Entry point ${entry.path} (${entry.type}) exists but may not be documented in README`,
      severity: "minor",
      recommendation: `Document how to use ${entry.path} in the README or a dedicated guide`,
    });
  }

  // Find documentation with high contradiction density
  if (contradictions.length > 3) {
    gaps.push({
      id: "gap-doc-drift",
      area: "Documentation drift",
      description: `${contradictions.length} contradictions found between docs and code. Documentation may be significantly out of date.`,
      severity: "critical",
      recommendation: "Audit all documentation against current code. Consider generating docs from source.",
    });
  }

  // Find areas with many footguns but no documentation
  const footgunsByFile = new Map<string, Footgun[]>();
  for (const fg of footguns) {
    const key = fg.source_file;
    if (!footgunsByFile.has(key)) footgunsByFile.set(key, []);
    footgunsByFile.get(key)!.push(fg);
  }

  for (const [file, fileFootguns] of footgunsByFile) {
    if (fileFootguns.length >= 3) {
      gaps.push({
        id: `gap-footgun-density-${file}`,
        area: "Footgun density",
        description: `${file} has ${fileFootguns.length} implicit constraints that are not documented. This file is a minefield for new developers.`,
        severity: "significant",
        recommendation: `Add a "CAUTION" section or inline comments explaining: ${fileFootguns.map((f) => f.description).join("; ")}`,
      });
    }
  }

  // Find data flow edges that are untested (integration gaps)
  const testedIntegrations = guarantees.filter((g) => g.assertion_type === "integration");
  if (architecture.data_flow.length > 0 && testedIntegrations.length === 0) {
    gaps.push({
      id: "gap-integration-tests",
      area: "Integration testing",
      description: `${architecture.data_flow.length} data flow edges detected but no integration tests found. The connections between components are unverified.`,
      severity: "critical",
      recommendation: "Add integration tests that verify data flows correctly between layers (e.g., API → DB, Server → subprocess).",
    });
  }

  return gaps;
}
