# Apache OFBiz CVE-2026-68524 detector reproduction

This branch contains a local reproduction package for a benign Nuclei detector of anonymous `file:` screen loading. It uses official Apache OFBiz 24.09.07 and 24.09.08 demo images. The detector selects OFBiz's own installed Web Tools screen through a local file URI and observes the renderer comment. It does not execute commands, read arbitrary files, write target files, or use a callback service.

Run the exact commands in [lab/README.md](lab/README.md). [verification.md](verification.md) states the scope, results, and limitations; [sources.md](sources.md) records primary source provenance. The JSON summaries and selected debug excerpts in `evidence/local-2026-11-05/` are sanitized to exclude cookies and session IDs.

The Nuclei contribution itself is the single file in `template/template.yaml`. This branch is supporting evidence, not an upstream template PR.
