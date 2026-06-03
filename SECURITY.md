# Security Policy

**Product:** Sourcetrace — Automated Truth-Extraction Engine
**Maintainer:** Haley Ann Bird
**Organization:** Swixixle / sENZ5hFx

---

## Scope

This security policy covers all code, APIs, and integrations within this repository, including:

- The truth-extraction engine and all static analysis modules;
- The divergence detection and footgun identification pipeline;
- The truth pack schema, versioning, and diff engine;
- The REST API layer and all external-facing endpoints;
- The cross-repo federation layer and upstream/downstream update propagation;
- All deployment infrastructure (Railway, Procfile, nixpacks, etc.).

## Supported Versions

Only the latest commit on `main` is actively maintained.

| Version | Supported |
|---|---|
| Latest (`main`) | ✅ |
| Forks / older tags | ❌ |

## Threat Model

1. **Credential leakage** — API keys or tokens committed to history or exposed in logs;
2. **Truth pack exfiltration** — unauthorized access to generated truth packs containing proprietary architectural knowledge;
3. **IP method reconstruction** — querying the API at scale to reverse-engineer divergence scoring or footgun detection algorithms;
4. **Dependency confusion** — malicious packages introduced via `requirements.txt`;
5. **Source injection** — malformed input codebases crafted to exploit parser logic;
6. **Federation poisoning** — malicious upstream truth packs injected to corrupt downstream reality maps;
7. **Deployment exposure** — Railway or nixpacks misconfiguration exposing internal services;
8. **Output exfiltration** — truth packs downloaded at scale to reconstruct proprietary methods.

## Reporting a Vulnerability

Do **not** open a public GitHub issue for security vulnerabilities.

- **GitHub Private Vulnerability Reporting:** Use the "Security" tab → "Report a vulnerability."
- Include: description, reproduction steps, affected module, commit SHA, and optional suggested fix.

## Response Timeline

| Stage | Target SLA |
|---|---|
| Acknowledgment | 72 hours |
| Severity assessment | 5 business days |
| Patch / mitigation | 14 days (critical), 30 days (medium) |
| Public disclosure | Coordinated with reporter |

## Security Hardening Requirements

- All API keys and tokens must be loaded via environment variables, never hardcoded;
- No credentials may be committed to repository history;
- All endpoints must validate and sanitize input before processing;
- Truth pack outputs must not expose raw file system paths or internal infrastructure details;
- Federation ingestion must validate and schema-check upstream truth packs before processing;
- Railway deployment must not expose debug endpoints in production;
- Dry-run mode must be default for any destructive analysis operation.

## Disclosure Policy

Coordinated disclosure model. Reporters credited in changelog unless anonymity requested.

---

*Haley Ann Bird — Swixixle / sENZ5hFx*
