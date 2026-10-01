# Feasibility gate — Bifrost CVE-2026-86242

Status: feasible. Build stage pending.

- Observation: Unaunthenticated `POST /api/plugins` with enabled plugin and controlled HTTP URL; vulnerable gateway performs outbound GET. A per-request Interactsh callback is the Nuclei proof; a local callback collector will independently record application-side traffic in the lab. This proves SSRF, not dynamic plugin RCE.
- Positive: official `maximhq/bifrost:v1.6.2` linux/arm64 image, manifest sha256:c4de3a1d6bd2f9b8b0b8f508deaaf0337a793603d2b84b61138cdb35f94a4318; clearly affected per upstream advisory `<1.6.3`.
- Negative: official `maximhq/bifrost:v2.1.0` linux/arm64 image, manifest sha256:653b74a8410e5757375aa9a25ce21f90f4591fc11d65879451939b6172ce80ed; tagged fix rejects unauthenticated custom HTTP plugin path before loading.
- Execution: native arm64 Docker Engine 27.5.1, 12 CPUs, ~8 GiB RAM; HTTP listener and gateway need no timing, kernel, hardware or hypervisor properties.
- Isolation: dedicated Compose network, loopback ports only if needed, disposable gateway data, unique plugin name and DELETE cleanup. Inert HTTP body, never a loadable shared object.
- Product prerequisites: public official images, no license/credentials; default management auth disabled.
- Expected: vulnerable gateway GET reaches collector with unique token; fixed returns 403 and no callback; generic reflection, wrong product and disabled plugin should not match. Require correlated callback and gateway logs; response error alone is insufficient.

## Validation result — passed (actual product)

- Nuclei v3.11.0 schema validation passed. Docker Compose runner: `python3 tests/verify.py /Users/alex/.local/state/nuclei-template-builds/2026-10-01/bifrost-ssrf`; successful run `evidence/85488f7bc6fd/summary.json`, template SHA-256 `d1aefca7473c88ce0a657b9c57246b055ec2726fe9e0c594f2e35d536ad42f1c`.
- Official Bifrost v1.6.2: one finding with correlated `GET /bifrost-86242` Interactsh HTTP callback; the gateway returned its product-specific 500. Official v2.1.0: zero findings; direct fixed request returned 403 with no callback (`evidence/preflight/patched-response.txt`).
- A post-failure `GET /api/plugins` on the same vulnerable lab volume returned `{"count":0,"plugins":[]}` (`evidence/preflight/post-failure-list.txt`). The 500 path in v1.6.2 calls `DeletePlugin` before responding. Its downloaded temporary plugin file may remain, so the template is tagged intrusive.
- Scope: confirms unauthenticated outbound HTTP fetch with dashboard auth disabled. It does not prove dynamic Go plugin loading or RCE in the static image.
