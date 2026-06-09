# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Tests for core.verifier — chain integrity validation."""
import core.ledger as ledger_module
from core.certifier import generate_certificate
from core.verifier import verify_chain


def test_empty_ledger_is_valid():
    result = verify_chain()
    assert result["valid"] is True
    assert result["count"] == 0


def test_single_cert_is_valid():
    cert = generate_certificate(content="first", author="haley", model="gpt-4")
    ledger_module.append_certificate(cert)
    result = verify_chain()
    assert result["valid"] is True
    assert result["count"] == 1


def test_chained_certs_are_valid():
    c1 = generate_certificate(content="a", author="h", model="m")
    ledger_module.append_certificate(c1)
    c2 = generate_certificate(
        content="b", author="h", model="m", prev_hash=c1["content_hash"]
    )
    ledger_module.append_certificate(c2)
    result = verify_chain()
    assert result["valid"] is True
    assert result["count"] == 2


def test_broken_chain_detected():
    c1 = generate_certificate(content="a", author="h", model="m")
    ledger_module.append_certificate(c1)
    c2 = generate_certificate(
        content="b", author="h", model="m", prev_hash="sha256:WRONG"
    )
    ledger_module.append_certificate(c2)
    result = verify_chain()
    assert result["valid"] is False
    assert result["broken_at"] == c2["id"]
