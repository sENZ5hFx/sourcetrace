# sourcetrace

**Automated truth-extraction for any codebase.**

sourcetrace reads your actual source code — tests, imports, routes, config — and produces a structured "source truth pack" that tells you what the system *really* guarantees, where the docs lie, and where the footguns hide.

---

## Philosophy

> Excellence isn't about fixing broken things. It's about owning and elevating the acceptable — turning hidden compromises into architectures of deliberate, resilient, and imaginative design.

Most documentation describes what someone *intended* to build. sourcetrace describes what *actually exists* — derived from code, not from memory or assumption.
# sourcetrace™
**Certified Ledger Protocol — AI Content Provenance Engine**

> *Every output has an origin. sourcetrace makes it verifiable.*

`sourcetrace` is a lightweight provenance certification engine that appends tamper-evident, timestamped records to AI-generated content outputs. It implements the **Certified Ledger Protocol (CLP)** — an append-only chain of content certificates anchored to author identity, model signature, and creation timestamp.

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
- **Certifies** AI-generated content with author + model + timestamp hash
- **Chains** certificates into an append-only ledger (tamper-evident)
- **Exports** provenance bundles as `.clp` files for storage or transmission
- **Verifies** any `.clp` bundle against its chain integrity
- **Integrates** with NeuroCatalyst, hazel, and external AI pipelines

---

## Architecture

```
sourcetrace/
├── core/
│   ├── certifier.py      # Generates content certificates
│   ├── ledger.py         # Append-only ledger chain
│   ├── verifier.py       # Chain integrity verification
│   └── bundle.py         # .clp export/import
├── api/
│   ├── main.py           # FastAPI surface
│   └── models.py         # Pydantic models
├── storage/
│   └── ledger.db         # SQLite ledger (gitignored)
├── tests/
│   └── test_certifier.py
├── main.py               # Entry point
├── requirements.txt
└── README.md
```

---

## Quick Start

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Certify Content
```bash
curl -X POST http://localhost:8000/certify \
  -H 'Content-Type: application/json' \
  -d '{"content": "Your AI output here", "author": "Haley Bird", "model": "gpt-4o"}'
```

### Verify a Bundle
```bash
curl http://localhost:8000/verify/{certificate_id}
```

### Export Ledger Bundle
```bash
curl http://localhost:8000/bundle/export
```

---

## Certificate Format

```json
{
  "id": "clp-abc123",
  "author": "Haley Bird",
  "model": "gpt-4o",
  "content_hash": "sha256:...",
  "timestamp": "2026-05-24T22:56:00Z",
  "prev_hash": "sha256:...",
  "chain_valid": true
}
```

---

*Part of the NeuroCatalyst™ ecosystem. Protected under Certified Ledger Protocol™ trademark (ITU filed May 2026).*
