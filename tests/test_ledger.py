# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Tests for core.ledger — append-only SQLite ledger."""
import core.ledger as ledger_module
from core.certifier import generate_certificate


def test_init_creates_db(isolated_db):
    assert isolated_db.exists()


def test_append_and_retrieve():
    cert = generate_certificate(content="hello", author="haley", model="gpt-4")
    result = ledger_module.append_certificate(cert)
    assert result is True
    retrieved = ledger_module.get_certificate(cert["id"])
    assert retrieved is not None
    assert retrieved["id"] == cert["id"]
    assert retrieved["author"] == "haley"


def test_get_certificate_missing_returns_none():
    result = ledger_module.get_certificate("clp-doesnotexist")
    assert result is None


def test_get_latest_hash_empty_returns_genesis():
    h = ledger_module.get_latest_hash()
    assert h == "GENESIS"


def test_get_latest_hash_after_append():
    cert = generate_certificate(content="test", author="h", model="m")
    ledger_module.append_certificate(cert)
    latest = ledger_module.get_latest_hash()
    assert latest == cert["content_hash"]


def test_get_full_ledger_ordered():
    for i in range(3):
        c = generate_certificate(content=f"entry {i}", author="h", model="m")
        ledger_module.append_certificate(c)
    records = ledger_module.get_full_ledger()
    assert len(records) == 3
    timestamps = [r["timestamp"] for r in records]
    assert timestamps == sorted(timestamps)


def test_duplicate_id_fails_gracefully():
    cert = generate_certificate(content="dup", author="h", model="m")
    r1 = ledger_module.append_certificate(cert)
    r2 = ledger_module.append_certificate(cert)
    assert r1 is True
    assert r2 is False
