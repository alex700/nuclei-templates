#!/usr/bin/env python3
"""Rebuild and check VSA-2026-062 against the actual XO source revisions.

Prerequisite: lab/source is a clone of vatesfr/xen-orchestra with Yarn
dependencies installed as documented in ../README.md. No token is persisted.
"""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "lab" / "source"
COMPOSE = ROOT / "lab" / "compose.yaml"
TEMPLATE = ROOT / "template.yaml"
PROJECT = "xo-vsa062-verify"
NUCLEI_IMAGE = "projectdiscovery/nuclei@sha256:582d5546902e67052097cb2d07296c642d50a1afc5e44623cb038845df9a32eb"
NODE_IMAGE = "node:24.22.1-bookworm@sha256:0925478b811e8890f5508ad2a75135933310effd45492696ecf7c111c8339d02"
REVISIONS = (
    ("affected", "724402733b2381d93372db0183e21df9d2c457f7", 1, 307),
    ("fixed", "50166fe3a49c02069d35ba9046ca4a1f77f4e11d", 0, 401),
)

PROBE_JS = r"""
(async()=>{
  const url='http://127.0.0.1:8080/rest/v0/users/me';
  const request=async(headers)=>{
    const r=await fetch(url,{headers,redirect:'manual'});
    return {status:r.status,locationIsUser:/^\/rest\/v0\/users\/[0-9a-f-]{36}$/.test(r.headers.get('location')||'')};
  };
  const before=await request({cookie:'authenticationToken=j:%7B%7D'});
  const created=await fetch(url+'/authentication_tokens',{
    method:'POST',
    headers:{authorization:'Basic '+Buffer.from('admin@admin.net:admin').toString('base64')}
  });
  const data=await created.json();
  if(created.status!==201 || !data.token?.id) throw Error('lab token creation failed');
  const results={
    before_token:before,
    token_created:created.status,
    anonymous:await request({}),
    malformed:await request({cookie:'authenticationToken=invalid'}),
    object_cookie:await request({cookie:'authenticationToken=j:%7B%7D'}),
    valid_token:await request({cookie:'authenticationToken='+encodeURIComponent(data.token.id)})
  };
  process.stdout.write(JSON.stringify(results)+'\n');
})().catch(e=>{process.stderr.write(e.message+'\n');process.exit(1)});
"""


def run(args, *, cwd=ROOT, capture=True, timeout=900):
    result = subprocess.run(
        args, cwd=cwd, text=True, capture_output=capture, timeout=timeout, check=False
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {args[:5]}\n{result.stderr[-1500:]}")
    return result.stdout


def compose(*args):
    return run(["docker", "compose", "-p", PROJECT, "-f", str(COMPOSE), *args])


def main():
    if not (SOURCE / ".git").exists() or not (SOURCE / "node_modules").exists():
        raise RuntimeError("Prepare lab/source and install dependencies as in README.md")
    os.environ["LAB_UID"] = str(os.getuid())
    os.environ["LAB_GID"] = str(os.getgid())
    evidence = ROOT / "evidence" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    evidence.mkdir(parents=True, exist_ok=False)
    os.chmod(evidence, 0o700)
    report = {
        "template_sha256": hashlib.sha256(TEMPLATE.read_bytes()).hexdigest(),
        "architecture": "linux/amd64 application on ARM64 Docker host",
        "scanner_image": NUCLEI_IMAGE,
        "tests": [],
    }
    try:
        for label, revision, expected_matches, expected_cookie_status in REVISIONS:
            compose("down")
            run(["git", "checkout", "--detach", revision], cwd=SOURCE)
            actual = run(["git", "rev-parse", "HEAD"], cwd=SOURCE).strip()
            if actual != revision:
                raise RuntimeError("wrong target revision")
            build = run([
                "docker", "run", "--rm", "--platform", "linux/amd64",
                "--cpus=4", "--memory=8g", "--user", f"{os.getuid()}:{os.getgid()}",
                "--mount", f"type=bind,src={SOURCE},dst=/work",
                "--workdir", "/work", "--env", "YARN_CACHE_FOLDER=/work/.yarn-cache",
                NODE_IMAGE, "yarn", "turbo", "run", "build", "--filter=xo-server", "--concurrency=4"
            ])
            (evidence / f"{label}-build.txt").write_text(build)
            compose("up", "-d", "--wait", "--force-recreate")
            probe = json.loads(compose("exec", "-T", "xo", "node", "-e", PROBE_JS))
            if probe["before_token"]["status"] != 401:
                raise AssertionError(f"{label}: no-token control failed")
            if probe["token_created"] != 201:
                raise AssertionError(f"{label}: token setup failed")
            if probe["anonymous"]["status"] != 401 or probe["malformed"]["status"] != 401:
                raise AssertionError(f"{label}: anonymous controls failed")
            if probe["object_cookie"]["status"] != expected_cookie_status:
                raise AssertionError(f"{label}: object cookie unexpected status")
            if probe["valid_token"]["status"] != 307 or not probe["valid_token"]["locationIsUser"]:
                raise AssertionError(f"{label}: valid-token route control failed")
            network = PROJECT + "_lab"
            raw = run([
                "docker", "run", "--rm", "--network", network,
                "--mount", f"type=bind,src={TEMPLATE},dst=/templates/template.yaml,readonly",
                NUCLEI_IMAGE, "-u", "http://xo:8080", "-t", "/templates/template.yaml",
                "-jsonl", "-duc", "-no-color", "-silent"
            ])
            raw_path = evidence / f"{label}-nuclei-private.jsonl"
            raw_path.write_text(raw)
            os.chmod(raw_path, 0o600)
            findings = [json.loads(line) for line in raw.splitlines() if line.strip()]
            ids = [item.get("template-id") for item in findings]
            if len(findings) != expected_matches or any(x != "vates-sa-2026-062" for x in ids):
                raise AssertionError(f"{label}: unexpected findings {ids}")
            summary = {"label": label, "revision": revision, "probe": probe,
                       "matches": len(findings), "template_ids": ids}
            report["tests"].append(summary)
            (evidence / f"{label}-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
        report["status"] = "passed"
    except Exception as exc:
        report["status"] = "failed"
        report["error"] = str(exc)
        raise
    finally:
        try:
            compose("down")
            report["cleanup"] = "Compose project removed"
        except Exception as exc:
            report["cleanup"] = f"Failed: {exc}"
        (evidence / "report.json").write_text(json.dumps(report, indent=2) + "\n")
        print(evidence / "report.json")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        sys.exit(1)
