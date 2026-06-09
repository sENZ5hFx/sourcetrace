from pydantic import BaseModel
from typing import Optional


class CertifyRequest(BaseModel):
    content: str
    author: str
    model: str
    metadata: Optional[dict] = {}


class CertificateResponse(BaseModel):
    id: str
    author: str
    model: str
    content_hash: str
    timestamp: str
    prev_hash: str
    chain_valid: bool = True
