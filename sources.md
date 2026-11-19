# Source and artifact provenance

## Vulnerability and fix

| Source | Claim supported |
| --- | --- |
| [Apache advisory for CVE-2026-129448](https://lists.apache.org/thread/lnz4s26tv6hdo03wngtdbpfj4hg4gtds) | Versions 4.0.0 through 6.1.4 are affected; 6.1.5 is the same issue tracked as CVE-2026-82384; 6.1.6 disables vendor extensions and gates disabled XML-RPC; CVSS 3.1 score 9.8. |
| [Apache fix PR](https://github.com/apache/roller/pull/171) | `enabledForExtensions` changes to false, and a filter closes the endpoint when XML-RPC is disabled. The regression test uses a benign `ex:nil` value. |
| [CVE record](https://www.cve.org/CVERecord?id=CVE-2026-129448) / [CNA JSON](https://cveawg.mitre.org/api/cve/CVE-2026-129448) | CWE-502, CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H, score 9.8. The JSON copy is `lab/cve-2026-129448.json`. |
| [NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-129448) | Additional public CVE reference; the browser view was not readable during preparation, so no classification was inferred from it. |

## Official product releases used for final controls

Each binary archive was downloaded from the [Apache release archive](https://archive.apache.org/dist/roller/roller-6.1/), checked against its adjacent `.sha256` file, and its `webapp/roller.war` was extracted without modification.

| Version | Archive SHA-256 | WAR SHA-256 | Role |
| --- | --- | --- | --- |
| 6.1.4 | `a67cc9dd56456b4f78203a239cf4f0d4bb99634b74a230da3cd4d0d345f55823` | `c7d308db1b070149028ca0a7959407445763fd0fd54c206031f3747de8a9a5bd` | Affected product for CVE-2026-129448 |
| 6.1.5 | `c0f16e0792b9475dbde8e24fa4116ca10d6e0a8a82f71f06e9d3871637207ea8` | `55db754e52b71d15604a618c949e7b10453bd9a04d0081aefef7c3cc9d13e9a4` | Same issue under CVE-2026-82384 |
| 6.1.6 | `59e22302c60a36172a6f397b09cfb4fb339b54af61430b0f4cc99ed19c739525` | `da0e9ef2e82ac4c0a6e71c1eb31d3c99848ba5e516dab84fcee97f3e09f6d32d` | Fixed product |

The first exploration also built the 6.1.5 and 6.1.6 GitHub source tags (`395cfa30a7b274f8540424d11404c3e7433243f8` and `04a6f3c3d34946b709433ded6859afcda36640fd`) with Maven. Final controls use Apache's released binary WARs instead.

The local lab uses PostgreSQL JDBC 42.7.4 (`188976721ead8e8627eb6d8389d500dccc0c9bebd885268a3047180274a6031e`) and JavaMail 1.4.7 (`78c33b4f7c7b60f4b680f2d2405b1f063d71929cf1a4fbc328888379f365fcfb`) from Maven Central. Container images are pinned by digest in `lab/compose.yaml` and `lab/Dockerfile`.

## Nuclei contribution context

- Upstream base: `projectdiscovery/nuclei-templates` commit `745c8d83f2daa49b5525793229a358044a8bb3e7` (2026-11-19).
- Engine tested: Nuclei v3.11.0.
- The upstream main tree and open PR titles were searched for both CVEs and the Roller XML-RPC route on 2026-11-19; no duplicate was found.
- Current [contribution guide](https://github.com/projectdiscovery/nuclei-templates/blob/main/CONTRIBUTING.md) and [PR template](https://github.com/projectdiscovery/nuclei-templates/blob/main/PULL_REQUEST_TEMPLATE.md) were reviewed at the above upstream base.
