# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
"""Shared pytest fixtures for sourcetrace test suite."""
import pytest

import core.ledger as ledger_module


@pytest.fixture(autouse=True)
def isolated_db(tmp_path):
    """Redirect DB_PATH to a per-test temp file. Autouse = always isolated."""
    original = ledger_module.DB_PATH
    db_path = tmp_path / "test.db"
    ledger_module.DB_PATH = db_path
    ledger_module.init_ledger(db_path)
    yield db_path
    ledger_module.DB_PATH = original
