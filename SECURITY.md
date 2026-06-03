# Security Policy

**Product:** Sourcetrace — Automated Truth-Extraction & Codebase Reality Mapping Engine
**Maintainer:** Haley Ann Bird
**Organization:** Swixixle / sENZ5hFx

---

## Scope

This security policy covers all code, APIs, and integrations within this repository, including:

- The static analysis and truth extraction core;
- The contradiction detection and footgun cataloging engine;
- The truth pack generation and serialization layer;
- The API serving layer and all external endpoints;
- Railway deployment configuration.

## Supported Versions

Only the latest commit on `main` is actively maintained.

| Version | Supported |
|---|---|
| Latest (`main`) | ✅ |
| Forks / older tags | ❌ |

## Threat Model

1. **Credential leakage** — API keys or tokens committed to history or exposed in pipeline logs;
2. **Truth pack tampering** — unauthorized modification of emitted truth pack artifacts to suppress or alter footgun or contradiction findings;
3. **IP exfiltration via API** — systematic querying of the truth extraction API to reconstruct proprietary analysis heuristics from outputs;
4. **Malicious repository input** — crafted repositories designed to exploit parser vulnerabilities in the static analysis core;
5. **Dependency confusion** — malicious packages introduced via `requirements.txt` mimicking legitimate dependencies;
6. **Deployment exposure** — Railway misconfiguration exposing internal analysis endpoints without authentication;
7. **Output injection** — truth pack serialization exploits embedding executable content in emitted artifacts.

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
- Truth pack outputs must be schema-validated before serialization;
- Repository inputs must be sandboxed — analysis must not execute arbitrary code from analyzed repos;
- API endpoints must require authentication tokens before serving truth pack data;
- Dependency updates must be reviewed before merging;
- Deployment config must not expose debug or internal endpoints in production.

## Disclosure Policy

Coordinated disclosure model. Reporters credited in changelog unless anonymity requested.

---

*Haley Ann Bird — Swixixle / sENZ5hFx*
