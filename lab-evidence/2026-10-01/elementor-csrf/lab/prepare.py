#!/usr/bin/env python3
"""Fetch and verify official Elementor ZIPs for the disposable WordPress lab."""
from pathlib import Path
import hashlib
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVES = {
    '4.3.0': '3617ade04fc0b236756159399c56e4cc91c463daaedb3318b7cf5c7207cefa90',
    '4.3.2': '8b3eee68425e5fd90007dc84b37ffea844c0db44b6d342968f33c76187a94371',
}
for version, expected in ARCHIVES.items():
    role = 'vulnerable' if version == '4.3.0' else 'patched'
    archive = ROOT / f'elementor.{version}.zip'
    if not archive.exists():
        urllib.request.urlretrieve(f'https://downloads.wordpress.org/plugin/elementor.{version}.zip', archive)
    actual = hashlib.sha256(archive.read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f'Unexpected {version} ZIP hash: {actual}')
    destination = ROOT / f'elementor-{role}'
    destination.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            target = (destination / member.filename).resolve()
            if not target.is_relative_to(destination.resolve()):
                raise SystemExit(f'Unsafe archive member: {member.filename}')
        z.extractall(destination)
    print(f'Elementor {version}: SHA-256 verified and extracted')
