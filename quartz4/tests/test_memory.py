# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Tests for quartz4/memory.py"""

import pytest
from memory import MemoryIntegrity


@pytest.mark.anyio
async def test_snapshot_returns_hash_and_count(memory, labyrinth):
    snap = await memory.snapshot()
    assert "hash" in snap
    assert "concept_count" in snap
    assert snap["concept_count"] == 0
    assert len(snap["hash"]) == 64


@pytest.mark.anyio
async def test_snapshot_prev_hash_is_none_initially(memory):
    snap = await memory.snapshot()
    assert snap["prev_hash"] is None


@pytest.mark.anyio
async def test_snapshot_chaining(memory, labyrinth):
    s1 = await memory.snapshot()
    await labyrinth.store_concept("ch-1", "first", [0.0] * 1536, 1.0)
    s2 = await memory.snapshot()
    assert s2["prev_hash"] == s1["hash"]
    assert s2["hash"] != s1["hash"]


@pytest.mark.anyio
async def test_verify_known_hash(memory, labyrinth):
    snap = await memory.snapshot()
    assert memory.verify(snap["hash"]) is True


@pytest.mark.anyio
async def test_verify_unknown_hash(memory):
    assert memory.verify("deadbeef" * 8) is False


@pytest.mark.anyio
async def test_audit_trail_grows(memory, labyrinth):
    await memory.snapshot()
    await memory.snapshot()
    trail = memory.audit_trail()
    assert len(trail) == 2


@pytest.mark.anyio
async def test_audit_trail_is_tamper_evident(memory, labyrinth):
    """Each entry's prev_hash references the prior entry's hash."""
    await memory.snapshot()
    await labyrinth.store_concept("te-1", "tamper", [0.0] * 1536, 1.0)
    await memory.snapshot()
    trail = memory.audit_trail()
    assert trail[1]["prev_hash"] == trail[0]["hash"]
