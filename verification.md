# CVE-2026-68524 local verification

Status: passed for the stated benign file-URI HTTP detector on actual OFBiz 24.09.07 and 24.09.08. No code execution was attempted or claimed. Exact tested template SHA-256: `c7fac613a76fb9f2f8a01db9adfa02223a93cfc564e3809afb43ded6353dd395`.

## Feasibility gate

1. **Observation:** POST JSON to the unauthenticated `/webtools/control/main` route supplies a `file:` URI for Web Tools' own installed screen as `mainDecoratorLocation`. On the affected build, the response's renderer comment shows `file:/proc/self/cwd/framework/webtools/widget/CommonScreens.xml#main-decorator`; on the fixed build it shows the configured `component://webtools/widget/CommonScreens.xml#main-decorator`. This exercises both anonymous attribute shadowing and local file-URI screen loading addressed by Apache fix #1654, without an exploit payload.
2. **Artifacts:** Both official preloaded demo images are available by immutable digest; their response footers identify 24.09.07 and 24.09.08 and their source revisions. No license or private data is required.
3. **Execution:** Both images are AMD64 and ran under Docker Desktop emulation on an ARM64 host. The issue is request attribute handling and widget resource selection, without timing, hardware, or native-memory dependencies.
4. **Isolation:** Targets were bound only to `127.0.0.1` and allocated 3 GiB each. The probe selects an existing built-in Web Tools screen and has no persistent application-side effect. No exploit payload, sensitive file, command, or external callback was used.
5. **Prerequisites:** The official demo images contain Web Tools. The scanner needs no account, prepared session, target-specific ID, Accounting component, or callback.
6. **Evidence:** Three fresh-session repetitions of six request types against each version, plus three Nuclei runs per version. The response must be HTTP 200 and contain exact renderer comments for the Web Tools main screen and the `file:`-loaded Web Tools decorator. The fixed build logs explicitly say it ignored a request body attribute shadowing `mainDecoratorLocation`.
7. **Mass-scan fit:** One unauthenticated JSON request is sufficient on default official Linux builds. A deployment with a different process working directory, without `/proc`, or with stripped renderer comments may yield a false negative; this limitation needs upstream review.

## Observed matrix

| Target | Baseline GET | File-URI JSON | Component JSON control | Unrelated JSON | Form override | Query override | Nuclei findings |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OFBiz 24.09.07 | Web Tools 3/3 | File-URI Web Tools 3/3 | Accounting 3/3 | Web Tools 3/3 | Web Tools 3/3 | Web Tools 3/3 | 3/3 |
| OFBiz 24.09.08 | Web Tools 3/3 | Web Tools 3/3 | Web Tools 3/3 | Web Tools 3/3 | Web Tools 3/3 | Web Tools 3/3 | 0/3 |

All 36 direct probes returned HTTP 200. All six Nuclei runs loaded exactly one template and received HTTP 200. Scanner v3.11.1 schema validation passed. The affected response shows the file-URI Web Tools screen; the fixed application log shows the shadowing rejection. See `evidence/local-2026-11-05/probes.json`, `nuclei-scans.json`, the redacted scanner logs, and selected application logs.

The first Nuclei attempt on a Docker bridge alias returned OFBiz's generic host-header rejection page. The lab scanner then used the target container's network namespace and an accepted `127.0.0.1` Host header. This is a lab routing detail, not a template matcher condition.

## Limitations and next step

- The detector confirms unsafe anonymous `file:` screen loading. It does not create or access a temporary file descriptor and does not execute or prove remote code execution.
- Only official demo configurations for 24.09.07 and 24.09.08 were product-tested. Older versions, Windows, nonstandard process working directories, custom themes, proxies that alter the JSON body, and disabled renderer comments were not tested.
- The current template is a local candidate. Independent template review and validation passed for the exact tested bytes. A focused local contribution branch and sanitized reviewer-reproduction package are prepared. The branches have not been pushed and no upstream PR exists. Recheck live upstream coverage and CI at submission time.

## Lab resource lifecycle

The two named lab containers were stopped after evidence capture. They were started with `--rm`, so their ephemeral demo data was removed. The temporary Docker network was removed. The pinned images and local reproduction files remain for repeat testing.
