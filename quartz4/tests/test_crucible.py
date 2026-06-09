# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Tests for quartz4/crucible.py"""

import math
import pytest
from crucible import Crucible
from labyrinth import Labyrinth


@pytest.mark.anyio
async def test_embed_stub_returns_1536_floats(crucible):
    """With no OPENAI_API_KEY, _embed returns deterministic 1536-dim stub."""
    vec = await crucible._embed("hello world")
    assert len(vec) == 1536
    assert all(isinstance(v, float) for v in vec)


@pytest.mark.anyio
async def test_embed_stub_is_deterministic(crucible):
    v1 = await crucible._embed("test input")
    v2 = await crucible._embed("test input")
    assert v1 == v2


@pytest.mark.anyio
async def test_embed_stub_differs_for_different_inputs(crucible):
    v1 = await crucible._embed("alpha")
    v2 = await crucible._embed("beta")
    assert v1 != v2


@pytest.mark.anyio
async def test_conceptual_gravity_is_positive(crucible):
    vec = await crucible._embed("test")
    gravity = crucible._conceptual_gravity(vec)
    assert gravity > 0
    assert isinstance(gravity, float)


@pytest.mark.anyio
async def test_process_returns_concept_id_and_stores(crucible, labyrinth):
    concept_id = await crucible.process("Large language models are transforming AI", source="test")
    assert isinstance(concept_id, str)
    assert len(concept_id) == 16
    assert concept_id in labyrinth._memory


@pytest.mark.anyio
async def test_process_idempotent_same_text(crucible):
    """Same text always produces the same concept_id (hash-based)."""
    id1 = await crucible.process("deterministic text")
    id2 = await crucible.process("deterministic text")
    assert id1 == id2


@pytest.mark.anyio
async def test_analyse_stub_mode_returns_string(crucible):
    """With no OpenAI key, analyse() returns a stub string."""
    result = await crucible.analyse("What is the future of AI?", context=[])
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.anyio
async def test_forecast_insufficient_data(crucible):
    result = await crucible.forecast("nonexistent-concept")
    assert result["trajectory"] == "insufficient_data"


@pytest.mark.anyio
async def test_forecast_stable_single_datapoint(crucible, labyrinth):
    await labyrinth.store_concept("fc-1", "quantum", [0.0] * 1536, 1.5)
    result = await crucible.forecast("fc-1")
    assert "trajectory" in result
    assert result["data_points"] == 1
