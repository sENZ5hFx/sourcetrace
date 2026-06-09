# Copyright (c) 2024–2026 Haley Ann Bird. All Rights Reserved.
# SPDX-License-Identifier: BSL-1.1
# sourcetrace — Certified Ledger Protocol (CLP) API entrypoint
# Invention: AI content provenance engine with hash-chained ledger
# Inventor: Haley Ann Bird | heyhaleybird@gmail.com | Fishers, IN, USA
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from api.models import CertifyRequest
from core.certifier import generate_certificate
from core.ledger import (
    append_certificate,
    get_certificate,
    get_full_ledger,
    get_latest_hash,
    init_ledger,
)
from core.verifier import verify_chain


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_ledger()
    yield


app = FastAPI(
    title="sourcetrace",
    description="Certified Ledger Protocol — AI Content Provenance Engine",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    chain = verify_chain()
    return {"status": "alive", "chain": chain}


@app.post("/certify")
def certify(req: CertifyRequest):
    prev = get_latest_hash()
    cert = generate_certificate(
        content=req.content,
        author=req.author,
        model=req.model,
        prev_hash=prev,
        metadata=req.metadata,
    )
    success = append_certificate(cert)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to append certificate")
    return {"certificate": cert, "chain_position": len(get_full_ledger())}


@app.get("/verify/{cert_id}")
def verify(cert_id: str):
    cert = get_certificate(cert_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    chain_status = verify_chain()
    return {"certificate": cert, "chain": chain_status}


@app.get("/chain")
def chain_status():
    return verify_chain()


@app.get("/ledger")
def ledger():
    records = get_full_ledger()
    return {"records": records, "count": len(records)}


@app.get("/bundle/export")
def export_bundle():
    records = get_full_ledger()
    chain = verify_chain()
    return {
        "format": "clp-bundle-v1",
        "chain_valid": chain["valid"],
        "record_count": len(records),
        "records": records,
    }
