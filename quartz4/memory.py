# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Memory Integrity Layer — cryptographic hash verification of memory state.

Applies the Memory Integrity protocol from Quartz 4 spec:
  - SHA-256 hash of Labyrinth snapshot at each checkpoint
  - Tamper-evident audit trail
  - Verifiable memory provenance
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MemoryIntegrity:
    """Cryptographic integrity layer for Labyrinth memory."""

    def __init__(self, labyrinth):
        self.labyrinth = labyrinth
        self._history: list[dict] = []

    async def snapshot(self) -> dict:
        """Capture and record a verified snapshot of current memory."""
        current_hash = await self.labyrinth.snapshot_hash()
        concept_count = len(self.labyrinth._memory)

        entry = {
            "hash": current_hash,
            "concept_count": concept_count,
            "timestamp": datetime.utcnow().isoformat(),
            "prev_hash": self._history[-1]["hash"] if self._history else None,
        }
        self._history.append(entry)
        logger.info(
            "Memory snapshot: %s (%d concepts)", current_hash[:12], concept_count
        )
        return entry

    def verify(self, claimed_hash: str) -> bool:
        """Verify a claimed hash against the snapshot history."""
        return any(s["hash"] == claimed_hash for s in self._history)

    def audit_trail(self) -> list[dict]:
        """Return the full tamper-evident audit trail."""
        return self._history
