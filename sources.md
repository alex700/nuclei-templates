# Source provenance

- Apache OFBiz security page, reviewed 2026-11-05: https://ofbiz.apache.org/security.html. It maps CVE-2026-68524 to fixes #1528 and #1654 and says releases before 24.09.08 are affected.
- Apache OFBiz maintainer advisory, reviewed 2026-11-05: https://www.openwall.com/lists/oss-security/2026/11/04/9. It calls the issue pre-authentication remote code execution via attacker-controlled screen definition loading.
- Apache CNA CVE record: https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2026/68xxx/CVE-2026-68524.json. It describes temporary-file and open-descriptor access followed by an injected `file:` URI, classifies the issue as CWE-94, and gives textual severity `important` without a CVSS vector. The Nuclei `high` severity is an alignment with `important`, not a published CVSS score.
- NVD record: https://nvd.nist.gov/vuln/detail/CVE-2026-68524. Referenced for identifier completeness; no CVSS value was copied from it.
- Apache fix #1528: https://github.com/apache/ofbiz-framework/pull/1528. It blocked the `proc/self/fd` screen path as an initial hardening step.
- Apache fix #1654: https://github.com/apache/ofbiz-framework/pull/1654. It prevents anonymous JSON request-body attributes from shadowing ServletContext attributes and tightens widget resource location handling.
- Affected official image: `ghcr.io/apache/ofbiz@sha256:b6151682feab85b5d9b834254945b821a9fc02e0327cbad0e1f5f35628934a58`, tag `24.09.07-preloaddemo`. Response footer: release 24.09.07, revision `42819e5ae1d5339d3a204ac06b43e69d46a9c0ae`.
- Fixed official image: `ghcr.io/apache/ofbiz@sha256:5718c99aec3470d3156cdccade1b2a48af3737b57c5a4c7da3934e4f32a5865a`, tag `24.09.08-preloaddemo`. Response footer: release 24.09.08, revision `a12cafc095b78fbba7978d26c6ad33dc0ce6cfae`.
- Nuclei image: `projectdiscovery/nuclei@sha256:582d5546902e67052097cb2d07296c642d50a1afc5e44623cb038845df9a32eb`, v3.11.1.
- Analog OFBiz template `CVE-2024-45507`: https://github.com/projectdiscovery/nuclei-templates/blob/main/http/cves/2024/CVE-2024-45507.yaml. It uses a request-controlled decorator and a DNS callback from a command-bearing XML screen. It is more invasive and not needed for this detector.
- Analog OFBiz template `CVE-2023-50968`: https://github.com/projectdiscovery/nuclei-templates/blob/main/http/cves/2023/CVE-2023-50968.yaml. It confirms SSRF through an HTTP Interactsh callback. This CVE has a direct response-side proof, so no callback is needed.
- Analog OFBiz template `CVE-2024-45195`: https://github.com/projectdiscovery/nuclei-templates/blob/main/http/cves/2024/CVE-2024-45195.yaml. It writes and fetches a server-side file, making it unsuitable as a safety model for mass scanning here.
- Upstream search on 2026-11-05: exact CVE code and PR searches of `projectdiscovery/nuclei-templates` returned no results. This is scoped to the identifier and does not prove no related logic exists under another name.

No CVSS vector is asserted because the Apache CNA record provides none. The template proves loading of a built-in screen through an attacker-supplied `file:` URI; it does not prove the temporary-file descriptor or code execution legs of the complete exploit chain.
