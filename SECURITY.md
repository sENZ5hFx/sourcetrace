# Security Policy

**Product:** Sourcetrace — Automated Truth-Extraction & Codebase Reality Mapping Engine
**Maintainer:** Haley Ann Bird
**Organization:** Swixixle / sENZ5hFx

---

## Scope

This security policy covers all code, APIs, and integrations within this repository, including:

- The core truth-extraction engine and AST analysis pipeline;
- The reality-gap scoring and footgun detection modules;
- The REST API layer and all external-facing endpoints;
- The truth pack serialization and deserialization layer;
- All deployment infrastructure (Railway, Procfile, nixpacks).

## Supported Versions

Only the latest commit on `main` is actively maintained.

| Version | Supported |
|---|---|
| Latest (`main`) | ✅ |
| Forks / older tags | ❌ |

## Threat Model

1. **Credential leakage** — API keys or tokens committed to history or exposed in pipeline logs;
2. **IP exfiltration via API** — systematic querying of the truth pack API to reconstruct proprietary scoring logic from outputs;
3. **Truth pack tampering** — unauthorized modification of serialized truth pack artifacts to corrupt reality-gap findings;
4. **Dependency confusion** — malicious packages introduced via `requirements.txt` updates;
5. **AST parser abuse** — malformed source files crafted to trigger unintended behavior in the tree-sitter parsing layer;
6. **Deployment misconfiguration** — Railway or nixpacks config exposing internal endpoints or debug surfaces;
7. **Documentation lie injection** — crafted documentation inputs designed to manipulate lie-detection classification outputs.

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
- Truth pack outputs must not include raw source file contents that expose confidential codebases;
- API endpoints must rate-limit and authenticate requests to prevent bulk IP extraction;
- Dependency updates must be reviewed before merging;
- Deployment config must not expose debug endpoints or internal scoring parameters in production.

## Disclosure Policy

Coordinated disclosure model. Reporters credited in changelog unless anonymity requested.

---

*Haley Ann Bird — Swixixle / sENZ5hFx*
