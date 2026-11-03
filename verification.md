# Guest-cart verification

Status: **author validation and independent review passed for the narrow guest-cart chain**. The tested file is `template.yaml` with SHA-256 `d51b7a1bebcaa7a1e202d4dedbed305a4372a4c416f616944f48e96eb5ea2c1a`. Nuclei v3.11.1 ran from the image digest pinned in `lab/compose.yaml`. Drupal Core was 10.6.20, with Commerce Core packages locked at 3.3.12, 3.3.13, 2.40.0, and 2.41.0. Two additional 3.3.12 controls removed the public product or exposed it only at ID 13. All sites were rebuilt from the pinned locks by `bash lab/setup.sh`; the six-case runner then passed on the exact template bytes and removed its Compose containers/network.

| Control | Product GETs | Guest cart POSTs | Final admin GET | Findings |
| --- | ---: | ---: | --- | ---: |
| affected_3x | 1 | 1 | 200 | 1 |
| fixed_3x | 1 | 1 | 403 | 0 |
| affected_2x | 1 | 1 | 200 | 1 |
| fixed_2x | 1 | 1 | 403 | 0 |
| no_public_product | 63 | 0 | not sent | 0 |
| later_product_13 | 11 | 1 | 200 | 1 |

The runner asserts findings by template ID, sequential product request counts, one cart POST when a product is selected, the final administrative status, and presence or absence of the exact state-transition form. The two affected versions returned HTTP 200 with the form; the two fixed versions returned 403. The no-product control sent all 63 product GETs and no POST. The later-product control stopped at ID 13 after 11 GETs. A fresh anonymous session was denied (403) at the affected 3.3.12 guest-cart admin route, and `/jsonapi` returned 404 in that lab. No order transition or checkout was submitted.

Validation commands were `bash lab/setup.sh` and `python3 tests/verify.py "$(pwd)"` in this package. A complete clean six-site setup and rerun passed. The successful local run is under ignored `evidence/22e060d1ae73/`; its `summary.json` reports `assertions_passed: true` and `cleanup_passed: true`. `evidence/redacted-guest-cart-debug.md` is the publishable summary. Raw runner debug output is retained locally only and may contain disposable session values. Nuclei schema validation, the repository's `.yamllint` rules, and `git diff --check` passed for the proposed upstream file. The weak-matcher honeypot CI and other upstream checks have not run on these bytes.

Limitations: product ID sampling is not guaranteed discovery, and no finding is inconclusive. Standard add-to-cart markup and default cart View were tested; custom storefronts were not. The first matching form stops product search even if its add-to-cart POST later fails. One anonymous draft cart remains per successful scan. This validates one route behavior, not all CVE paths or financial effects. The existing upstream PR remains closed while the independently reviewed local evidence and template await Alex's publication decision.
