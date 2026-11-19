#!/usr/bin/env python3
"""Complete first-run setup for disposable Roller instances."""

import http.cookiejar
import os
import re
import secrets
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = os.environ.get("ROLLER_LAB_PROJECT", "roller-nuclei-lab")
COMPOSE = ["docker", "compose", "-p", PROJECT, "-f", str(HERE / "compose.yaml")]


def compose(*args):
    return subprocess.run(COMPOSE + list(args), check=True, capture_output=True, text=True).stdout


def port_for(service):
    return int(compose("port", service, "8080").strip().rsplit(":", 1)[1])


def fetch(client, url, data=None):
    encoded = urllib.parse.urlencode(data).encode() if data is not None else None
    try:
        with client.open(url, data=encoded, timeout=30) as response:
            return response.url, response.status, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        return error.url, error.code, error.read().decode("utf-8", "replace")


def salt_from(html):
    match = re.search(r'name="salt" value="([^"]*)"', html)
    return match.group(1) if match else ""


def bootstrap_token():
    log = compose("exec", "-T", "fixed", "cat", "/usr/local/tomcat/logs/roller.log")
    matches = re.findall(
        r"Enter this one-time setup token \(expires in 60 minutes\):[^\n]*\n\|\s*([A-Za-z0-9_-]{43})\s*\|",
        log,
    )
    if not matches:
        raise RuntimeError("Fixed version setup token not found in local log")
    return matches[-1]


def user_count(service):
    value = compose("exec", "-T", f"db-{service}", "psql", "-U", "roller", "-d", "rollerdb",
                    "-Atc", "select count(*) from roller_user;")
    return int(value.strip())


def initialize(service):
    base = f"http://127.0.0.1:{port_for(service)}"
    client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    url, status, html = fetch(client, base + "/roller-ui/install/install.rol")
    if service == "fixed" and "bootstrap-token" in url:
        url, status, html = fetch(client, base + "/roller-ui/bootstrap-token!redeem.rol",
                                  {"salt": salt_from(html), "token": bootstrap_token()})
        if status != 200 or "bootstrap-token" in url:
            raise RuntimeError("Fixed version rejected its setup token")
        print("fixed: setup token accepted")
    if "No database tables found" not in html:
        url, status, html = fetch(client, base + "/roller-ui/install/install.rol")
    if "No database tables found" in html:
        for attempt in range(2):
            url, status, html = fetch(client, base + "/roller-ui/install/install!create.rol",
                                      {"salt": salt_from(html)})
            if status == 200 and "Tables created successfully" in html:
                break
            if attempt == 0:
                _, _, html = fetch(client, base + "/roller-ui/install/install.rol")
        else:
            raise RuntimeError(f"{service}: database creation failed")
        print(f"{service}: database tables created")
    url, status, html = fetch(client, base + "/roller-ui/install/install!bootstrap.rol")
    if status != 200 or "An unknown error has occurred" in html:
        raise RuntimeError(f"{service}: bootstrap failed")
    url, status, html = fetch(client, base + "/roller-ui/register.rol")
    if status != 200:
        raise RuntimeError(f"{service}: registration page unavailable")
    if user_count(service) == 0:
        password = secrets.token_urlsafe(12)
        url, status, html = fetch(client, base + "/roller-ui/register!save.rol", {
            "salt": salt_from(html), "bean.userName": "rollerlab", "bean.screenName": "Roller Lab",
            "bean.fullName": "Roller Lab", "bean.emailAddress": "rollerlab@example.com",
            "bean.passwordText": password, "bean.passwordConfirm": password,
            "bean.locale": "en_US", "bean.timeZone": "UTC",
        })
        if status != 200 or user_count(service) != 1:
            raise RuntimeError(f"{service}: first-user registration failed")
        print(f"{service}: first lab user created")
    _, status, html = fetch(client, base + "/roller-ui/login.rol")
    if status != 200 or "/roller_j_security_check" not in html:
        raise RuntimeError(f"{service}: login page did not become ready")
    print(f"{service}: ready on local port {port_for(service)}")


if __name__ == "__main__":
    for service in ("affected", "vulnerable", "fixed"):
        initialize(service)
