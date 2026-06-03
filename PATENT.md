# Patent Claims — Sourcetrace

**Product:** Sourcetrace — Automated Truth-Extraction Engine
**Inventor:** Haley Ann Bird (sole)
**Organization:** Swixixle / sENZ5hFx
**Disclosure Date:** 2026-05-18
**License:** Business Source License 1.1 — Change Date: 2029-05-18 → Apache 2.0

---

## Prior Art Statement

To the best of the inventor's knowledge as of the disclosure date, no prior art exists that anticipates the combination of claims described herein. The inventor has conducted a good-faith prior art search and believes the following claims describe novel, non-obvious, and useful inventions.

---

## Claim 1 — Structural Reality Extraction Engine

A system and method for automatically extracting verified structural facts from a software codebase comprising:
- Static analysis of source files to identify what a system actually guarantees vs. what documentation claims;
- A divergence detection layer that flags contradictions between declared interfaces and implemented behavior;
- Output of a machine-readable "truth pack" representing the verified reality of the codebase at a point in time;
- A diff engine that computes truth pack deltas across commits to surface behavioral regressions.

Novel aspect: the combination of (a) behavioral claim extraction, (b) doc-vs-implementation divergence detection, and (c) versioned truth pack output in a single automated pipeline.

---

## Claim 2 — Footgun Detection and Annotation System

A method for automatically identifying and annotating dangerous code patterns ("footguns") in a software repository comprising:
- Pattern matching against a configurable footgun taxonomy;
- Severity scoring with configurable thresholds;
- Inline annotation generation linking each footgun to the truth pack node it affects;
- A suppression audit trail recording which footguns were acknowledged vs. unresolved.

Novel aspect: the integration of footgun detection output directly into a structured truth pack as first-class annotated nodes.

---

## Claim 3 — Interactive Onboarding Guide Generator

A system for transforming a truth pack into an explorable onboarding experience comprising:
- Automatic narrative generation describing what a codebase does in plain language;
- Progressive disclosure rendering: high-level overview → module detail → implementation reality;
- Footgun and divergence markers surfaced inline within the onboarding flow;
- A "start here" path recommendation derived from the truth pack's dependency graph.

Novel aspect: the use of a verified truth pack (not raw source or docs) as the sole input for onboarding guide generation.

---

## Claim 4 — Cross-Codebase Truth Pack Federation

A method for federating truth packs across multiple repositories into a unified multi-project reality map comprising:
- Truth pack ingestion from N independent repositories;
- Cross-repo dependency resolution using declared interfaces and truth pack exports;
- A unified graph encoding verified inter-project relationships and cross-boundary divergences;
- An update propagation mechanism that re-derives affected downstream truth packs when an upstream pack changes.

Novel aspect: the combination of federated truth pack ingestion, cross-boundary divergence detection, and dependency-aware update propagation.

---

## Enforcement

All claims herein are the exclusive property of Haley Ann Bird. Unauthorized use constitutes patent infringement and/or trade secret misappropriation under DTSA (18 U.S.C. § 1836).

*Haley Ann Bird — sole inventor — Fishers, Indiana, USA — 2026-05-18*
