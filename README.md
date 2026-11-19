# Apache Roller XML-RPC extension detector: reviewer reproduction

This package reproduces the benign parser-policy check used by `apache-roller-xmlrpc-extensions.yaml`. It detects the same issue across releases assigned CVE-2026-129448 and CVE-2026-82384, without trying to infer the release version from the response. It does not send a serialized Java object or attempt code execution. It uses official Apache Roller 6.1.4, 6.1.5, and 6.1.6 binary releases, verified against Apache's SHA-256 files.

## Run

Requirements: Docker with Compose v2, Python 3.9 or later, `curl`, and network access to the Apache archive and Maven Central for the first download. On an arm64 or amd64 host, run from this directory:

```sh
python3 tests/verify.py "$(pwd)"
```

The runner downloads and verifies release archives, starts three disposable Roller/PostgreSQL pairs with loopback-only host ports, completes product setup using lab-only accounts, runs Nuclei v3.11.0 from a pinned Docker image with the template mounted read-only, asserts one finding each on 6.1.4 and 6.1.5 and zero on 6.1.6 in both XML-RPC configurations, saves evidence under `evidence/<run-id>/`, and removes only its own Compose project.

The first-run setup token is read from the local fixed-version container log and is never printed. Raw application logs in a local run may still contain that token; do not post those logs without redaction.

## What the result means

The template detects an unauthenticated XML-RPC endpoint accepting a benign vendor extension value into method dispatch. Apache's fix disables extension types. The finding is a safe indicator for this vulnerable parser configuration, not a demonstration of the advisory's code-execution impact. See `evidence/http-differential.md` and `sources.md` for the observed responses and attribution.
