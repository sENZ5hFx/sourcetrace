# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Quartz 4 v2.1 — Living System Backend AI Core.

FastAPI entrypoint wiring all modules: Collector, Crucible,
Labyrinth, Sentinel, Oracle, and the cryptographic Memory layer.

New in v2.1:
  - Sentinel receives Labyrinth reference + starts background scan loop
  - Collector receives Sentinel reference for post-ingest scanning
  - /forecast/{concept_id} endpoint
  - /memory/audit-trail endpoint
  - /alerts/all endpoint (includes authorized alerts)
"""

from contextlib import asynccontextmanager

from collector import Collector
from crucible import Crucible
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from labyrinth import Labyrinth
from memory import MemoryIntegrity
from oracle import Oracle
from sentinel import Sentinel


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: initialise all modules. Shutdown: flush and close."""
    app.state.labyrinth = Labyrinth()
    await app.state.labyrinth.connect()

    app.state.crucible = Crucible(labyrinth=app.state.labyrinth)

    # Sentinel now receives Labyrinth for its background scan loop
    app.state.sentinel = Sentinel(
        crucible=app.state.crucible,
        labyrinth=app.state.labyrinth,
    )

    # Collector receives Sentinel so post-ingest scans fire automatically
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
    await app.state.sentinel.start_background_scan()

    yield

    await app.state.sentinel.stop_background_scan()
    await app.state.collector.stop()
    await app.state.labyrinth.close()


app = FastAPI(
    title="Quartz 4 — Living System",
    version="2.1.0",
    description="AI organism: real-world data → persistent memory → symbiotic conversation",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ────────────────────────────────────────────────


@app.get("/health")
async def health():
    return {"status": "alive", "version": "2.1.0", "system": "Quartz 4 Living System"}


# ── Labyrinth ────────────────────────────────────────────


@app.get("/concepts")
async def list_concepts(limit: int = 50):
    """Return top concepts by conceptual gravity from the Labyrinth."""
    return await app.state.labyrinth.top_concepts(limit=limit)


@app.post("/ingest")
async def manual_ingest(body: dict):
    """Manually push a concept or document into the Labyrinth."""
    concept = body.get("concept", "")
    source = body.get("source", "manual")
    if not concept:
        raise HTTPException(status_code=422, detail="'concept' field required")
    result = await app.state.crucible.process(concept, source=source)
    return {"status": "ingested", "concept_id": result}


# ── Oracle ───────────────────────────────────────────────


@app.post("/query")
async def oracle_query(body: dict):
    """Natural language query over entire historical memory.

    Example: {"q": "Trace the decline of Proof-of-Work since 2023"}
    """
    question = body.get("q", "")
    if not question.strip():
        raise HTTPException(status_code=422, detail="'q' field required")
    result = await app.state.oracle.answer(question)
    return {"answer": result}


# ── Crucible ────────────────────────────────────────────


@app.get("/forecast/{concept_id}")
async def forecast_concept(concept_id: str):
    """Predict the future trajectory of a concept by its ID."""
    result = await app.state.crucible.forecast(concept_id)
    if result.get("trajectory") == "insufficient_data":
        raise HTTPException(
            status_code=404,
            detail=f"Concept '{concept_id}' not found or has no history.",
        )
    return result


# ── Sentinel ────────────────────────────────────────────


@app.get("/alerts")
async def get_alerts():
    """Fetch current pending (unauthorized) Sentinel hypotheses."""
    return await app.state.sentinel.pending_alerts()


@app.get("/alerts/all")
async def get_all_alerts():
    """Fetch all Sentinel alerts, including authorized ones."""
    return await app.state.sentinel.all_alerts()


@app.post("/alerts/{alert_id}/authorize")
async def authorize_alert(alert_id: str):
    """Authorize Sentinel to run a deep analysis cycle on a hypothesis."""
    result = await app.state.sentinel.authorize(alert_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return {"status": "authorized", "result": result}


# ── Memory ───────────────────────────────────────────────


@app.get("/memory/snapshot")
async def memory_snapshot():
    """Return a cryptographic hash snapshot of current memory state."""
    return await app.state.memory.snapshot()


@app.get("/memory/audit-trail")
async def memory_audit_trail():
    """Return the full tamper-evident memory audit trail."""
    return {"trail": app.state.memory.audit_trail()}


# ── WebSocket ───────────────────────────────────────────


@app.websocket("/ws/dialogue")
async def dialogue_socket(websocket: WebSocket):
    """Real-time symbiotic conversation channel.

    The Oracle and Sentinel both push to this channel.
    Client sends natural language; receives analysis + hypotheses.
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
                await websocket.send_json({"type": "alerts", "payload": alerts})

            elif msg_type == "forecast":
                result = await app.state.crucible.forecast(data.get("concept_id", ""))
                await websocket.send_json({"type": "forecast", "payload": result})

    except WebSocketDisconnect:
        pass
