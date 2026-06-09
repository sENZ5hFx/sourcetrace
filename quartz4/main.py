# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Quartz 4 v2.0 — Living System Backend AI Core.

FastAPI entrypoint wiring all modules: Collector, Crucible,
Labyrinth, Sentinel, Oracle, and the cryptographic Memory layer.

Sentinel is injected into Collector so that proactive alerts are
automatically generated after every ingestion cycle.
"""

from contextlib import asynccontextmanager

from collector import Collector
from crucible import Crucible
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from labyrinth import Labyrinth
from memory import MemoryIntegrity
from oracle import Oracle
from sentinel import Sentinel


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: initialise all modules. Shutdown: flush and close.

    Initialisation order matters:
      1. Labyrinth (DB connections) must come first.
      2. Crucible depends on Labyrinth.
      3. Sentinel depends on Crucible.
      4. Collector depends on Labyrinth AND Sentinel (for post-ingest scans).
      5. Oracle depends on Labyrinth and Crucible.
      6. MemoryIntegrity depends on Labyrinth.
    """
    app.state.labyrinth = Labyrinth()
    await app.state.labyrinth.connect()

    app.state.crucible = Crucible(labyrinth=app.state.labyrinth)
    app.state.sentinel = Sentinel(crucible=app.state.crucible)

    # Collector receives sentinel so alerts fire after every ingestion cycle
    app.state.collector = Collector(
        labyrinth=app.state.labyrinth,
        sentinel=app.state.sentinel,
    )

    app.state.oracle = Oracle(
        labyrinth=app.state.labyrinth,
        crucible=app.state.crucible,
    )
    app.state.memory = MemoryIntegrity(labyrinth=app.state.labyrinth)

    await app.state.collector.start()
    yield
    await app.state.collector.stop()
    await app.state.labyrinth.close()


app = FastAPI(
    title="Quartz 4 — Living System",
    version="2.0.0",
    description="AI organism: real-world data → persistent memory → symbiotic conversation",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── REST Endpoints ─────────────────────────────────────────────────────────────


@app.get("/health")
async def health():
    return {"status": "alive", "version": "2.0.0", "system": "Quartz 4 Living System"}


@app.get("/concepts")
async def list_concepts(limit: int = 50):
    """Return top concepts by conceptual gravity from the Labyrinth."""
    return await app.state.labyrinth.top_concepts(limit=limit)


@app.post("/query")
async def oracle_query(body: dict):
    """Natural language query over entire historical memory.

    Example: {"q": "Trace the decline of Proof-of-Work since 2023"}
    """
    question = body.get("q", "")
    result = await app.state.oracle.answer(question)
    return {"answer": result}


@app.get("/alerts")
async def get_alerts():
    """Fetch current Sentinel hypotheses and proactive alerts."""
    return await app.state.sentinel.pending_alerts()


@app.post("/alerts/{alert_id}/authorize")
async def authorize_alert(alert_id: str):
    """Authorize Sentinel to run a deep analysis cycle on a hypothesis."""
    result = await app.state.sentinel.authorize(alert_id)
    return {"status": "authorized", "result": result}


@app.get("/memory/snapshot")
async def memory_snapshot():
    """Return cryptographic hash snapshot of current memory state."""
    return await app.state.memory.snapshot()


@app.get("/memory/audit")
async def memory_audit():
    """Return the full tamper-evident memory audit trail."""
    return app.state.memory.audit_trail()


@app.get("/memory/verify/{claimed_hash}")
async def memory_verify(claimed_hash: str):
    """Verify a claimed memory hash against the audit trail."""
    valid = app.state.memory.verify(claimed_hash)
    return {"claimed_hash": claimed_hash, "valid": valid}


@app.post("/ingest")
async def manual_ingest(body: dict):
    """Manually push a concept or document into the Labyrinth."""
    concept = body.get("concept", "")
    source = body.get("source", "manual")
    result = await app.state.crucible.process(concept, source=source)
    # Trigger Sentinel scan after manual ingest too
    concepts = await app.state.labyrinth.top_concepts(limit=25)
    await app.state.sentinel.scan(concepts)
    return {"status": "ingested", "concept_id": result}


@app.get("/forecast/{concept_id}")
async def forecast_concept(concept_id: str):
    """Return predictive trajectory for a stored concept."""
    return await app.state.crucible.forecast(concept_id)


# ── WebSocket — Symbiotic Dialogue ───────────────────────────────────────────


@app.websocket("/ws/dialogue")
async def dialogue_socket(websocket: WebSocket):
    """Real-time symbiotic conversation channel.

    The Oracle and Sentinel both push to this channel.
    Client sends natural language; receives analysis + hypotheses.

    Message types (client → server):
      {"type": "query", "q": "<question>"}  → Oracle answer
      {"type": "ping"}                      → Sentinel alerts snapshot
      {"type": "ingest", "concept": "..."}  → Manual ingest + scan
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type", "query")

            if msg_type == "query":
                answer = await app.state.oracle.answer(data.get("q", ""))
                await websocket.send_json({"type": "answer", "payload": answer})

            elif msg_type == "ping":
                alerts = await app.state.sentinel.pending_alerts()
                snapshot = await app.state.memory.snapshot()
                await websocket.send_json(
                    {"type": "state", "alerts": alerts, "memory": snapshot}
                )

            elif msg_type == "ingest":
                concept = data.get("concept", "")
                if concept:
                    cid = await app.state.crucible.process(concept, source="ws")
                    concepts = await app.state.labyrinth.top_concepts(limit=25)
                    new_alerts = await app.state.sentinel.scan(concepts)
                    await websocket.send_json(
                        {
                            "type": "ingested",
                            "concept_id": cid,
                            "new_alerts": len(new_alerts),
                        }
                    )

    except WebSocketDisconnect:
        pass
