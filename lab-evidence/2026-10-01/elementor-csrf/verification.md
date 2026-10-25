# Elementor REST nonce bypass: login revision

## Scope and prerequisite

The template detects the Elementor 4.3.0-4.3.1 Editor Events REST nonce
bypass for a WordPress administrator account. It now takes authorized
`username` and `password` variables and logs in through standard
`/wp-login.php`. An HTTP 302 plus a `Set-Cookie: wordpress_logged_in_...` header is required.
The cookie is extracted internally and sent with the denied baseline,
denied near-miss, and exact-marker requests. The login redirect is not followed.
The scan does not claim anonymous access. SSO, MFA, and custom login paths
are outside the validated setup. The Editor Events experiment must be active.

## Fresh product validation

Nuclei v3.11.0 ran against official Elementor 4.3.0 and 4.3.2 in disposable
WordPress 7.1.0 / MariaDB 11.4 containers on native arm64. The exact updated
template SHA-256 is `950893ddb545ea29a4cb6b3f3d5bcb9ee56b035cd21104a06d750d4a61da659f`.
The saved run is `evidence/4206f0a72fca/`.

| Control | Login and application evidence | Findings |
| --- | --- | ---: |
| Elementor 4.3.0, valid admin credentials | Login 302; baseline 401; near miss 401; exact marker 200 with settings JSON | 1 |
| Elementor 4.3.2, valid admin credentials | Login 302; exact marker 401 | 0 |
| Elementor 4.3.0, wrong password | Login 200; no differential probe followed | 0 |

The runner asserted template ID and counts, Nuclei schema validation passed,
and the exact Compose project was removed. Application logs show the expected
requests and healthy responses. Saved command logs redact the lab password
and session cookie. The template performs one WordPress login and three
read-only GET requests; no WordPress state change is part of the probe.

Reproduce with `python3 tests/verify.py /absolute/path/to/this/package`
after `python3 lab/prepare.py`, using Docker Compose v2 and Python 3.
The official Elementor ZIPs are pinned and hash-checked by `prepare.py`.

## Earlier evidence

`evidence/5c6ec6fe1fe1/` (if present) belongs to the original template
that accepted a caller-supplied cookie. It does not validate the updated
login flow. The new run above supersedes it for this PR revision.
