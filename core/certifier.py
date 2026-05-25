import hashlib
import json
from datetime import datetime, timezone
from typing import Optional


def hash_content(content: str) -> str:
    return "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()


def generate_certificate(
    content: str,
    author: str,
    model: str,
    prev_hash: Optional[str] = None,
    metadata: Optional[dict] = None
) -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()
    content_hash = hash_content(content)
    cert_body = {
        "author": author,
        "model": model,
        "content_hash": content_hash,
        "timestamp": timestamp,
        "prev_hash": prev_hash or "GENESIS",
        "metadata": metadata or {}
    }
    cert_id = "clp-" + hashlib.sha256(
        json.dumps(cert_body, sort_keys=True).encode()
    ).hexdigest()[:12]
    return {"id": cert_id, **cert_body}
