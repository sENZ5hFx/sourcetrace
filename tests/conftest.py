# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Shared pytest fixtures for sourcetrace test suite."""
import pytest

import core.ledger as ledger_module


@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    """Redirect DB_PATH to a per-test temp file via monkeypatch.
    
    Using monkeypatch ensures teardown is guaranteed even on test failure,
    eliminating the DB_PATH race condition where module-level imports
    could resolve the real path before fixture setup completes.
    """
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(ledger_module, "DB_PATH", db_path)
    ledger_module.init_ledger(db_path)
    yield db_path
