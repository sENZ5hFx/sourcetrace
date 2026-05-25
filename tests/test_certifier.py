import pytest
from core.certifier import generate_certificate, hash_content


def test_hash_is_deterministic():
    h1 = hash_content("hello world")
    h2 = hash_content("hello world")
    assert h1 == h2
    assert h1.startswith("sha256:")


def test_certificate_structure():
    cert = generate_certificate(
        content="Test output",
        author="Haley Bird",
        model="gpt-4o"
    )
    assert "id" in cert
    assert cert["id"].startswith("clp-")
    assert cert["prev_hash"] == "GENESIS"
    assert cert["author"] == "Haley Bird"


def test_certificate_chain_links():
    cert1 = generate_certificate("First", "Haley Bird", "gpt-4o")
    cert2 = generate_certificate("Second", "Haley Bird", "gpt-4o", prev_hash=cert1["content_hash"])
    assert cert2["prev_hash"] == cert1["content_hash"]
