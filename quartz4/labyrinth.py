# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Module 4: The Labyrinth — Persistent Dual-Database Memory Layer.

Dual-database architecture:
  Vector DB (Pinecone): concept embeddings, gravity calculations,
                        lightning-fast similarity search.
  Graph DB (Neo4j):     relationships, temporal evolution,
                        structural connections — permanent knowledge graph.

Memory Integrity: cryptographic hashing of snapshots.
"""
import hashlib
import json
import logging
import os
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)


class Labyrinth:
    """Persistent dual-database memory layer."""

    def __init__(self):
        self._pinecone = None
        self._neo4j = None
        self._index_name = os.getenv("PINECONE_INDEX", "quartz4-concepts")
        # In-memory fallback for development without cloud DBs
        self._memory: dict[str, dict] = {}
        self._graph: dict[str, list] = {}

    async def connect(self):
        """Establish connections to Vector and Graph databases."""
        await self._connect_pinecone()
        await self._connect_neo4j()
        logger.info("Labyrinth connected")

    async def close(self):
        if self._neo4j:
            await self._neo4j.close()
        logger.info("Labyrinth closed")

    async def _connect_pinecone(self):
        api_key = os.getenv("PINECONE_API_KEY", "")
        if not api_key:
            logger.info("Pinecone: no API key — using in-memory fallback")
            return
        try:
            from pinecone import Pinecone
            pc = Pinecone(api_key=api_key)
            self._pinecone = pc.Index(self._index_name)
            logger.info("Pinecone: connected to index '%s'", self._index_name)
        except Exception as exc:
            logger.warning("Pinecone connection failed: %s", exc)

    async def _connect_neo4j(self):
        uri = os.getenv("NEO4J_URI", "")
        if not uri:
            logger.info("Neo4j: no URI — using in-memory graph fallback")
            return
        try:
            from neo4j import AsyncGraphDatabase
            self._neo4j = AsyncGraphDatabase.driver(
                uri,
                auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "")),
            )
            logger.info("Neo4j: connected at %s", uri)
        except Exception as exc:
            logger.warning("Neo4j connection failed: %s", exc)

    # ── Core Memory Operations ────────────────────────────────────

    async def ingest(self, event) -> None:
        """Ingest a ConceptEvent from the Collector."""
        self._memory[event.id] = {
            "id": event.id,
            "source": event.source,
            "title": event.title,
            "summary": event.summary,
            "url": event.url,
            "timestamp": event.timestamp.isoformat(),
            "gravity": 0.0,
        }

    async def store_concept(
        self,
        concept_id: str,
        text: str,
        embedding: list[float],
        gravity: float,
        source: str = "manual",
    ) -> None:
        """Store a processed concept with its embedding."""
        record = {
            "id": concept_id,
            "text": text[:500],
            "gravity": gravity,
            "source": source,
            "stored_at": datetime.utcnow().isoformat(),
            "history": [{"gravity": gravity, "ts": datetime.utcnow().isoformat()}],
        }
        self._memory[concept_id] = record

        if self._pinecone:
            try:
                self._pinecone.upsert(vectors=[{"id": concept_id, "values": embedding, "metadata": {"source": source}}])
            except Exception as exc:
                logger.warning("Pinecone upsert failed: %s", exc)

        if self._neo4j:
            try:
                async with self._neo4j.session() as session:
                    await session.run(
                        "MERGE (c:Concept {id: $id}) SET c.gravity = $gravity, c.source = $source",
                        id=concept_id, gravity=gravity, source=source,
                    )
            except Exception as exc:
                logger.warning("Neo4j write failed: %s", exc)

    async def top_concepts(self, limit: int = 50) -> list[dict]:
        """Return top concepts by gravity score."""
        concepts = sorted(self._memory.values(), key=lambda c: c.get("gravity", 0), reverse=True)
        return concepts[:limit]

    async def search(self, query_embedding: list[float], top_k: int = 10) -> list[dict]:
        """Similarity search over stored concepts."""
        if self._pinecone:
            try:
                result = self._pinecone.query(vector=query_embedding, top_k=top_k, include_metadata=True)
                ids = [m["id"] for m in result.get("matches", [])]
                return [self._memory[i] for i in ids if i in self._memory]
            except Exception as exc:
                logger.warning("Pinecone query failed: %s", exc)
        # Fallback: return most recent
        return list(self._memory.values())[:top_k]

    async def get_concept_history(self, concept_id: str) -> list[dict]:
        """Return temporal evolution of a concept's gravity."""
        concept = self._memory.get(concept_id, {})
        return concept.get("history", [])

    async def snapshot_hash(self) -> str:
        """Compute cryptographic hash of current memory state."""
        state = json.dumps(
            {k: v.get("gravity") for k, v in sorted(self._memory.items())},
            sort_keys=True,
        )
        return hashlib.sha256(state.encode()).hexdigest()
