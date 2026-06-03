# Patent Claims — sourcetrace

**Product:** sourcetrace — Automated Truth-Extraction Engine  
**Inventor:** Haley Ann Bird (sole)  
**Organization:** Swixixle / sENZ5hFx  
**Disclosure Date:** 2026-05-18  
**License:** Business Source License 1.1 — Change Date: 2029-05-18 → Apache 2.0  

---

## Prior Art Statement

To the best of the inventor's knowledge, no prior art exists that discloses the specific combination of methods described below. Prior art searches were conducted via USPTO, Google Patents, arXiv, and GitHub as of the disclosure date. All four inventions below are believed to be novel and non-obvious.

---

## Claim 1 — Static-Behavioral Divergence Detector

A system and method for automatically detecting divergence between static documentation (README, docstrings, comments, changelogs) and observed runtime behavioral signals (test outputs, API response schemas, error logs, CI artifacts) within a software repository, comprising:

- A multi-source ingestion layer that parses documentation artifacts and runtime artifacts from the same repository into a unified canonical schema;
- A divergence scoring engine that computes a per-claim confidence score for each documented assertion against runtime evidence;
- A structured output layer that emits a ranked list of "documentation lies" — documented claims with evidence of falsity or absence of supporting runtime evidence;
- A configurable threshold system that classifies divergences as critical, warning, or informational.

## Claim 2 — Footgun Surface Mapper

A system and method for automatically identifying and ranking dangerous usage patterns ("footguns") within a codebase by:

- Parsing source code, test files, and issue history to extract patterns associated with prior failures, exceptions, or misuse;
- Scoring each identified pattern by frequency, severity of downstream consequence, and visibility in documentation;
- Emitting a structured "footgun map" that assigns each dangerous pattern a canonical location, usage context, and recommended mitigation;
- Integrating with onboarding documentation generators to surface footgun warnings at the point of first developer contact.

## Claim 3 — Structured Reality Map Generator

A system and method for transforming an arbitrary software codebase into a machine-readable and human-readable "reality map" that distinguishes:

- Guaranteed behaviors (backed by tests, contracts, or formal verification);
- Assumed behaviors (present in documentation but untested);
- Unknown behaviors (code paths with no documentation or test coverage);
- Dangerous behaviors (code paths with known failure modes);

where the map is generated fully automatically without human annotation and is exportable as structured JSON for downstream consumption by onboarding tools, AI assistants, and audit systems.

## Claim 4 — Truth Pack Protocol

A method for packaging the output of a codebase truth-extraction run into a versioned, signed, portable artifact ("truth pack") comprising:

- A canonical reality map as defined in Claim 3;
- A divergence report as defined in Claim 1;
- A footgun map as defined in Claim 2;
- A provenance block recording the source commit SHA, extraction timestamp, extractor version, and operator identity;
- A schema version identifier enabling downstream consumers to validate compatibility;

such that a truth pack can be consumed by any conforming downstream tool (e.g., onboarding guide renderers, AI context injectors, audit dashboards) without access to the original source repository.

---

## Inventorship Statement

I, Haley Ann Bird, conceived of and reduced to practice all four inventions described herein without co-inventors. Conception date: on or about 2026-05-18. First reduction to practice evidenced by the initial commit SHA in this repository.

---

*Haley Ann Bird — sole inventor*  
*Fishers, Indiana, USA*  
*2026-05-18*
