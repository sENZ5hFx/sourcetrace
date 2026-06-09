# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Tests for quartz4/sentinel.py"""

import pytest
from sentinel import Sentinel, Alert


@pytest.mark.anyio
async def test_scan_below_threshold_no_alerts(sentinel):
    concepts = [{"id": "c1", "title": "test", "gravity": 0.5}]
    alerts = await sentinel.scan(concepts)
    assert alerts == []


@pytest.mark.anyio
async def test_scan_above_threshold_creates_alert(sentinel):
    concepts = [{"id": "c1", "title": "AI Breakthrough", "gravity": 2.0}]
    alerts = await sentinel.scan(concepts)
    assert len(alerts) == 1
    assert "AI Breakthrough" in alerts[0].hypothesis
    assert alerts[0].confidence == pytest.approx(2.0 / 3.0, rel=1e-3)


@pytest.mark.anyio
async def test_scan_deduplicates_same_concept(sentinel):
    concepts = [{"id": "c1", "title": "AI Breakthrough", "gravity": 2.0}]
    await sentinel.scan(concepts)
    alerts2 = await sentinel.scan(concepts)
    # Second scan on same concept id should produce no new alerts
    assert alerts2 == []


@pytest.mark.anyio
async def test_pending_alerts_excludes_authorized(sentinel):
    concepts = [{"id": "c2", "title": "Quantum", "gravity": 2.5}]
    alerts = await sentinel.scan(concepts)
    alert_id = alerts[0].id
    await sentinel.authorize(alert_id)
    pending = await sentinel.pending_alerts()
    assert all(a["id"] != alert_id for a in pending)


@pytest.mark.anyio
async def test_all_alerts_includes_authorized(sentinel):
    concepts = [{"id": "c3", "title": "Fusion", "gravity": 3.0}]
    alerts = await sentinel.scan(concepts)
    await sentinel.authorize(alerts[0].id)
    all_a = await sentinel.all_alerts()
    assert any(a["authorized"] for a in all_a)


@pytest.mark.anyio
async def test_authorize_missing_alert_returns_error(sentinel):
    result = await sentinel.authorize("doesnotexist")
    assert "error" in result


@pytest.mark.anyio
async def test_confidence_capped_at_1(sentinel):
    concepts = [{"id": "c4", "title": "Mega", "gravity": 100.0}]
    alerts = await sentinel.scan(concepts)
    assert alerts[0].confidence <= 1.0


@pytest.mark.anyio
async def test_scan_is_concurrent_safe(sentinel):
    """Two concurrent scans on different concepts both succeed."""
    import asyncio
    c1 = [{"id": "cc1", "title": "Alpha", "gravity": 2.0}]
    c2 = [{"id": "cc2", "title": "Beta", "gravity": 2.1}]
    results = await asyncio.gather(sentinel.scan(c1), sentinel.scan(c2))
    # Combined unique alerts should be 2
    total = sum(len(r) for r in results)
    assert total == 2
