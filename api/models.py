# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
# sourcetrace — API request/response models
from pydantic import BaseModel


class CertifyRequest(BaseModel):
    content: str
    author: str
    model: str
    metadata: dict | None = None


class CertificateResponse(BaseModel):
    id: str
    author: str
    model: str
    content_hash: str
    timestamp: str
    prev_hash: str
    chain_valid: bool = True
