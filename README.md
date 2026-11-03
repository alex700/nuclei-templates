# CVE-2026-118539 guest-cart reproduction package

This package builds four isolated actual-product Drupal Commerce installations and two additional controls, then runs the exact site-root Nuclei template. It requires no scanner account or known order ID. Setup creates one public standard product per affected/fixed site, a copy with no public product, and a copy whose first public product is ID 13. A successful scan creates one persistent anonymous draft cart. No checkout or order state transition is submitted. The scanner samples 63 product IDs at most, using odd non-round increments after IDs 1-10, and stops at the first matched standard add-to-cart form. A failed add-to-cart POST yields no finding; the scan does not continue to later IDs.

Requirements: Docker Engine with Compose v2, Python 3, and network access to the pinned Drupal image and Composer packages for initial setup.

```sh
bash lab/setup.sh
python3 tests/verify.py "$(pwd)"
```

Setup refuses to overwrite existing lab installations. The runner uses a unique Compose project, validates the template under pinned Nuclei v3.11.1, checks all six controls, and removes the Compose containers/network. Generated Drupal directories and raw local debug logs remain until separately reviewed and removed. Raw logs can contain disposable session material and must not be published. The publishable summary is `evidence/redacted-guest-cart-debug.md`.

A finding proves only guest access to its own draft order state-transition confirmation form in the tested standard cart configuration. It does not submit the form, establish all paths in the Drupal advisory, or show that every site has a public product among the sampled IDs. A missing finding is inconclusive.
