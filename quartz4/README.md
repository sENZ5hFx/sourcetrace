# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1

# Quartz 4 — Living System Architecture v2.0

> *From perfect instrument to living intelligence.*

This is the backend AI core for the Quartz 4 Web Garden — a full-stack AI organism
that bridges real-world data, persistent memory, and symbiotic conversation.

## Architecture

```
Frontend Cockpit (React/Svelte)
        │
        │  WebSocket + REST
        ▼
Backend AI Core (FastAPI)
  ├── Collector    — live multi-source data ingestion
  ├── Crucible     — LLM semantic analysis + ML forecasting
  ├── Sentinel     — proactive alert + hypothesis engine
  ├── Oracle       — natural language memory query
  └── Memory       — cryptographic integrity layer
        │
        ▼
Persistent Memory Layer
  ├── Vector DB    — Pinecone (concept embeddings + gravity)
  └── Graph DB     — Neo4j (relationships + temporal evolution)
```

## Quick Start

```bash
cd quartz4
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Environment Variables

```env
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_ENV=us-east1-gcp
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=...
ARXIV_MAX_RESULTS=50
ALPHA_VANTAGE_API_KEY=...
NEWS_API_KEY=...
```

## Module Reference

| Module | Role | Status |
|---|---|---|
| `collector.py` | Live data ingestion | ✅ Scaffolded |
| `crucible.py` | AI analysis engine | ✅ Scaffolded |
| `labyrinth.py` | Persistent memory | ✅ Scaffolded |
| `sentinel.py` | Alert + hypothesis | ✅ Scaffolded |
| `oracle.py` | NL query interface | ✅ Scaffolded |
| `memory.py` | Integrity layer | ✅ Scaffolded |
| `main.py` | FastAPI entrypoint | ✅ Scaffolded |
