# Feasibility gate — Elementor REST nonce bypass

Status: feasible. Build stage pending.

- Observation: with the same legitimate admin cookie and no REST nonce, GET `/wp-json/wp/v2/settings` is rejected; adding exact `elementor/v1/events/` query marker returns protected settings JSON on 4.3.0. Patched 4.3.2 rejects it.
- Positive/control artifacts: official `elementor.4.3.0.zip` and `elementor.4.3.2.zip` both returned HTTP 200 from `downloads.wordpress.org`, 23,146,934 and 23,604,020 bytes. Cached native arm64 WordPress 7.1.0/PHP8.3 Apache and MariaDB 11.4 images are available, pinned by local repo digests.
- Execution: native arm64 Docker; no timing or architecture properties. Editor Events experiment must be active for positive. Use admin account/cookie only in isolated lab.
- Isolation: separate WordPress/DB pairs on dedicated Compose network with disposable volumes; no state-changing REST probe. Lab-only admin credentials.
- Product prerequisites: public GPL plugin ZIPs, no activation/license. Need CLI setup of WordPress and plugin in lab; confirm feature enabled.
- Expected: vulnerable exact marker 200 settings JSON while baseline/near-miss/no-cookie and patched exact marker deny access. An HTTP 200 alone or product version string is insufficient.

## Validation result — passed (actual product)

- Nuclei v3.11.0 schema validation passed. Docker Compose runner: `python3 tests/verify.py /Users/alex/.local/state/nuclei-template-builds/2026-10-01/elementor-csrf`; successful run `evidence/5c6ec6fe1fe1/summary.json`, template SHA-256 `751fa07576fb3b54bd9933b3b42e754f87e951a8941849c8d3f01b81e580fe76`.
- Official Elementor 4.3.0 in WordPress 7.1.0: valid administrator cookie without REST nonce yields 401 baseline, 401 near-miss, 200 settings JSON on exact `elementor/v1/events/` query marker. Official Elementor 4.3.2: zero findings and exact marker denied. Invalid cookie on 4.3.0: zero findings. The lab explicitly enables Editor Events.
- The only test mutation is disposable WordPress installation and local administrator creation. The template itself is read-only. Supply an authorized admin cookie with `-var token='wordpress_logged_in_<hash>=...'`; do not send a real cookie to an untrusted target.
- Scope: proves a REST nonce bypass for an authenticated administrator session under the stated module prerequisite; it does not claim anonymous access.
