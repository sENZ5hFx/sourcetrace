# Security Policy

**Product:** sourcetrace — Automated Truth-Extraction Engine  
**Maintainer:** Haley Ann Bird  
**Organization:** Swixixle / sENZ5hFx  

---

## Scope

This security policy covers all code, APIs, and integrations within this repository, including:

- The truth-extraction core engine and all static analysis parsers;
- The divergence scoring engine and footgun mapper;
- The truth pack assembly and signing layer;
- The REST API layer and all output schema definitions;
- Railway deployment infrastructure and Procfile configuration.

## Supported Versions

Only the latest commit on `main` is actively maintained.

| Version | Supported |
|---|---|
| Latest (`main`) | ✅ |
| Forks / older tags | ❌ |

## Threat Model

1. **Credential leakage** — API keys or tokens committed to history or exposed in pipeline logs;
2. **Truth pack poisoning** — maliciously crafted repositories designed to produce false or misleading truth packs that corrupt downstream consumers;
3. **IP exfiltration via API** — systematic querying of the truth-extraction API to reconstruct proprietary divergence scoring and footgun detection logic from outputs;
4. **Parser injection** — malformed source files designed to exploit vulnerabilities in the static analysis or tree-sitter parsing layer;
5. **Dependency confusion** — malicious packages introduced via `requirements.txt` mimicking legitimate dependencies;
6. **Railway/deployment exposure** — misconfigured deployment environment exposing internal API endpoints or debug surfaces;
7. **Schema version spoofing** — crafted truth packs with falsified provenance blocks or schema version identifiers.

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
- All repository inputs must be sandboxed before parsing — no arbitrary code execution from analyzed repos;
- Truth pack outputs must not expose internal scoring parameters or trade secret thresholds;
- Dependency updates must be reviewed before merging;
- API endpoints must validate and rate-limit all inputs.

## Disclosure Policy

Coordinated disclosure model. Reporters credited in changelog unless anonymity requested.

---

*Haley Ann Bird — Swixixle / sENZ5hFx*
