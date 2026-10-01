# Sources and product controls

- Disclosure: https://patchstack.com/articles/cross-site-request-forgery-in-elementor-plugin-affecting-2-million-sites/
- Official WordPress release archives: `https://downloads.wordpress.org/plugin/elementor.4.3.0.zip` and `https://downloads.wordpress.org/plugin/elementor.4.3.2.zip`. SHA-256 values are pinned in `lab/prepare.py`.
- WordPress 7.1.0 PHP 8.3 Apache and MariaDB 11.4 are pinned by immutable image digest in `lab/compose.yaml`.
- The REST authentication filter in 4.3.0 inspects the entire request URI for `elementor/v1/events/`. Version 4.3.2 tests the parsed route instead. The lab enables the Editor Events experiment explicitly and creates an administrator cookie for a local account.
