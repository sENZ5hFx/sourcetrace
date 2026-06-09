# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Integration tests for quartz4/main.py FastAPI endpoints."""

import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(scope="module")
def client():
    from main import app  # noqa: PLC0415
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "alive"
    assert data["version"] == "2.1.0"


def test_concepts_empty(client):
    r = client.get("/concepts")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_ingest_success(client):
    r = client.post("/ingest", json={"concept": "Machine learning model compression", "source": "test"})
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ingested"
    assert "concept_id" in data


def test_ingest_missing_concept_422(client):
    r = client.post("/ingest", json={"source": "test"})
    assert r.status_code == 422


def test_query_success(client):
    r = client.post("/query", json={"q": "What is machine learning?"})
    assert r.status_code == 200
    assert "answer" in r.json()


def test_query_missing_q_422(client):
    r = client.post("/query", json={})
    assert r.status_code == 422


def test_alerts_initially_empty(client):
    r = client.get("/alerts")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_all_alerts_endpoint(client):
    r = client.get("/alerts/all")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_authorize_missing_alert_404(client):
    r = client.post("/alerts/doesnotexist/authorize")
    assert r.status_code == 404


def test_memory_snapshot(client):
    r = client.get("/memory/snapshot")
    assert r.status_code == 200
    data = r.json()
    assert "hash" in data
    assert len(data["hash"]) == 64


def test_memory_audit_trail(client):
    r = client.get("/memory/audit-trail")
    assert r.status_code == 200
    assert "trail" in r.json()


def test_forecast_unknown_concept_404(client):
    r = client.get("/forecast/concept-does-not-exist")
    assert r.status_code == 404


def test_forecast_after_ingest(client):
    """Ingest a concept then forecast it — should return trajectory data."""
    ingest_r = client.post("/ingest", json={"concept": "Topological quantum computing", "source": "test"})
    concept_id = ingest_r.json()["concept_id"]
    r = client.get(f"/forecast/{concept_id}")
    # Concept exists but has only 1 gravity point, so trajectory = stable or rising
    assert r.status_code == 200
    assert "trajectory" in r.json()
