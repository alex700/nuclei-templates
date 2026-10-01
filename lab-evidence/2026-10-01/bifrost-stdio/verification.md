# Feasibility gate — Bifrost CVE-2026-90898

Status: feasible for build. Confirm actual runtime callback and schema before setting validation status.

- Observation: unauthenticated `POST /api/mcp/client` registering a stdio client starts its command before MCP handshake. A per-request Interactsh callback would prove command execution.
- Positive: official `maximhq/bifrost:v2.0.0` linux/arm64, manifest sha256:cf71be9fad4e0749b6e26cbb774c687413dad9a0970b83f4e1dadb6f503ea208.
- Negative: official `maximhq/bifrost:v2.1.0` linux/arm64, manifest sha256:653b74a8410e5757375aa9a25ce21f90f4591fc11d65879451939b6172ce80ed; source patch rejects unauthenticated stdio registration with 403.
- Execution: native arm64 Docker; no timing or kernel dependency. Tagged v2.0.0 Dockerfile uses Alpine `/bin/sh` and BusyBox `wget` in HEALTHCHECK. Verify actual runtime before authoring.
- Isolation: dedicated Compose network, disposable registry DB, unique client name and DELETE cleanup; no shell payload on workstation.
- Product prerequisites: official public images, management auth disabled by default.
- Expected: vulnerable gateway executes harmless outbound request and collector logs unique path; fixed returns 403 and no callback. API acceptance or spawn-error alone is insufficient.

## Validation result — passed (actual product)

- Nuclei v3.11.0 schema validation passed. Docker Compose runner: `python3 tests/verify.py /Users/alex/.local/state/nuclei-template-builds/2026-10-01/bifrost-stdio`; successful run `evidence/10bf73e66254/summary.json`, template SHA-256 `4f6098a575c4afe5a4621543b818714fd8c0d8a996fdca0f8b09e8310c8eda23`.
- Official Bifrost v2.0.0: two findings for one request because its MCP connection retry launched the harmless `/bin/sh`/`wget` callback twice; both callbacks share the same Nuclei interaction ID. The 500 response reports MCP handshake timeout after the command. Official v2.1.0: zero findings; direct fixed request returned 403 with no callback (`evidence/preflight/patched-response.txt`).
- A post-failure `GET /api/mcp/clients` on the same vulnerable lab volume returned an empty client list (`evidence/preflight/post-failure-list.txt`). The matched 500 path in v2.0.0 calls `DeleteMCPClientConfig` before responding.
- Scope: confirms shell command execution on the native ARM64 official image with dashboard auth disabled. The 45-second timeout accommodates the product's 30-second MCP handshake failure; the request is intrusive and should run only against authorized targets.
