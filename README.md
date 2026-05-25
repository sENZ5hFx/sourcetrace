# sourcetrace™
**Certified Ledger Protocol — AI Content Provenance Engine**

> *Every output has an origin. sourcetrace makes it verifiable.*

`sourcetrace` is a lightweight provenance certification engine that appends tamper-evident, timestamped records to AI-generated content outputs. It implements the **Certified Ledger Protocol (CLP)** — an append-only chain of content certificates anchored to author identity, model signature, and creation timestamp.

---

## What It Does

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
