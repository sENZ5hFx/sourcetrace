# Patent Claims — Sourcetrace

**Product:** Sourcetrace — Automated Truth-Extraction & Codebase Reality Mapping Engine
**Inventor:** Haley Ann Bird (sole)
**Organization:** Swixixle / sENZ5hFx
**Disclosure Date:** 2026-05-18
**License:** Business Source License 1.1 — Change Date: 2029-05-18 → Apache 2.0

---

## Notice

One or more patent applications covering inventions described herein are pending or in preparation. Nothing in this repository constitutes a waiver of patent rights. All methods, architectures, and algorithms described herein are the exclusive property of Haley Ann Bird.

---

## Claim 1 — Automated Codebase Reality-Gap Detection Engine

A system and method for automatically detecting and surfacing divergences between
documented behavior and actual runtime behavior of a software codebase, comprising:
- Static analysis traversal of source files to extract declared contracts, documented
  invariants, and API surface descriptions;
- Dynamic instrumentation or log analysis to derive observed runtime behavior;
- A divergence-scoring engine that computes a per-module "reality gap" score
  representing the magnitude of deviation between documentation and observed behavior;
- A structured output layer that serializes reality gap findings into a machine-readable
  "truth pack" format consumable by downstream rendering or reporting tools;
- A footgun detection pass that flags high-risk divergences (security, data loss,
  silent failure) with elevated priority scores.

Novel aspects: the combination of (a) per-module reality gap scoring, (b) footgun
prioritization within the same pass, and (c) truth pack serialization as a
first-class portable artifact.

---

## Claim 2 — Source-Truth Pack Format & Portability Protocol

A structured data format and associated generation protocol for representing the
extracted ground truth of a software system, comprising:
- A versioned schema encoding: module identity, declared contracts, observed behavior,
  reality gap scores, footgun flags, dependency graph edges, and authorship metadata;
- A deterministic content-addressed identifier (SHA-256 of normalized content) per
  truth pack enabling tamper detection and deduplication;
- A portability layer allowing truth packs to be consumed by heterogeneous downstream
  tools (interactive renderers, AI onboarding agents, compliance auditors) without
  re-running the extraction engine;
- An incremental update protocol: only modules whose source hash has changed since
  the last extraction are re-analyzed, with unchanged modules inheriting prior truth pack entries.

Novel aspects: the combination of (a) content-addressed truth pack identity, (b) portability
across heterogeneous consumers, and (c) incremental update protocol tied to source hashes.

---

## Claim 3 — Lie-Detection Pass for Technical Documentation

A method for automatically classifying technical documentation claims as true, stale,
or false relative to current source code, comprising:
- Extraction of factual assertions from documentation (README, inline comments, API docs)
  using pattern matching and NLP-based claim extraction;
- Cross-referencing each extracted claim against the live source code AST, runtime
  logs, or test suite results;
- Classification of each claim into: VERIFIED (supported by code), STALE (was true
  in a prior version, no longer accurate), or FALSE (directly contradicted by code);
- Generation of a per-claim evidence record citing the specific source location
  that confirms or refutes the claim;
- Aggregation into a documentation health score with breakdown by module and severity.

Novel aspects: the combination of (a) tri-class claim verification (verified/stale/false),
(b) per-claim source-cited evidence records, and (c) documentation health scoring
within the same pipeline.

---

## Claim 4 — Interactive Fear-Free Onboarding Guide Generator

A system for generating interactive, adaptive onboarding guides from source truth packs,
comprising:
- Ingestion of a truth pack artifact as sole input (no access to live codebase required);
- Automated generation of an explorable, layered onboarding narrative that progressively
  reveals system complexity from surface to internals;
- Adaptive depth control: the guide presents a minimal safe entry path first, with
  optional drill-down into reality gap details and footgun warnings;
- Fear-free framing: footguns and reality gaps are surfaced with remediation context
  rather than raw error dumps, reducing cognitive overload for new contributors;
- Export to multiple formats: interactive web (consumed by Threshold renderer),
  static Markdown, and structured JSON for AI agent consumption.

Novel aspects: the combination of (a) truth-pack-only input (no live codebase access),
(b) adaptive depth control with safe entry path prioritization, and (c) fear-free
remediation framing as a first-class design constraint.

---

## Prior Art Statement

The inventor is not aware of any prior art that discloses the specific combination
of elements claimed herein. Existing codebase analysis tools (static analyzers, linters,
doc generators) do not perform reality-gap scoring, truth pack portability, tri-class
documentation lie detection, or fear-free adaptive onboarding generation as described.

---

*Haley Ann Bird — sole inventor*
*Fishers, Indiana, USA*
*2026-05-18*
