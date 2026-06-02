# Security Policy

**Product:** Sourcetrace — Automated Truth-Extraction Engine  
**Maintainer:** Haley Ann Bird  
**Organization:** Swixixle / sENZ5hFx  

---

## Scope

This security policy covers all code, APIs, and integrations within this repository, including:

- The core truth-extraction and static analysis engine;
- The guarantee scanner and lie detection pipeline;
- The truth pack schema and API endpoints;
- The fear-surface mapper and onboarding export layer;
- All deployment infrastructure (Railway, nixpacks, Procfile).

## Supported Versions

Only the latest commit on `main` is actively maintained.

| Version | Supported |
|---|---|
| Latest (`main`) | ✅ |
| Forks / older tags | ❌ |

## Threat Model

1. **Credential leakage** — API keys committed to history or exposed in analysis output;
2. **Source code exfiltration** — unauthorized use of analyzed codebases passed through the pipeline without operator consent;
3. **Truth pack poisoning** — maliciously crafted truth packs injected into downstream consumers (threshold, firstlight) to corrupt onboarding output;
4. **Lie detection bypass** — crafted documentation that exploits parser edge cases to suppress legitimate contradiction flags;
5. **Fear-surface data leakage** — truth pack outputs exposing internal architecture of analyzed codebases to unauthorized parties;
6. **Dependency confusion** — malicious packages introduced via `requirements.txt` mimicking legitimate dependencies;
7. **API abuse** — unauthenticated bulk calls to analysis endpoints enabling competitive reverse engineering of the engine.

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

- All API keys must be loaded via environment variables, never hardcoded;
- Truth pack outputs must not include raw source code from analyzed repositories;
- Analysis endpoints must validate input size and type before processing;
- Dependency updates must be reviewed before merging;
- Railway deployment must not expose debug or internal analysis endpoints in production.

## Disclosure Policy

Coordinated disclosure model. Reporters credited in changelog unless anonymity requested.

---

*Haley Ann Bird — Swixixle / sENZ5hFx*
