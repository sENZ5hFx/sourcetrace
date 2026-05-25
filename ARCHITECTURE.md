# sourcetrace — Architecture
**Certified Ledger Protocol (CLP) Engine**

```
┌─────────────────────────────────────────────┐
│                  FastAPI App                │
│  POST /certify   GET /verify/:id   /bundle  │
└──────────────┬──────────────────────────────┘
               │
       ┌───────▼────────┐
       │   core/         │
       │  certifier.py  │  — SHA-256 hash + chain-link
       │  ledger.py     │  — In-memory ledger store
       │  verifier.py   │  — Certificate lookup + validation
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │   api/          │
       │  models.py     │  — Pydantic request/response schemas
       └────────────────┘
```

## Data Flow
1. Client POSTs content → `certifier.py` hashes it → stores in `ledger.py` → returns certificate
2. Each certificate includes `previous_hash` → tamper-evident chain
3. GET `/verify/{id}` → `verifier.py` re-hashes content → compares to stored hash
4. GET `/bundle/export` → portable `.clp` JSON bundle of full ledger

## Certificate Schema
```json
{
  "certificate_id": "uuid4",
  "content_hash": "sha256hex",
  "previous_hash": "sha256hex | null",
  "certified_at": "ISO8601",
  "source": "string",
  "metadata": {}
}
```

## Production Path
- Swap in-memory ledger → PostgreSQL or SQLite
- Add API key auth middleware
- Add webhook on certification event
- Integrate with `cartograph` for graph-linked provenance

---
*NeuroCatalyst™ — Certified Ledger Protocol™*
