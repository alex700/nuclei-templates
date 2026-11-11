# VSA-2026-062 Nuclei detector: reviewer reproduction

This package checks the actual Xen Orchestra server at the vendor's source
revision immediately before the fix and at the fix commit. It never requests
token IDs and does not follow the authenticated redirect. The scanner sends
two `GET /rest/v0/users/me` requests. On a vulnerable target, successful
authentication updates the selected token's last-use metadata server-side.

## Requirements

- Docker Engine with Compose v2 and Linux AMD64 container support. The recorded
  run used Docker Desktop on an ARM64 Mac, emulating AMD64 for Xen Orchestra.
- Approximately 8 GiB free disk space for the source checkout and Yarn cache,
  plus Docker image space. Node 24 and Yarn Classic are supplied by the pinned
  Node container image.
- Python 3.9 or newer.

The test creates a token in its disposable, private Redis instance solely to
exercise the vulnerable path. No token is saved or printed. This is a target
prerequisite, not a scanner credential. The default `admin@admin.net:admin`
account is used only in the isolated local lab.

## Prepare the source

Run these commands from the package root:

```sh
git clone --filter=blob:none --no-checkout https://github.com/vatesfr/xen-orchestra.git lab/source
git -C lab/source fetch --depth=2 origin 50166fe3a49c02069d35ba9046ca4a1f77f4e11d
git -C lab/source checkout --detach 724402733b2381d93372db0183e21df9d2c457f7
docker run --rm --platform linux/amd64 --cpus=4 --memory=8g --user "$(id -u):$(id -g)" \
  --mount type=bind,src="$(pwd)/lab/source",dst=/work --workdir /work \
  --env YARN_CACHE_FOLDER=/work/.yarn-cache node:24.22.1-bookworm@sha256:0925478b811e8890f5508ad2a75135933310effd45492696ecf7c111c8339d02 \
  yarn install --frozen-lockfile
ln -s libfuse.so lab/source/node_modules/fuse-shared-library-linux/libfuse/lib/libfuse.so.2
```

The symlink exposes the bundled AMD64 library under its expected SONAME in
the Node runtime image. If it already exists, do not create it again.

## Verify

```sh
docker run --rm --mount type=bind,src="$(pwd)/template.yaml",dst=/templates/template.yaml,readonly \
  projectdiscovery/nuclei@sha256:582d5546902e67052097cb2d07296c642d50a1afc5e44623cb038845df9a32eb \
  -validate -t /templates/template.yaml -duc
python3 tests/verify.py
```

The verifier builds each pinned revision, starts a fresh XO and Redis pair,
creates a lab-only token, checks anonymous and valid-token controls, runs the
exact template in Nuclei v3.11.1, and removes the Compose project. It writes
sanitized summaries to `evidence/<run>/report.json`. Private raw JSONL is
saved locally with mode 0600 and must not be published. The expected result
is one finding on the affected revision and zero on the fix revision.

The lab does not require an XCP-ng host and exposes no service to the public
network. `lab/source` and private raw scan output are not included in the
reviewer evidence branch; sanitized run summaries are included. Its
`lab/config/xo-server/config.toml` contains:

```toml
[http]
[[http.listen]]
port = 8080
[redis]
uri = "redis://redis:6379/0"
```

## Scope

This detector proves that the empty-object cookie changes an anonymous
current-user request into an authenticated user redirect when an unexpired
token exists. It does not extract the token, read the user record, or test
administrative actions. An affected installation with no unexpired token will
not match. The source revisions bracket the vendor's fix; this lab did not
install packaged XO appliance releases.
