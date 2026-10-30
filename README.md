# CVE-2026-118539 local reproduction package

This package reproduces the authenticated Drupal Commerce order-route detector on actual local vulnerable and patched installations for both supported branches. It contains only public source references, pinned Composer metadata, scripts, and sanitized findings. Generated Drupal sites, raw HTTP/debug logs, and session material are excluded.

Requirements: Docker Engine with Compose v2, Python 3, and available network access to the official pinned Drupal image and Composer package downloads during the first setup.

```bash
bash lab/setup.sh
python3 tests/verify.py "$(pwd)"
```

The setup refuses to overwrite existing installations. The runner uses a unique Docker Compose project, starts only the four local targets, validates the exact template, runs 11 scenarios, and tears down that project. `verification.md`, `evidence/final-sanitized.md`, and `evidence/redacted-nuclei-debug.md` describe the expected outcomes, redacted Nuclei request/response proof, and limitations. The generated lab application directories stay local until manually removed.
