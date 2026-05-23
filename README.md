# sourcetrace

**Automated truth-extraction for any codebase.**

sourcetrace reads your actual source code — tests, imports, routes, config — and produces a structured "source truth pack" that tells you what the system *really* guarantees, where the docs lie, and where the footguns hide.

---

## Philosophy

> Excellence isn't about fixing broken things. It's about owning and elevating the acceptable — turning hidden compromises into architectures of deliberate, resilient, and imaginative design.

Most documentation describes what someone *intended* to build. sourcetrace describes what *actually exists* — derived from code, not from memory or assumption.

---

## What It Does

| Analyzer | What It Finds |
|----------|---------------|
| **Test Reader** | What the system actually guarantees. Extracts assertions, invariants, and correctness models from test files. |
| **Architecture Mapper** | The real dependency graph and data flow — built from imports, routes, and function calls, not from outdated diagrams. |
| **Doc Differ** | Where documentation contradicts code. Finds staleness, lies, and drift. |
| **Footgun Detector** | Implicit constraints that will break you: path hacks, undocumented env vars, run-from-root requirements, magic constants. |
| **Evidence Classifier** | Categorizes every claim as EVIDENCED (tested), INFERRED (reasonable but unverified), or UNKNOWN (no basis). |
| **Gap Mapper** | What's undocumented, untested, or silently assumed. The voids. |

---

## Output: The Source Truth Pack

```json
{
  "source_truth_pack_version": "1.0",
  "target": "path/to/repo",
  "generated_at": "2026-05-18T19:30:00Z",
  "architecture": { ... },
  "guarantees": [ ... ],
  "contradictions": [ ... ],
  "footguns": [ ... ],
  "evidence_tiers": {
    "evidenced": [ ... ],
    "inferred": [ ... ],
    "unknown": [ ... ]
  },
  "gaps": [ ... ],
  "quick_start": { ... }
}
```

This artifact is consumed by [threshold](https://github.com/sENZ5hFx/threshold) (the beautiful interface) and managed by [firstlight](https://github.com/sENZ5hFx/firstlight) (the orchestrator).

---

## Usage

```bash
# Analyze a local repo
sourcetrace analyze ./path/to/repo

# Output to a specific file
sourcetrace analyze ./path/to/repo -o truth-pack.json

# Analyze without LLM calls (fast, local-only)
sourcetrace analyze ./path/to/repo --no-llm

# Run as a GitHub Action (see .github/workflows/)
```

---

## Architecture

```
sourcetrace/
├── src/
│   ├── cli.ts              # CLI entrypoint
│   ├── engine.ts           # Core orchestrator
│   ├── analyzers/
│   │   ├── test-reader.ts      # Extract guarantees from tests
│   │   ├── arch-mapper.ts      # Build real architecture graph
│   │   ├── doc-differ.ts       # Find doc-vs-code contradictions
│   │   ├── footgun-detector.ts # Surface implicit constraints
│   │   ├── evidence-classifier.ts  # Tier every claim
│   │   └── gap-mapper.ts       # Find the voids
│   ├── parsers/
│   │   ├── python.ts       # Python AST parsing
│   │   ├── typescript.ts   # TypeScript AST parsing
│   │   └── generic.ts      # Regex/heuristic fallback
│   ├── output/
│   │   └── truth-pack.ts   # Schema + serialization
│   └── utils/
│       ├── fs.ts           # File system helpers
│       └── git.ts          # Git history helpers
├── tests/
├── package.json
├── tsconfig.json
└── README.md
```

---

## Part of the System

| Product | Role |
|---------|------|
| **sourcetrace** (this) | The engine — reads code, produces truth |
| [threshold](https://github.com/sENZ5hFx/threshold) | The shell — makes truth beautiful and explorable |
| [firstlight](https://github.com/sENZ5hFx/firstlight) | The orchestrator — connects repos, runs continuously, serves the portal |

---

## License

MIT

---

*Created by Haley Bird · May 2026*
