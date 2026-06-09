# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Shared fixtures for Quartz 4 test suite.

All external I/O (OpenAI, Pinecone, Neo4j, httpx) is stubbed out
so tests run fully offline with zero API keys required.
"""

import sys
import os
import pytest

# Ensure quartz4/ is importable when pytest is run from repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from labyrinth import Labyrinth
from crucible import Crucible
from sentinel import Sentinel
from memory import MemoryIntegrity


@pytest.fixture
def labyrinth():
    """Fresh in-memory Labyrinth (no cloud DBs)."""
    lab = Labyrinth()
    return lab


@pytest.fixture
def crucible(labyrinth):
    """Crucible with stubbed OpenAI client (no API key needed)."""
    return Crucible(labyrinth=labyrinth)


@pytest.fixture
def sentinel(crucible):
    """Sentinel with no background loop (labyrinth=None)."""
    return Sentinel(crucible=crucible)


@pytest.fixture
def memory(labyrinth):
    return MemoryIntegrity(labyrinth=labyrinth)


@pytest.fixture
async def connected_labyrinth():
    """Labyrinth that has gone through connect() lifecycle."""
    lab = Labyrinth()
    await lab.connect()
    yield lab
    await lab.close()
