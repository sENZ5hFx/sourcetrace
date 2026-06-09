# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Tests for core.certifier — CLP certificate generation."""

from core.certifier import generate_certificate, hash_content


def test_hash_content_is_deterministic():
    h1 = hash_content("hello world")
    h2 = hash_content("hello world")
    assert h1 == h2
    assert h1.startswith("sha256:")


def test_hash_content_is_unique():
    assert hash_content("a") != hash_content("b")


def test_generate_certificate_structure():
    cert = generate_certificate(
        content="test content",
        author="test_author",
        model="gpt-4",
    )
    assert cert["id"].startswith("clp-")
    assert cert["author"] == "test_author"
    assert cert["model"] == "gpt-4"
    assert cert["prev_hash"] == "GENESIS"
    assert cert["content_hash"].startswith("sha256:")
    assert isinstance(cert["metadata"], dict)


def test_generate_certificate_with_prev_hash():
    prev = "sha256:abc123"
    cert = generate_certificate(
        content="chained content",
        author="haley",
        model="claude",
        prev_hash=prev,
    )
    assert cert["prev_hash"] == prev


def test_generate_certificate_is_deterministic_by_content():
    c1 = generate_certificate(content="x", author="a", model="m")
    c2 = generate_certificate(content="x", author="a", model="m")
    # IDs are hash-derived from body — same body within same second = same id
    # (timestamps differ by microseconds in practice; test the structure)
    assert c1["content_hash"] == c2["content_hash"]


def test_generate_certificate_with_metadata():
    meta = {"source": "web", "confidence": 0.99}
    cert = generate_certificate(
        content="meta test", author="haley", model="gpt-4", metadata=meta
    )
    assert cert["metadata"] == meta


def test_cert_id_is_12_hex_chars():
    cert = generate_certificate(content="id test", author="h", model="m")
    # clp- prefix + 12 hex chars
    assert len(cert["id"]) == 16
    assert all(c in "0123456789abcdef" for c in cert["id"][4:])
