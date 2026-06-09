# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Tests for quartz4/labyrinth.py"""

import pytest
from labyrinth import Labyrinth
from collector import ConceptEvent


@pytest.mark.anyio
async def test_connect_and_close_without_cloud():
    """Connect/close cycle works with no env vars set (in-memory fallback)."""
    lab = Labyrinth()
    await lab.connect()
    await lab.close()


@pytest.mark.anyio
async def test_ingest_stores_event(labyrinth):
    event = ConceptEvent(
        id="test-001",
        source="test",
        title="Quantum Entanglement Breakthrough",
        summary="Researchers demonstrate room-temperature entanglement.",
        url="https://arxiv.org/abs/test001",
    )
    await labyrinth.ingest(event)
    assert "test-001" in labyrinth._memory
    stored = labyrinth._memory["test-001"]
    assert stored["title"] == "Quantum Entanglement Breakthrough"
    assert stored["gravity"] == 0.0


@pytest.mark.anyio
async def test_store_concept_and_retrieve(labyrinth):
    embedding = [0.1] * 1536
    await labyrinth.store_concept(
        concept_id="c-abc",
        text="Neural scaling laws",
        embedding=embedding,
        gravity=2.5,
        source="manual",
    )
    assert "c-abc" in labyrinth._memory
    assert labyrinth._memory["c-abc"]["gravity"] == 2.5


@pytest.mark.anyio
async def test_top_concepts_sorted_by_gravity(labyrinth):
    for i, g in enumerate([1.0, 3.0, 2.0]):
        await labyrinth.store_concept(f"c-{i}", f"concept {i}", [0.0] * 1536, g)
    top = await labyrinth.top_concepts(limit=3)
    assert top[0]["gravity"] == 3.0
    assert top[1]["gravity"] == 2.0


@pytest.mark.anyio
async def test_search_fallback_returns_recent(labyrinth):
    for i in range(5):
        await labyrinth.store_concept(f"s-{i}", f"text {i}", [float(i)] * 1536, float(i))
    results = await labyrinth.search(query_embedding=[0.0] * 1536, top_k=3)
    assert len(results) == 3


@pytest.mark.anyio
async def test_snapshot_hash_is_deterministic(labyrinth):
    await labyrinth.store_concept("h-1", "hello", [0.0] * 1536, 1.0)
    h1 = await labyrinth.snapshot_hash()
    h2 = await labyrinth.snapshot_hash()
    assert h1 == h2
    assert len(h1) == 64  # SHA-256 hex digest


@pytest.mark.anyio
async def test_snapshot_hash_changes_on_new_concept(labyrinth):
    await labyrinth.store_concept("h-1", "hello", [0.0] * 1536, 1.0)
    h1 = await labyrinth.snapshot_hash()
    await labyrinth.store_concept("h-2", "world", [0.0] * 1536, 2.0)
    h2 = await labyrinth.snapshot_hash()
    assert h1 != h2


@pytest.mark.anyio
async def test_get_concept_history_empty(labyrinth):
    history = await labyrinth.get_concept_history("nonexistent")
    assert history == []


@pytest.mark.anyio
async def test_get_concept_history_populated(labyrinth):
    await labyrinth.store_concept("h-x", "concept x", [0.0] * 1536, 1.5)
    history = await labyrinth.get_concept_history("h-x")
    assert len(history) == 1
    assert history[0]["gravity"] == 1.5
