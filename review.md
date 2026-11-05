# Independent template review: CVE-2026-68524

- Reviewer: `/root/ofbiz_template_review` (`nuclei-reviewer` profile)
- Reviewed template SHA-256: `c7fac613a76fb9f2f8a01db9adfa02223a93cfc564e3809afb43ded6353dd395`
- Verdict: **PASS for the scoped local template and reproduction package**. No blocking template finding remains. Upstream PR creation, CI, and maintainer acceptance were not assessed.

## Checks

- Inspected the exact template request, matcher, metadata, `verification.md`, `sources.md`, lab scripts, saved evidence, and the synchronized `publication/evidence-repo` copy. Corresponding package files and the template match byte-for-byte; the scan summary names the reviewed template SHA-256.
- Compared the detection claim with the [Apache security page](https://ofbiz.apache.org/security.html), [Apache fix #1654](https://github.com/apache/ofbiz-framework/pull/1654), and [Apache CNA record](https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2026/68xxx/CVE-2026-68524.json). The `high` severity is an explicit mapping from CNA `important`, CWE-94 is supported, and no CVSS vector is invented.
- Independently ran the unchanged template with pinned Nuclei v3.11.1 against local official OFBiz 24.09.07 and 24.09.08 containers: one finding on 24.09.07, zero on 24.09.08. Direct requests to both returned HTTP 200; the vulnerable response contained the exact `file:` renderer comment and the fixed response contained the configured `component://` renderer comment.
- Checked the saved repeated controls: 36 fresh-session requests across baseline, file-URI JSON, component-URI JSON, unrelated JSON, form override, and query override. Only the vulnerable file-URI JSON requests produced the file-URI renderer marker (3/3); all fixed controls retained the configured decorator. Six saved Nuclei runs loaded one template each, reached the targets with HTTP 200, and found 3/3 vulnerable and 0/3 fixed.
- The affected application log records `ScreenFactory` loading 11 screens from the injected local `file:` URI. This independently supports that the marker reflects resource loading rather than merely echoed input.

## Accepted limits

- The benign request loads the server's own installed Web Tools XML through a `file:` URI. It does not establish temporary-file descriptor access or execute code, so the result is a partial-chain CVE signal. The template and evidence state this limit.
- The `/proc/self/cwd` path assumes Linux and a conventional OFBiz working directory. Stripped renderer comments or custom layouts can yield false negatives. The `linux` tag and verification report disclose these prerequisites.
- Only official demo images of 24.09.07 and 24.09.08 were product-tested. No public or third-party target was scanned.

No source or template files were edited by the reviewer. The prior review blockers (unsupported critical severity, missing CWE/reference, and component-only probe) were corrected and the final package was retested.
