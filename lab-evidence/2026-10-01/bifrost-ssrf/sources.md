# Sources

- https://github.com/maximhq/bifrost/security/advisories/GHSA-2qp8-4xgm-fw6g — primary advisory: default auth disabled, POST /api/plugins remote path fetch, static Docker image only proves SSRF, dynamic plugin RCE conditional.
- https://github.com/maximhq/bifrost/blob/transports/v1.6.2/transports/bifrost-http/handlers/plugins.go — vulnerable handler persists a custom path, reloads plugin, and rolls back a failed load; `CreatePluginRequest` fields confirmed.
- https://github.com/maximhq/bifrost/blob/transports/v2.1.0/transports/bifrost-http/handlers/plugins.go — fixed handler checks `BifrostContextKeyAuthBypassed` and rejects custom paths with 403 before DB write.
- Official Docker images: `maximhq/bifrost:v1.6.2` sha256:c4de3a1d6bd2f9b8b0b8f508deaaf0337a793603d2b84b61138cdb35f94a4318, `maximhq/bifrost:v2.1.0` sha256:653b74a8410e5757375aa9a25ce21f90f4591fc11d65879451939b6172ce80ed; native arm64 image manifests inspected 2026-10-01.
- Official upstream nuclei-templates `8b9d065ccb0492d39f7680c908b3030a97ddfe1b`; no equivalent Bifrost template or active PR found in identifier/alias searches 2026-10-01.
