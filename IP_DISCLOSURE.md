# Intellectual Property Disclosure

**Project:** sourcetrace — Certified Ledger Protocol (CLP)  
**Inventor:** Haley Ann Bird  
**Email:** heyhaleybird@gmail.com  
**Location:** Fishers, Indiana, USA  
**First Committed:** 2024  
**Disclosure Updated:** 2026-06-09  
**License:** BSL-1.1 (Business Source License 1.1)

---

## NOTICE

This document constitutes a public defensive disclosure establishing a prior art record and priority date for all novel inventions described herein. All inventions are the sole intellectual property of **Haley Ann Bird**. Unauthorized use, reproduction, distribution, or commercial deployment of any described systems, methods, or algorithms is strictly prohibited without written permission.

---

## Inventions Disclosed

### 1. Certified Ledger Protocol (CLP)
**Priority Date:** 2024-01-01  
**Status:** Actively maintained — defensive disclosure filed  
**Novel Contribution:** A hash-chained, append-only provenance ledger for AI-generated content, enabling tamper-evident attribution with cryptographic linkage between successive content entries. The CLP uniquely combines SHA-256 content hashing with a GENESIS sentinel, deterministic cert ID generation via JSON-normalized hash, and structured bundle export (`clp-bundle-v1`) for portable proof chains.

### 2. AI Content Provenance Certificate (`clp-{id}` format)
**Priority Date:** 2024-01-01  
**Novel Contribution:** A structured certificate schema that captures `author`, `model`, `content_hash`, `timestamp`, `prev_hash`, and arbitrary `metadata` in a single verifiable document. The cert ID is derived from the SHA-256 hash of the JSON-serialized (sort_keys=True) certificate body, making it globally unique and deterministic without external key generation.

### 3. Hash-Chained Chain Verification Algorithm
**Priority Date:** 2024-01-01  
**Novel Contribution:** A lightweight, stateless algorithm for verifying the structural integrity of a hash-chained certificate ledger. Traverses the ordered ledger, comparing each cert's `prev_hash` against the prior cert's `content_hash`, and identifies the exact certificate ID at which chain integrity breaks.

### 4. Bundle Export Format (`clp-bundle-v1`)
**Priority Date:** 2024-01-01  
**Novel Contribution:** A portable, self-describing export format for CLP ledgers combining `chain_valid` status, `record_count`, and full ordered certificate records into a single transferable JSON document suitable for legal discovery, audit, and third-party verification.

### 5. Automated IP Audit Timestamping via CI/CD
**Priority Date:** 2026-01-01  
**Novel Contribution:** A GitHub Actions workflow that automatically appends cryptographically-anchored timestamp entries (commit SHA, UTC timestamp, branch, actor) to `.ip-timestamp` on every push touching source or IP files. Creates a continuous, append-only machine-generated evidence chain embedded directly in the repository history.

---

## Trademark Claims

- **sourcetrace™** — trademark of Haley Ann Bird
- **Certified Ledger Protocol™** — trademark of Haley Ann Bird
- **CLP™** (in the context of AI content provenance) — trademark of Haley Ann Bird

See [TRADEMARK.md](./TRADEMARK.md) for full trademark assertions.

---

## Copyright

Copyright © 2024–2026 Haley Ann Bird. All Rights Reserved.  
All source code, documentation, architecture, algorithms, and creative works in this repository are protected by copyright law.  
See [LICENSE](./LICENSE) and [COPYRIGHT_AND_ATTRIBUTIONS.md](./COPYRIGHT_AND_ATTRIBUTIONS.md).

---

## BSL License Notice

This software is licensed under the Business Source License 1.1. The Change Date is four (4) years from the first commit date. After the Change Date, the software is licensed under the Apache License 2.0. Commercial use before the Change Date requires a separate written license from Haley Ann Bird.

---

*This document was last updated by the repository owner on 2026-06-09. It is a living document and will be updated as new inventions are developed.*
