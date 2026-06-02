# Patent Disclosure — Sourcetrace

**Product:** Sourcetrace — Automated Truth-Extraction Engine  
**Inventor:** Haley Ann Bird (sole)  
**Organization:** Swixixle / sENZ5hFx  
**Disclosure Date:** 2026-05-18  
**License:** Business Source License 1.1 — Change Date: 2029-05-18 → Apache 2.0  

---

## Patent Claims

### Claim 1: Guarantee-Scoped Static Analysis Pipeline

A system and method for analyzing source code repositories to extract only what the system *actually guarantees at runtime*, comprising:
- Static traversal of entry points, route definitions, middleware chains, and exported interfaces;
- Automated detection of discrepancies between documentation assertions and code-level guarantees;
- Structured output of a "reality map" distinguishing guaranteed behavior from aspirational documentation;
- Footgun detection: automated flagging of dangerous defaults, silent failure modes, and missing error boundaries.

Novel aspect: the explicit separation of *what is guaranteed* vs *what is documented* as a first-class output artifact.

### Claim 2: Cross-Codebase Truth Pack Schema

A portable, versioned data schema ("truth pack") for encoding the extracted reality map of any codebase, comprising:
- Normalized representations of guarantees, lies, footguns, and unknowns;
- Source-location anchors (file, line, symbol) for every extracted claim;
- Compatibility metadata enabling downstream consumers (onboarding tools, documentation generators, AI systems) to consume truth packs without re-analyzing source;
- Incremental update semantics: truth packs can be diffed and patched as the codebase evolves.

Novel aspect: the truth pack as a portable, diff-able, source-anchored IP artifact separable from the analysis engine.

### Claim 3: Lie Detection Engine

A method for automatically identifying contradictions between natural-language documentation and executable code behavior, comprising:
- Extraction of claims from README, docstrings, and inline comments;
- Cross-reference of extracted claims against static analysis of actual code paths;
- Classification of each claim as: verified, unverified, contradicted, or unknown;
- Emission of a structured "lie report" with severity scores and source anchors.

Novel aspect: automated claim-level contradiction detection between prose documentation and code semantics as a pipeline output.

### Claim 4: Onboarding Fear-Surface Mapper

A system for computing the "fear surface" of a codebase — the set of entry points, abstractions, and patterns most likely to confuse or block a new developer — comprising:
- Complexity scoring of public interfaces weighted by documentation quality;
- Detection of implicit contracts (behaviors assumed but not stated);
- Ranking of modules by onboarding friction score;
- Export of fear-surface map for consumption by adaptive onboarding UI systems.

Novel aspect: fear surface as a computable, ranked, exportable metric derived from static analysis.

---

## Prior Art Statement

Inventor has reviewed available prior art including static analysis tools (pylint, mypy, semgrep), documentation linters, and onboarding platforms. None implement guarantee-scoped truth extraction, lie detection at the claim level, or fear-surface mapping as defined above. Conception date: 2026-05-18. First reduction to practice: initial commit in this repository.

---

*Haley Ann Bird — sole inventor*  
*Fishers, Indiana, USA*  
*2026-05-18*
