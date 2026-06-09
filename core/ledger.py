# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
# sourcetrace — Certified Ledger Protocol (CLP) Append-Only SQLite Ledger
# Invention: Tamper-evident hash-chained ledger for AI content provenance
# Inventor: Haley Ann Bird | Priority date: 2024-01-01
import json
import sqlite3
from pathlib import Path

DB_PATH = Path("storage/ledger.db")


def init_ledger() -> None:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS certificates (
            id TEXT PRIMARY KEY,
            author TEXT NOT NULL,
            model TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            prev_hash TEXT NOT NULL,
            metadata TEXT DEFAULT '{}',
            chain_valid INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()


def append_certificate(cert: dict) -> bool:
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            """
            INSERT INTO certificates
            (id, author, model, content_hash, timestamp, prev_hash, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                cert["id"],
                cert["author"],
                cert["model"],
                cert["content_hash"],
                cert["timestamp"],
                cert["prev_hash"],
                json.dumps(cert.get("metadata", {})),
            ),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def get_certificate(cert_id: str) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT * FROM certificates WHERE id = ?", (cert_id,)).fetchone()
    conn.close()
    if not row:
        return None
    keys = [
        "id",
        "author",
        "model",
        "content_hash",
        "timestamp",
        "prev_hash",
        "metadata",
        "chain_valid",
    ]
    return dict(zip(keys, row))


def get_latest_hash() -> str:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT content_hash FROM certificates ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    conn.close()
    return row[0] if row else "GENESIS"


def get_full_ledger() -> list:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM certificates ORDER BY timestamp ASC").fetchall()
    conn.close()
    keys = [
        "id",
        "author",
        "model",
        "content_hash",
        "timestamp",
        "prev_hash",
        "metadata",
        "chain_valid",
    ]
    return [dict(zip(keys, r)) for r in rows]
