# Security Policy

**Product:** Sourcetrace — Automated Truth-Extraction & Codebase Reality Mapping Engine  
**Maintainer:** Haley Ann Bird  
**Organization:** Swixixle / sENZ5hFx  

---

## Scope

This security policy covers all code, APIs, and integrations within this repository, including:

- The core truth-extraction engine and static analysis passes;
- The contradiction detector and footgun scanner;
- The truth pack serialization layer and schema definitions;
- The REST API layer and all external-facing endpoints;
- Railway deployment configuration.

## Supported Versions

Only the latest commit on `main` is actively maintained.

| Version | Supported |
|---|---|
| Latest (`main`) | ✅ |
| Forks / older tags | ❌ |

## Threat Model

1. **Credential leakage** — API keys or tokens committed to history or exposed in logs;
2. **Truth pack exfiltration** — unauthorized access to generated truth packs exposing proprietary codebase analysis of third-party systems;
3. **Analysis result poisoning** — crafted input repositories designed to produce false or misleading truth packs;
4. **IP exfiltration via API** — systematic API querying to reverse-engineer the internal contradiction detection or footgun classification logic;
5. **Dependency confusion** — malicious packages introduced via `requirements.txt` updates;
6. **Deployment environment exposure** — Railway misconfiguration exposing internal analysis endpoints;
7. **Git history injection** — forged commits attempting to pollute the provenance record of truth packs.

## Reporting a Vulnerability

Do **not** open a public GitHub issue to report security vulnerabilities.

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
- Truth pack outputs must not embed raw API credentials or filesystem paths;
- All API endpoints must validate and sanitize input before dispatching analysis;
- Dependency updates must be reviewed before merging;
- Railway deployment must not expose debug or admin endpoints in production.

## Disclosure Policy

Coordinated disclosure model. Reporters credited in changelog unless anonymity requested.

---

*Haley Ann Bird — Swixixle / sENZ5hFx*
