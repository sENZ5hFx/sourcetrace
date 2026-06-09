# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Module 8: The Sentinel — Proactive Alert & Hypothesis Engine.

Monitors the Labyrinth for emerging patterns and generates
conversational hypotheses:
  'Hypothesis: A breakthrough in [domain] is imminent based on
   converging patent and pre-print data. Authorize deep analysis?'

Now includes a periodic background scan loop that wakes every
`scan_interval` seconds to re-evaluate the full concept landscape,
and a `_scan_lock` to prevent concurrent overlapping scans.
"""

import asyncio
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class Alert:
    def __init__(self, hypothesis: str, concepts: list[str], confidence: float):
        self.id = str(uuid.uuid4())[:8]
        self.hypothesis = hypothesis
        self.concepts = concepts
        self.confidence = confidence
        self.created_at = datetime.utcnow().isoformat()
        self.authorized = False
        self.result: dict | None = None


class Sentinel:
    """Proactive hypothesis generator and alert manager."""

    GRAVITY_THRESHOLD = 1.5

    def __init__(self, crucible, labyrinth=None, scan_interval: int = 600):
        self.crucible = crucible
        self.labyrinth = labyrinth  # optional; enables background loop
        self.scan_interval = scan_interval
        self._alerts: dict[str, Alert] = {}
        self._scan_lock = asyncio.Lock()
        self._bg_task: asyncio.Task | None = None

    # ── Lifecycle ─────────────────────────────────────────

    async def start_background_scan(self) -> None:
        """Launch the periodic background scan loop."""
        if self.labyrinth is None:
            logger.warning("Sentinel: no Labyrinth injected — background scan disabled")
            return
        self._bg_task = asyncio.create_task(self._background_loop())
        logger.info("Sentinel: background scan loop started (interval=%ds)", self.scan_interval)

    async def stop_background_scan(self) -> None:
        """Cancel the background scan loop."""
        if self._bg_task:
            self._bg_task.cancel()
            await asyncio.gather(self._bg_task, return_exceptions=True)
            logger.info("Sentinel: background scan loop stopped")

    async def _background_loop(self) -> None:
        while True:
            await asyncio.sleep(self.scan_interval)
            try:
                concepts = await self.labyrinth.top_concepts(limit=100)
                await self.scan(concepts)
            except Exception as exc:  # pragma: no cover
                logger.warning("Sentinel background scan error: %s", exc)

    # ── Core ───────────────────────────────────────────────

    async def scan(self, concepts: list[dict]) -> list[Alert]:
        """Scan concept list for emerging high-gravity signals.

        Thread-safe: uses _scan_lock to prevent overlapping scans.
        Only one unique hypothesis per rising concept is stored
        (idempotent by concept id).
        """
        async with self._scan_lock:
            new_alerts: list[Alert] = []
            rising = [
                c for c in concepts if c.get("gravity", 0) >= self.GRAVITY_THRESHOLD
            ]
            if not rising:
                return new_alerts

            # Deduplicate: one alert per top concept id
            existing_concept_ids = {
                cid for a in self._alerts.values() for cid in a.concepts
            }
            novel = [
                c for c in rising if c.get("id", "") not in existing_concept_ids
            ]
            if not novel:
                return new_alerts

            top = novel[0]
            hypothesis = (
                f"Hypothesis: A significant development in "
                f"'{top.get('title', top.get('id', '?'))}' "
                f"is emerging (gravity={top.get('gravity', 0):.3f}) based on "
                f"converging data. Authorize a deep analysis cycle?"
            )
            alert = Alert(
                hypothesis=hypothesis,
                concepts=[c.get("id", "") for c in novel[:5]],
                confidence=min(top.get("gravity", 0) / 3.0, 1.0),
            )
            self._alerts[alert.id] = alert
            new_alerts.append(alert)
            logger.info("Sentinel: new alert %s (confidence=%.2f)", alert.id, alert.confidence)
            return new_alerts

    async def pending_alerts(self) -> list[dict]:
        """Return all unresolved alerts."""
        return [
            {
                "id": a.id,
                "hypothesis": a.hypothesis,
                "confidence": a.confidence,
                "created_at": a.created_at,
                "authorized": a.authorized,
            }
            for a in self._alerts.values()
            if not a.authorized
        ]

    async def all_alerts(self) -> list[dict]:
        """Return all alerts including authorized ones (for audit)."""
        return [
            {
                "id": a.id,
                "hypothesis": a.hypothesis,
                "confidence": a.confidence,
                "created_at": a.created_at,
                "authorized": a.authorized,
                "result": a.result,
            }
            for a in self._alerts.values()
        ]

    async def authorize(self, alert_id: str) -> dict:
        """Authorize a Sentinel alert to run deep analysis."""
        alert = self._alerts.get(alert_id)
        if not alert:
            return {"error": f"Alert {alert_id} not found"}
        alert.authorized = True
        result = await self.crucible.analyse(
            question=alert.hypothesis,
            context=[
                {"source": cid, "title": cid, "summary": ""} for cid in alert.concepts
            ],
        )
        alert.result = {"analysis": result}
        return alert.result
