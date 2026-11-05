# Reproduce the CVE-2026-68524 benign probe

These commands run the official Apache OFBiz demo images on loopback only. Both images are AMD64; Docker Desktop on Apple Silicon uses emulation. The issue is an application request-handling flaw, not a timing or CPU-specific flaw. Docker with AMD64 support, 8 GiB of available Docker memory, and ports 18443/18444 are required.

From this candidate directory:

```sh
docker run -d --rm --platform linux/amd64 --name ig-ofbiz-68524-vuln --memory=3g --cpus=4 -p 127.0.0.1:18443:8443 ghcr.io/apache/ofbiz@sha256:b6151682feab85b5d9b834254945b821a9fc02e0327cbad0e1f5f35628934a58
docker run -d --rm --platform linux/amd64 --name ig-ofbiz-68524-fixed --memory=3g --cpus=4 -p 127.0.0.1:18444:8443 ghcr.io/apache/ofbiz@sha256:5718c99aec3470d3156cdccade1b2a48af3737b57c5a4c7da3934e4f32a5865a
```

Wait until both URLs return HTTP 200. The demo certificates are self-signed:

```sh
curl -sk -o /dev/null -w '%{http_code}\n' https://127.0.0.1:18443/webtools/control/main
curl -sk -o /dev/null -w '%{http_code}\n' https://127.0.0.1:18444/webtools/control/main
```

Then run the browserless controls and the exact local Nuclei template:

```sh
python3 lab/probe.py https://127.0.0.1:18443 https://127.0.0.1:18444
python3 lab/scan.py
```

The Python probe uses `requests`. The Nuclei script uses `projectdiscovery/nuclei@sha256:582d5546902e67052097cb2d07296c642d50a1afc5e44623cb038845df9a32eb` (v3.11.1). Each scanner container shares only its target's network namespace so the request uses the loopback Host header accepted by OFBiz. It mounts `template/` read-only. Neither script creates accounts, writes files through OFBiz, executes commands on the target, or requires an external callback.

The expected Nuclei result is 3/3 findings on 24.09.07 and 0/3 on 24.09.08, with HTTP 200 and the renderer comment for the `file:`-loaded Web Tools decorator only on the vulnerable build. Probe controls use fresh sessions for GET, a component URI, unrelated JSON, form data, and query string. The component URI control switches to the Accounting decorator only on 24.09.07; the other controls retain the configured Web Tools decorator.

After saving evidence, stop these exact lab containers:

```sh
docker stop ig-ofbiz-68524-vuln ig-ofbiz-68524-fixed
```

The containers use `--rm`, so their ephemeral demo data is removed on stop. The pulled official images and this candidate directory remain for future reproduction. Do not remove unrelated Docker resources.
