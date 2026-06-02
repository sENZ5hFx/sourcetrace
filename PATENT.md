# Patent Claims — Sourcetrace

**Product:** Sourcetrace — Automated Truth-Extraction & Codebase Reality Mapping Engine  
**Inventor:** Haley Ann Bird (sole)  
**Organization:** Swixixle / sENZ5hFx  
**Disclosure Date:** 2026-05-18  
**License:** Business Source License 1.1 — Change Date: 2029-05-18 → Apache 2.0  

---

## Patent Claim 1 — Automated Truth-Extraction Engine

A method and system for automatically extracting verified behavioral claims from a software codebase, comprising:
- Static and dynamic analysis passes that produce a structured 'reality map' distinguishing what a system actually guarantees from what its documentation claims;
- A contradiction detector that flags divergences between documented behavior and observed code paths;
- A footgun detector that identifies dangerous or undocumented failure modes in the codebase;
- Output serialization into a portable 'truth pack' format consumable by downstream rendering systems.

## Patent Claim 2 — Source Truth Pack Protocol

A data structure and serialization protocol for representing codebase reality maps, comprising:
- A versioned schema encoding verified guarantees, known failure modes, documentation contradictions, and dependency surface;
- A provenance field recording the exact commit SHA, timestamp, and analysis engine version that produced each claim;
- A machine-readable format enabling downstream onboarding interfaces to render interactive, fear-free exploration experiences without re-analyzing the source.

## Patent Claim 3 — Multi-Codebase Orchestrated Analysis

A system for orchestrated simultaneous analysis of multiple software repositories, comprising:
- A centralized orchestrator that dispatches analysis jobs to per-repo truth-extraction agents;
- A cross-repo contradiction surface that identifies interfaces where one repo's guarantees conflict with another's assumptions;
- A unified truth pack aggregation layer producing a multi-project reality map from individual per-repo truth packs.

## Patent Claim 4 — Adaptive Onboarding Guide Generator

A method for generating adaptive, developer-personalized onboarding guides from truth packs, comprising:
- Personalization signals derived from the developer's prior interaction history and declared expertise level;
- Dynamic section ordering that surfaces highest-risk footguns first for safety-critical onboarding;
- Live refresh that re-generates affected guide sections when the underlying truth pack changes.

---

## Prior Art Statement

To the best of the inventor's knowledge, no prior art exists for the combination of (a) automated contradiction detection between documentation and code behavior, (b) the truth pack serialization protocol, and (c) adaptive footgun-first onboarding guide generation from static analysis outputs.

---

*Haley Ann Bird — sole inventor*  
*Fishers, Indiana, USA*  
*2026-05-18*
