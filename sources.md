# Sources and provenance

- [Vates VSA-2026-062](https://docs.vates.tech/security-advisories/advisories/2026/vates-sa-2026-062/), published and updated 2026-11-10: vulnerability mechanism, critical severity, affected XO versions, fixed versions, and active exploitation warning. The advisory does not assign a CVE or CVSS score at the time of this preparation.
- [Vendor fix PR 10748](https://github.com/vatesfr/xen-orchestra/pull/10748), merged commit `50166fe3a49c02069d35ba9046ca4a1f77f4e11d`: token-ID type validation. Direct parent `724402733b2381d93372db0183e21df9d2c457f7` is the affected source control used in the lab.
- [Official source installation guide](https://github.com/vatesfr/xen-orchestra/blob/master/docs/docs/getting-started/install-from-sources.md): source build prerequisites and runtime dependencies. The repository is AGPL-3.0-or-later; this package links to the source rather than redistributing a build.
- [ProjectDiscovery nuclei-templates](https://github.com/projectdiscovery/nuclei-templates): contribution conventions and the current PR form. The contribution base was `0d4157cc395` from `upstream/main` on 2026-11-11. The repository had no VSA-2026-062 template or issue at preparation time; its only Xen Orchestra file was an exposed-panel detector.

No third-party exploit code or private target material was used.
