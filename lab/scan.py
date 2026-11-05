#!/usr/bin/env python3
"""Run the exact candidate template on the two official OFBiz images."""

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
template = root / "template" / "template.yaml"
evidence = root / "evidence" / "local-2026-11-05"
evidence.mkdir(parents=True, exist_ok=True)
image = "projectdiscovery/nuclei@sha256:582d5546902e67052097cb2d07296c642d50a1afc5e44623cb038845df9a32eb"
targets = {"vulnerable_24_09_07": "ig-ofbiz-68524-vuln",
           "fixed_24_09_08": "ig-ofbiz-68524-fixed"}
results = []
for target, container in targets.items():
    for repeat in range(3):
        base = ["docker", "run", "--rm", "--network", f"container:{container}",
                "-v", f"{template.parent}:/templates:ro", image]
        common = ["-u", "https://127.0.0.1:8443", "-t", "/templates/template.yaml", "-duc", "-ni", "-no-color"]
        finding_proc = subprocess.run(base + common + ["-silent"], text=True, capture_output=True, timeout=90)
        proc = subprocess.run(base + common + ["-debug"], text=True, capture_output=True, timeout=90)
        output = proc.stdout + proc.stderr
        redacted = re.sub(r"(?im)^(Set-Cookie|Cookie):.*$", r"\1: [REDACTED]", output)
        (evidence / f"nuclei-{target}-{repeat + 1}.log").write_text(redacted)
        finding = "[CVE-2026-68524] [http] [high]" in finding_proc.stdout
        loaded = "Templates loaded for current scan: 1" in output
        reached = "Dumped HTTP response" in output and "HTTP/1.1 200" in output
        file_screen = "Begin section widgetfile:/proc/self/cwd/framework/webtools/widget/CommonScreens.xml#main-decorator" in output
        webtools = "Begin section widgetcomponent://webtools/widget/CommonScreens.xml#main-decorator" in output
        result = {"target": target, "repeat": repeat + 1, "exitCode": proc.returncode,
                  "findingExitCode": finding_proc.returncode,
                  "finding": finding, "templateLoaded": loaded, "targetReachedWith200": reached,
                  "fileScreenSectionInResponse": file_screen, "webtoolsDecoratorInResponse": webtools,
                  "log": f"nuclei-{target}-{repeat + 1}.log"}
        results.append(result)
        print(json.dumps(result))
        assert proc.returncode == 0 and finding_proc.returncode == 0 and loaded and reached, result
        expected = target == "vulnerable_24_09_07"
        assert finding == expected and file_screen == expected and webtools != expected, result

report = {"at": datetime.now(timezone.utc).isoformat(), "nucleiImage": image,
          "templateSha256": hashlib.sha256(template.read_bytes()).hexdigest(),
          "results": results, "conclusion": "3/3 vulnerable findings, 0/3 fixed findings; all requests reached OFBiz and templates loaded"}
(evidence / "nuclei-scans.json").write_text(json.dumps(report, indent=2) + "\n")
