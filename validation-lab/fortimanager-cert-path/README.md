# Feasibility and scope

Narrow maintenance correction: verify whether the template's keysDir variable prevents the existing Python certificate-loading function from loading the bundled certificate. Existing Nuclei v3.11.0 and Python/OpenSSL are available. Positive/control artifacts are the exact upstream function and bundled public test fixtures, with original versus corrected directory variable. Run only this function; do not call check_vulnerability or main, create sockets, or scan a target. An isolated Docker network-none control can reproduce the same Python path.

This is feasible as a code-path reproducer for a resource-loading defect. Actual FortiManager vulnerable/fixed appliances are not available; full vulnerability-detection verification is blocked and will not be claimed. No new vulnerability template or target lab will be constructed. A draft maintenance PR may disclose partial product validation with meaningful loader evidence.

## Observed results

Nuclei v3.11.0 executed signed, locally generated code-path fixtures containing only the exact certificate-loading function extracted by AST. No network calls or original main/check_vulnerability were included. Original variable: CERT_LOADED=False. Corrected variable: CERT_LOADED=True. Both expected assertions matched, exit zero. Temporary test signing keys were deleted automatically. Docker Python 3.12 Alpine network-none controls reproduced false/true with repository mounted read-only. This proves loader behavior only, not FortiManager detection.

Reproduce: python3 tests/verify.py /path/to/nuclei-templates (requires nuclei v3.11.0, Python 3, OpenSSL). Evidence is written to evidence/. Original upstream digest is preserved in the one-line maintenance diff; upstream signing automation must refresh it after acceptance.
