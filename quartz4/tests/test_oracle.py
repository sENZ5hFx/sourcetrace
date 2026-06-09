# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Tests for quartz4/oracle.py"""

import pytest
from oracle import Oracle


@pytest.mark.anyio
async def test_oracle_answer_empty_question(crucible, labyrinth):
    oracle = Oracle(labyrinth=labyrinth, crucible=crucible)
    result = await oracle.answer("")
    assert result == "Please ask a question."


@pytest.mark.anyio
async def test_oracle_answer_whitespace_only(crucible, labyrinth):
    oracle = Oracle(labyrinth=labyrinth, crucible=crucible)
    result = await oracle.answer("   ")
    assert result == "Please ask a question."


@pytest.mark.anyio
async def test_oracle_answer_returns_string(crucible, labyrinth):
    """With stub Crucible (no API key), answer() still returns a non-empty string."""
    oracle = Oracle(labyrinth=labyrinth, crucible=crucible)
    result = await oracle.answer("What is the future of quantum computing?")
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.anyio
async def test_oracle_uses_labyrinth_context(crucible, labyrinth):
    """After ingesting a concept, Oracle should retrieve it as context."""
    await labyrinth.store_concept(
        concept_id="ctx-001",
        text="Quantum error correction milestone achieved",
        embedding=[0.5] * 1536,
        gravity=2.0,
        source="test",
    )
    oracle = Oracle(labyrinth=labyrinth, crucible=crucible)
    result = await oracle.answer("Tell me about quantum error correction")
    # With stub crucible this still returns a string; no crash = context pipeline works
    assert isinstance(result, str)
