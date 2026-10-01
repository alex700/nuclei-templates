# Reproducible labs for three Nuclei findings

These packages validate the template files in the separate PR branches against official vulnerable and patched product images. They run only disposable local Docker services. The Bifrost templates make outbound Interactsh callbacks; run them only where outbound HTTP is permitted. Elementor requires an admin cookie generated inside its local lab.

From this branch's repository root:

```sh
python3 lab-evidence/2026-10-01/bifrost-ssrf/tests/verify.py "$PWD/lab-evidence/2026-10-01/bifrost-ssrf"
python3 lab-evidence/2026-10-01/bifrost-stdio/tests/verify.py "$PWD/lab-evidence/2026-10-01/bifrost-stdio"
python3 lab-evidence/2026-10-01/elementor-csrf/lab/prepare.py
python3 lab-evidence/2026-10-01/elementor-csrf/tests/verify.py "$PWD/lab-evidence/2026-10-01/elementor-csrf"
```

The pinned official Elementor ZIPs are downloaded and checked by SHA-256; they are omitted from this branch. Successful-run evidence and manifests are next to each package. Elementor's public logs redact its disposable test cookie; the runner creates full raw evidence locally. The two Bifrost labs show that the failed registration paths leave no database records, although the SSRF request may leave a temporary downloaded file in the container.

Issabel JWT and PIAF-HMS SQL injection were gated as blocked for full product validation; no templates or PRs are offered for them. Their gate notes are in the local build record, not this evidence branch.
