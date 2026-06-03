# Patent Claims — Sourcetrace
# Automated Truth-Extraction & Codebase Reality Mapping Engine

**Inventor:** Haley Ann Bird (sole)
**Organization:** Swixixle / sENZ5hFx
**Conception Date:** 2026-05-18
**Reduction to Practice:** This repository and its commit history
**License:** Business Source License 1.1 — Change Date: 2029-05-18 → Apache 2.0

---

## Claim 1 — Automated Structural Truth Extraction

A computer-implemented method for automated truth extraction from software repositories comprising:
- statically analyzing source code, configuration files, and infrastructure definitions to derive a machine-verifiable "reality map" distinct from developer-authored documentation;
- detecting contradictions between stated behavior in README/docs and actual implemented behavior in code;
- emitting a structured "truth pack" artifact encoding guaranteed behaviors, failure modes, and footguns with confidence scores;
- operating without execution or runtime instrumentation, relying solely on static analysis and semantic parsing.

Novel aspect: the explicit contradiction-detection layer between documentation claims and code reality, producing a scored discrepancy manifest.

## Claim 2 — Footgun & Failure Mode Cataloging

A system for automatically identifying and cataloging latent failure modes in software systems comprising:
- pattern-matched detection of known footgun categories (unhandled exceptions, silent failures, credential exposure vectors, race conditions) across the full codebase;
- ranking footguns by exploitability and blast radius using a configurable severity model;
- associating each footgun with the specific code location, call chain, and downstream consumers;
- emitting footgun records as structured data consumable by downstream onboarding and documentation systems.

Novel aspect: the combination of (a) footgun cataloging as a first-class pipeline output, (b) blast-radius scoring, and (c) downstream consumption interface for onboarding systems.

## Claim 3 — Source Truth Pack Format

A structured data format for encoding verified software system reality comprising fields for:
- guaranteed_behaviors: behaviors the system provably exhibits under all analyzed conditions;
- contradiction_manifest: list of documentation claims contradicted by code evidence;
- footgun_catalog: ranked list of latent failure modes with location and severity;
- dependency_reality: actual vs. declared dependency graph with version conflict detection;
- coverage_gaps: modules and code paths excluded from analysis with stated reasons.

Novel aspect: the truth_pack as a portable, versioned, machine-readable contract between a codebase and its consumers.

## Claim 4 — Onboarding Guide Generation from Truth Packs

A method for generating interactive, fear-free onboarding experiences from truth pack artifacts comprising:
- consuming a truth pack as sole input without access to the originating repository;
- rendering a guided exploration interface that surfaces safe entry points, warns on footguns, and presents the contradiction manifest as interactive callouts;
- generating a "lie detector" layer that flags discrepancies between what documentation promises and what truth pack evidence confirms.

Novel aspect: the decoupled, truth-pack-only onboarding generator that produces a lie-detector layer as a first-class UI component.

---

## Prior Art Statement

To the inventor's knowledge, no prior system combines automated contradiction detection between documentation and code reality, footgun cataloging with blast-radius scoring, and a portable truth pack format as described herein. Standard static analysis tools (ESLint, SonarQube, Semgrep) detect code defects but do not produce documentation-vs-reality contradiction manifests or truth pack artifacts.

---

*Haley Ann Bird — sole inventor*
*Fishers, Indiana, USA*
*2026-06-03*
