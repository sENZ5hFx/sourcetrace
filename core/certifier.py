# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
# sourcetrace — Certified Ledger Protocol (CLP) Core Engine
# Invention: Hash-chained AI content provenance certificate generation
# Inventor: Haley Ann Bird | First committed: 2024 | Priority date: 2024-01-01
import hashlib
import json
from datetime import UTC, datetime


def hash_content(content: str) -> str:
    return "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()


def generate_certificate(
    content: str,
    author: str,
    model: str,
    prev_hash: str | None = None,
    metadata: dict | None = None,
) -> dict:
    timestamp = datetime.now(UTC).isoformat()
    content_hash = hash_content(content)
    cert_body = {
        "author": author,
        "model": model,
        "content_hash": content_hash,
        "timestamp": timestamp,
        "prev_hash": prev_hash or "GENESIS",
        "metadata": metadata or {},
    }
    cert_id = (
        "clp-"
        + hashlib.sha256(json.dumps(cert_body, sort_keys=True).encode()).hexdigest()[
            :12
        ]
    )
    return {"id": cert_id, **cert_body}
