# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Module 3 + 8: The Crucible & Sentinel AI Engine.

Analytical core using LLMs for deep semantic understanding
and ML models for:
  - Conceptual Gravity (vector proximity + network centrality)
  - Structural Imperative (graph-based foundational importance)
  - Predictive Forecasting (time-series trajectory analysis)
"""

import hashlib
import logging
import os

logger = logging.getLogger(__name__)


class Crucible:
    """LLM-powered analytical engine."""

    def __init__(self, labyrinth):
        self.labyrinth = labyrinth
        self._client: object | None = None
        self._model = os.getenv("OPENAI_MODEL", "gpt-4o")

    def _get_client(self):
        """Lazy-init OpenAI client."""
        if self._client is None:
            try:
                from openai import AsyncOpenAI

                self._client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except ImportError:
                logger.warning("openai not installed — running in stub mode")
        return self._client

    async def process(self, text: str, source: str = "manual") -> str:
        """Process raw text: embed, analyse gravity, store.

        Returns concept_id.
        """
        concept_id = hashlib.sha256(text.encode()).hexdigest()[:16]
        embedding = await self._embed(text)
        gravity_score = self._conceptual_gravity(embedding)
        await self.labyrinth.store_concept(
            concept_id=concept_id,
            text=text,
            embedding=embedding,
            gravity=gravity_score,
            source=source,
        )
        return concept_id

    async def analyse(self, question: str, context: list[dict]) -> str:
        """Deep semantic analysis of a question given context chunks."""
        client = self._get_client()
        if client is None:
            return f"[Stub] Analysis of: {question[:80]}..."

        context_text = "\n\n".join(
            f"[{c.get('source', '?')}] {c.get('title', '')}: {c.get('summary', '')}"
            for c in context[:10]
        )
        messages = [
            {
                "role": "system",
                "content": (
                    "You are the Crucible — the analytical core of the Quartz 4 Living System. "
                    "You perform deep semantic analysis, identify conceptual gravity, "
                    "structural imperatives, and predictive trajectories across knowledge domains. "
                    "Be precise, incisive, and reveal non-obvious connections."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context_text}\n\nAnalyse: {question}",
            },
        ]
        response = await client.chat.completions.create(
            model=self._model,
            messages=messages,
            max_tokens=1500,
            temperature=0.3,
        )
        return response.choices[0].message.content

    async def forecast(self, concept_id: str) -> dict:
        """Predict future trajectory of a concept based on historical momentum."""
        history = await self.labyrinth.get_concept_history(concept_id)
        if not history:
            return {"concept_id": concept_id, "trajectory": "insufficient_data"}
        # Time-series stub — replace with actual ML model (e.g. Prophet, ARIMA)
        velocities = [h.get("gravity", 0) for h in history]
        trend = (
            "rising"
            if len(velocities) > 1 and velocities[-1] > velocities[0]
            else "stable"
        )
        return {
            "concept_id": concept_id,
            "trajectory": trend,
            "data_points": len(velocities),
            "latest_gravity": velocities[-1] if velocities else 0,
        }

    async def _embed(self, text: str) -> list[float]:
        """Generate embedding vector for a text."""
        client = self._get_client()
        if client is None:
            # Deterministic stub embedding (1536-dim)
            import hashlib

            seed = int(hashlib.md5(text.encode()).hexdigest(), 16)
            import random

            rng = random.Random(seed)
            return [rng.gauss(0, 1) for _ in range(1536)]
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=text[:8000],
        )
        return response.data[0].embedding

    def _conceptual_gravity(self, embedding: list[float]) -> float:
        """Compute conceptual gravity score from embedding magnitude.

        Full implementation: vector proximity to existing concepts
        + network centrality in the graph DB. Stub: L2 norm proxy.
        """
        import math

        magnitude = math.sqrt(sum(x**2 for x in embedding[:128]))
        return round(magnitude / 10.0, 4)
