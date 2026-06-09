# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Quartz 4 v2.0 — Living System Backend AI Core.

FastAPI entrypoint wiring all modules: Collector, Crucible,
Labyrinth, Sentinel, Oracle, and the cryptographic Memory layer.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from collector import Collector
from crucible import Crucible
from labyrinth import Labyrinth
from sentinel import Sentinel
from oracle import Oracle
from memory import MemoryIntegrity


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: initialise all modules. Shutdown: flush and close."""
    app.state.labyrinth = Labyrinth()
    await app.state.labyrinth.connect()

    app.state.collector = Collector(labyrinth=app.state.labyrinth)
    app.state.crucible = Crucible(labyrinth=app.state.labyrinth)
    app.state.sentinel = Sentinel(crucible=app.state.crucible)
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


# ── REST Endpoints ────────────────────────────────────────────────

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


@app.post("/ingest")
async def manual_ingest(body: dict):
    """Manually push a concept or document into the Labyrinth."""
    concept = body.get("concept", "")
    source = body.get("source", "manual")
    result = await app.state.crucible.process(concept, source=source)
    return {"status": "ingested", "concept_id": result}


# ── WebSocket — Symbiotic Dialogue ───────────────────────────────

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

    except WebSocketDisconnect:
        pass
