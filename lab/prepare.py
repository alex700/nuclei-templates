#!/usr/bin/env python3
"""Fetch checksum-verified Apache Roller release WARs for the disposable lab."""

from hashlib import sha256
from pathlib import Path
import shutil
import subprocess
import tarfile


HERE = Path(__file__).resolve().parent
ARCHIVES = {
    "6.1.4": "a67cc9dd56456b4f78203a239cf4f0d4bb99634b74a230da3cd4d0d345f55823",
    "6.1.5": "c0f16e0792b9475dbde8e24fa4116ca10d6e0a8a82f71f06e9d3871637207ea8",
    "6.1.6": "59e22302c60a36172a6f397b09cfb4fb339b54af61430b0f4cc99ed19c739525",
}
JARS = {
    "postgresql.jar": (
        "https://repo.maven.apache.org/maven2/org/postgresql/postgresql/42.7.4/postgresql-42.7.4.jar",
        "188976721ead8e8627eb6d8389d500dccc0c9bebd885268a3047180274a6031e",
    ),
    "javax-mail.jar": (
        "https://repo.maven.apache.org/maven2/javax/mail/mail/1.4.7/mail-1.4.7.jar",
        "78c33b4f7c7b60f4b680f2d2405b1f063d71929cf1a4fbc328888379f365fcfb",
    ),
}


def digest(path):
    hasher = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def obtain(path, url, expected):
    if path.exists() and digest(path) == expected:
        return
    temp = path.with_name(path.name + ".download")
    subprocess.run(["curl", "--fail", "--location", "--silent", "--show-error",
                    "--retry", "2", "--output", str(temp), url], check=True)
    if digest(temp) != expected:
        temp.unlink(missing_ok=True)
        raise ValueError(f"Checksum mismatch for {path.name}")
    temp.replace(path)


def main():
    (HERE / "war").mkdir(exist_ok=True)
    for version, expected in ARCHIVES.items():
        filename = f"apache-roller-{version}-binary.tar.gz"
        archive = HERE / filename
        url = f"https://archive.apache.org/dist/roller/roller-6.1/v{version}/{filename}"
        obtain(archive, url, expected)
        war = HERE / "war" / (f"roller-{version}.war" if version == "6.1.4" else f"roller-{version}-official.war")
        with tarfile.open(archive, "r:gz") as bundle:
            with bundle.extractfile(f"apache-roller-{version}/webapp/roller.war") as source, war.open("wb") as sink:
                shutil.copyfileobj(source, sink)
        print(f"Verified Apache Roller {version} archive and extracted WAR")
    for filename, (url, expected) in JARS.items():
        obtain(HERE / filename, url, expected)
        print(f"Verified {filename}")


if __name__ == "__main__":
    main()
