# Sources and product controls

- Upstream security fix: https://github.com/maximhq/bifrost/pull/6757
- Official MCP configuration documentation: https://github.com/maximhq/bifrost/blob/main/docs/mcp/connecting-to-servers.mdx
- Positive fixture: official `maximhq/bifrost:v2.0.0`, immutable arm64 image digest in `lab/compose.yaml`.
- Patched fixture: official `maximhq/bifrost:v2.1.0`, immutable arm64 image digest in `lab/compose.yaml`.
- Bifrost v2.0.0 launches `/bin/sh` from unauthenticated stdio registration before the MCP handshake. The command makes only a harmless HTTP callback. The process then fails the handshake with a 500 after about 30 seconds. A retry may cause two callbacks, each tied to the same Nuclei interaction ID. Version v2.1.0 returns 403 before starting the command.
