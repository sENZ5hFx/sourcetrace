# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Module 8 (partial): The Sentinel — Proactive Alert & Hypothesis Engine.

Monitors the Labyrinth for emerging patterns and generates
conversational hypotheses:
  'Hypothesis: A breakthrough in [domain] is imminent based on
   converging patent and pre-print data. Authorize deep analysis?'
"""

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

    GRAVITY_THRESHOLD = 1.5  # Trigger alert when concept gravity exceeds this

    def __init__(self, crucible):
        self.crucible = crucible
        self._alerts: dict[str, Alert] = {}

    async def scan(self, concepts: list[dict]) -> list[Alert]:
        """Scan concept list for emerging high-gravity signals."""
        new_alerts = []
        rising = [c for c in concepts if c.get("gravity", 0) >= self.GRAVITY_THRESHOLD]
        if rising:
            top = rising[0]
            hypothesis = (
                f"Hypothesis: A significant development in '{top.get('title', top.get('id', '?'))}' "
                f"is emerging (gravity={top.get('gravity', 0):.3f}) based on converging data. "
                f"Authorize a deep analysis cycle?"
            )
            alert = Alert(
                hypothesis=hypothesis,
                concepts=[c.get("id", "") for c in rising[:5]],
                confidence=min(top.get("gravity", 0) / 3.0, 1.0),
            )
            self._alerts[alert.id] = alert
            new_alerts.append(alert)
            logger.info("Sentinel: new alert %s", alert.id)
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

    async def authorize(self, alert_id: str) -> dict:
        """Authorize a Sentinel alert to run deep analysis."""
        alert = self._alerts.get(alert_id)
        if not alert:
            return {"error": f"Alert {alert_id} not found"}
        alert.authorized = True
        # Trigger deep analysis via Crucible
        result = await self.crucible.analyse(
            question=alert.hypothesis,
            context=[
                {"source": cid, "title": cid, "summary": ""} for cid in alert.concepts
            ],
        )
        alert.result = {"analysis": result}
        return alert.result
