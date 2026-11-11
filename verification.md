# VSA-2026-062 verification

## Feasibility gate (preflight, 2026-11-11)

**Decision: conditional.** Do not author or claim a validated template until both pinned application revisions build and run, and the proposed GET-only probe yields a specific positive and negative response.

1. **Observable behavior:** Vates documents an unauthenticated authentication-token type confusion in Xen Orchestra's REST API. A GET request to the current-user endpoint may distinguish an affected server from a fixed one. The probe must not request token IDs or call a mutation endpoint. Successful authentication may update token last-use metadata. A redirect alone is insufficient; compare it with an unauthenticated baseline and require a user-record location.
2. **Product controls:** The affected source is Vates commit `724402733b2381d93372db0183e21df9d2c457f7`; the fix is its direct child `50166fe3a49c02069d35ba9046ca4a1f77f4e11d` (vendor PR 10748). Both are publicly obtainable from the official repository under AGPL-3.0-or-later. These source revisions must be built and run as the application, with separate Redis data.
3. **Execution invariants:** The bug is JavaScript token parsing and database lookup, with no published native timing, memory-layout, or CPU requirement. The host is ARM64, has Node 22 and Docker; Vates' installation guide validates Debian 12 x64, so ARM64 application behavior must be established rather than assumed. Approximately 14 GiB is free; dependency installation and build must stay within that limit. No full-product test has been run yet.
4. **Isolation and recovery:** Run both XO instances only on a private Docker network, with no host exposure. Use lab-only accounts and tokens, separate Redis instances, no XCP-ng host, and disposable containers. The GET probe can update token last-use metadata on an affected target.
5. **Prerequisites:** Vates publishes source and the fix. Redis is already available locally. Yarn and build dependencies are not yet installed; install only if the pinned application build is feasible in the available space. No proprietary appliance or account is required for the source installation.
6. **Evidence threshold:** On the affected build, require a valid current-user response through the test cookie, while anonymous and malformed-token controls deny access. On the fixed build, require denial for the same test cookie and a separate known-valid-token request to prove the server and route are healthy. Repeat the positive and fixed controls; retain sanitized application and scanner evidence.
7. **General-use limitation:** The vendor says the bypass selects an existing unexpired token. An instance without one may appear negative despite affected code. A lab-created token proves the code path but not universal deployment coverage. Record this limitation and assess whether a normal unauthenticated Nuclei check is suitable before any upstream submission.

The preflight did not itself establish behavior. The actual-product tests below satisfied its conditional requirements.

## First build attempt

The pinned affected source was fetched. A Linux ARM64 Node 24 container reached dependency compilation, then failed while linking `fuse-native`: its bundled `libfuse.so` had the wrong binary format for ARM64. This is an architecture incompatibility in a dependency, not evidence about the vulnerability. The failed install used lab-owned files only. The next bounded attempt used a Linux AMD64 container, matching the vendor's documented platform. Dependency installation and the XO server build succeeded. A bundled `libfuse.so` needed a lab-local SONAME symlink to start in the pinned Node image. No workstation library was changed. Docker initially ran out of internal disk space; pruning build cache older than 24 hours recovered 3.538 GB and allowed the fixed build to complete. No application images or volumes were deleted for that recovery.

## Actual-product validation

The [repeatable verifier](tests/verify.py) ran both source revisions with a fresh, disposable Redis state. The exact template SHA-256 was `b50b35d8392050e61967d26307fa3180d9c55c03e8f4a5b8b38803b176c287d0`. The scanner was the pinned Nuclei v3.11.1 Docker image. The sanitized results are in [the run report](evidence/20261111T181459Z/report.json).

| Control | Affected parent `7244027` | Fixed commit `50166fe` |
| --- | ---: | ---: |
| Crafted cookie before a token exists | 401 | 401 |
| Lab token created | 201 | 201 |
| Anonymous current-user request | 401 | 401 |
| Malformed string token | 401 | 401 |
| Crafted empty-object cookie | 307 user redirect | 401 |
| Valid lab token | 307 user redirect | 307 user redirect |
| Nuclei findings | 1 | 0 |

The Nuclei template matches the `307` redirect's `Location` header and does not follow it or request token IDs. Successful authentication updates the token's last-use metadata in XO; the check is GET-only but not free of server-side writes. A first matcher that expected a final `200` failed because Nuclei's raw HTTP request did not follow the redirect; the corrected final bytes above passed both product controls. The lab-only `GET` response, when followed manually for research, contained account fields; their values were not saved in publishable evidence.

**Status: passed for the stated detector. Evidence level: actual product source build.** The target was the complete open-source XO server built from the vendor's revisions, not a mock endpoint. The lab did not install the packaged 6.9.2/6.10.1 releases or an XOA appliance, and did not test broad internet deployment. The detector requires an existing unexpired token on the target; an affected installation with no such token is a false negative for this technique. The scanner itself uses no credentials or target-specific IDs. No exploit actions, token extraction, or external scanning were run.

## Resource cleanup

The `xo-vsa062` and `xo-vsa062-verify` local Compose projects used isolated networks, XO containers, and Redis containers with tmpfs data. The verifier removed its project after testing; the manual project was also removed. No cloud access, firewall rule, SSH key, or external account was created. The source checkout, Yarn cache, pinned images, and local evidence remain for review and reruns.

## Primary sources

- Vates advisory: https://docs.vates.tech/security-advisories/advisories/2026/vates-sa-2026-062/
- Vates fix: https://github.com/vatesfr/xen-orchestra/pull/10748
- Official source installation guide: https://github.com/vatesfr/xen-orchestra/blob/master/docs/docs/getting-started/install-from-sources.md
