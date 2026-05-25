from core.ledger import get_full_ledger


def verify_chain() -> dict:
    records = get_full_ledger()
    if not records:
        return {"valid": True, "count": 0, "message": "Empty ledger"}

    broken_at = None
    prev = "GENESIS"
    for i, cert in enumerate(records):
        if i > 0 and cert["prev_hash"] != prev:
            broken_at = cert["id"]
            break
        prev = cert["content_hash"]

    return {
        "valid": broken_at is None,
        "count": len(records),
        "broken_at": broken_at,
        "message": "Chain intact" if not broken_at else f"Chain broken at {broken_at}"
    }
