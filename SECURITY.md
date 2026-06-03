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
- The cross-repo federation layer and update propagation;
- All deployment infrastructure (Railway, Procfile, nixpacks).

## Supported Versions

| Version | Supported |
|---|---|
| Latest (`main`) | ✅ |
| Forks / older tags | ❌ |

## Threat Model

1. **Credential leakage** — API keys committed to history or exposed in logs;
2. **Truth pack exfiltration** — unauthorized access to generated truth packs containing proprietary architectural knowledge;
3. **IP method reconstruction** — querying API outputs at scale to reverse-engineer divergence scoring or footgun detection algorithms;
4. **Dependency confusion** — malicious packages via `requirements.txt`;
5. **Source injection** — malformed input codebases exploiting parser logic;
6. **Federation poisoning** — malicious upstream truth packs corrupting downstream reality maps;
7. **Deployment exposure** — Railway/nixpacks misconfiguration exposing debug endpoints;
8. **Output exfiltration** — truth packs downloaded at scale to reconstruct proprietary methods.

## Reporting a Vulnerability

Do **not** open a public GitHub issue.

- Use the **"Security" tab → "Report a vulnerability"** on GitHub.
- Include: description, reproduction steps, affected module, commit SHA, suggested fix.

## Response Timeline

| Stage | Target SLA |
|---|---|
| Acknowledgment | 72 hours |
| Severity assessment | 5 business days |
| Patch / mitigation | 14 days (critical), 30 days (medium) |
| Public disclosure | Coordinated with reporter |

## Security Hardening Requirements

- All API keys via environment variables only — never hardcoded;
- No credentials committed to repository history;
- All endpoints validate and sanitize input before processing;
- Truth pack outputs must not expose raw file system paths or infrastructure details;
- Dependencies reviewed before merging;
- Federation ingestion must schema-validate upstream truth packs;
- No debug endpoints in production;
- Dry-run mode default for all destructive operations.

## Disclosure Policy

Coordinated disclosure. Reporters credited in changelog unless anonymity requested.

---

*Haley Ann Bird — Swixixle / sENZ5hFx*
