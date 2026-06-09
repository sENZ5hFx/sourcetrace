# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Integration tests for sourcetrace FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

import core.ledger as ledger_module


@pytest.fixture(autouse=True)
def isolated_db(tmp_path):
    original = ledger_module.DB_PATH
    ledger_module.DB_PATH = tmp_path / "test_api.db"
    ledger_module.init_ledger()
    yield
    ledger_module.DB_PATH = original


@pytest.fixture
def client():
    from main import app

    with TestClient(app) as c:
        yield c


def test_health_returns_alive(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "alive"


def test_certify_creates_certificate(client):
    payload = {"content": "hello world", "author": "haley", "model": "gpt-4"}
    r = client.post("/certify", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "certificate" in data
    assert data["certificate"]["id"].startswith("clp-")
    assert data["chain_position"] == 1


def test_verify_existing_cert(client):
    payload = {"content": "verify me", "author": "haley", "model": "gpt-4"}
    cert_r = client.post("/certify", json=payload)
    cert_id = cert_r.json()["certificate"]["id"]
    r = client.get(f"/verify/{cert_id}")
    assert r.status_code == 200
    assert r.json()["certificate"]["id"] == cert_id


def test_verify_missing_cert_returns_404(client):
    r = client.get("/verify/clp-doesnotexist")
    assert r.status_code == 404


def test_chain_endpoint(client):
    r = client.get("/chain")
    assert r.status_code == 200
    assert "valid" in r.json()


def test_ledger_endpoint(client):
    client.post("/certify", json={"content": "a", "author": "h", "model": "m"})
    client.post("/certify", json={"content": "b", "author": "h", "model": "m"})
    r = client.get("/ledger")
    assert r.status_code == 200
    assert r.json()["count"] == 2


def test_bundle_export(client):
    client.post(
        "/certify", json={"content": "bundle test", "author": "h", "model": "m"}
    )
    r = client.get("/bundle/export")
    assert r.status_code == 200
    data = r.json()
    assert data["format"] == "clp-bundle-v1"
    assert data["record_count"] == 1
    assert "records" in data
