# CVE-2026-118539 verification

Status: **author validation passed for the tested order-route behavior in both affected Commerce Core branches**. Independent reviewer and validator reruns of these final bytes are pending. The earlier independent reports cover a superseded 3.x-only draft.

## Feasibility and scope

The Drupal advisory identifies affected Commerce Core versions before 8.x-2.41 and 3.0.0 through 3.3.12. The official 3.x and 2.x patches add the `access commerce administration pages` requirement to order administration routes. In both branches, the state-machine order transition confirmation route had been reachable by a customer with update access to their own draft cart order. The safe observation is a GET of `/admin/commerce/orders/{{order_id}}/state/place`; the template never submits that form or changes the order. The prerequisite is a supplied ordinary customer account and that customer's existing draft order ID.

One template covers both branches because the same exact route and form ID were observed on both vulnerable controls, and the same permission barrier was observed on both fixed controls. This does not test every route or field access flaw covered by the advisory.

## Product and lab provenance

- Official Drupal 10.6.20 PHP 8.3 Apache image, pinned by digest `sha256:fbf47235f54bbb4801923e4fe8574029e8975016bc28766ecd02a65a31926870`, with PHP bcmath added in `lab/Dockerfile.drupal`.
- Commerce Core 3.3.12 and 3.3.13, corresponding to official Git tags `3.3.12` and `3.3.13`.
- Commerce Core Composer versions 2.40.0 and 2.41.0, corresponding to official Git tags `8.x-2.40` and `8.x-2.41`.
- Four separate SQLite-backed Drupal sites. `lab/create-fixture.php` creates an online store, ordinary customer, and customer-owned draft cart order ID 1. It confirms the customer can update that order. No additional admin role is granted.
- Composer dependency versions are pinned by the four `lab/locks/*/composer.lock` files. `lab/setup.sh` copies the lock pair and uses `composer install` for each variant. A clean run in `/tmp/drupal-commerce-four-branch-clean-20261030` recreated all four sites, with matching lockfiles and identical fixture IDs/access results.
- The scanner is Nuclei v3.11.1 from `projectdiscovery/nuclei@sha256:582d5546902e67052097cb2d07296c642d50a1afc5e44623cb038845df9a32eb`; the template mount is read-only. Docker architecture: Linux arm64.

## Final exact-byte results

Final template SHA-256: `46b137565a7a9715259d3627ed64f0b4be6db520efd601bc0f31aa63e100b801`. The installed lab and the independently recreated clean lab each passed the same 11 Nuclei scenarios on these bytes. Both test projects were removed by the runner. Sanitized results, including application-side HTTP status checks, are in `evidence/final-sanitized.md`. A separate pinned Nuclei `-debug` run captured the request and response for the privilege-denial control and final GET on all four product versions. Redacted excerpts are in `evidence/redacted-nuclei-debug.md`; original logs remain private and are excluded from the reviewer package.

| Target / supplied account | Findings | Admin denial control | Final GET |
| --- | ---: | ---: | ---: |
| Commerce 3.3.12, ordinary customer, own draft order | 1 | 403 | 200, matching transition form |
| Commerce 3.3.13, same fixture | 0 | 403 | 403 |
| Commerce 2.40.0, ordinary customer, own draft order | 1 | 403 | 200, matching transition form |
| Commerce 2.41.0, same fixture | 0 | 403 | 403 |

Additional controls on both branch families produced zero findings: incorrect password, nonexistent order, and administrator account. The missing order returned 404 on the vulnerable control. The administrator reached the admin control with HTTP 200, causing the flow to stop before the final probe. A login failure also stopped the flow. These are healthy negative responses, not timeouts or unreachable targets.

The final file passed the upstream `.yamllint` configuration, `git diff --check`, and Nuclei's normal template validation in the lab runner. ProjectDiscovery's `metadata.verified: true` debug-evidence requirement is met by the redacted request/response excerpts above. The upstream CI weak-matcher job probes an external honeypot and was not run in this local-only task.

## Reproduction

From a clean copy of the sanitized evidence package, with Docker Engine/Compose v2 and Python 3:

```bash
bash lab/setup.sh
python3 tests/verify.py "$(pwd)"
```

The script refuses to overwrite existing lab installation directories. The runner starts only its uniquely named Compose project, verifies target health, schema-validates the mounted template, runs all positive and negative scenarios, and removes that project. The generated application directories and raw runner outputs are local-only. The package includes source and lockfiles but excludes generated Drupal installs, session-bearing debug logs, and credentials beyond the disposable fixture account values in the scripts.

## Upstream status and limits

The official template tree was refreshed on 2026-10-30 at `5cfe87d58464ab47a871d0be3d2844bf51e6eda5`; no CVE-specific or Drupal Commerce template path was present. GitHub issue/PR search for this CVE returned zero results. Recheck before external submission because upstream can change.

A finding establishes only the tested authenticated order state-transition route bypass for the supplied order. It requires a pre-existing customer account and draft order ID. It does not enumerate orders, submit transitions, prove financial impact, or cover the advisory's other access paths. No live external system was scanned. No branch was pushed and no PR was created.
