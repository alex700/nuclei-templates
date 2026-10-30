# Redacted Nuclei `-debug` excerpts

The excerpts for four product versions below come from Nuclei v3.11.1 with the exact template SHA-256 `46b137565a7a9715259d3627ed64f0b4be6db520efd601bc0f31aa63e100b801` against isolated local Drupal/Commerce sites. The command used `-debug -ni` and the pinned scanner image documented in `verification.md`. Only the final GET and its access-control GET are shown. Session cookies, response bodies, user data, and login POST data are omitted. The only retained response-body fragment is the issue-specific form ID.

## Commerce Core 3.3.12

Local raw debug SHA-256 (private, not published): `90be8e0996b43a1d3471f513bd527fc899176e3ee0b0199e5b6c90a5113de2b2`.

```http
[INF] [CVE-2026-118539] Dumped HTTP request for http://vulnerable/admin/commerce/config/orders
GET /admin/commerce/config/orders HTTP/1.1
Host: vulnerable
Cookie: [REDACTED]
[DBG] [CVE-2026-118539] Dumped HTTP response http://vulnerable/admin/commerce/config/orders
HTTP/1.1 403 Forbidden
[response body omitted]
```

```http
[INF] [CVE-2026-118539] Dumped HTTP request for http://vulnerable/admin/commerce/orders/1/state/place
GET /admin/commerce/orders/1/state/place HTTP/1.1
Host: vulnerable
Cookie: [REDACTED]
[DBG] [CVE-2026-118539] Dumped HTTP response http://vulnerable/admin/commerce/orders/1/state/place
HTTP/1.1 200 OK
... name="form_id" value="commerce_order_default_state-transition-confirm_form" ... [remaining HTML omitted]
```

## Commerce Core 3.3.13

Local raw debug SHA-256 (private, not published): `f5830ec877e6df08b28e3b2b2910219f63fbebcbcae00219d7457f553f0bb11c`.

```http
[INF] [CVE-2026-118539] Dumped HTTP request for http://patched/admin/commerce/config/orders
GET /admin/commerce/config/orders HTTP/1.1
Host: patched
Cookie: [REDACTED]
[DBG] [CVE-2026-118539] Dumped HTTP response http://patched/admin/commerce/config/orders
HTTP/1.1 403 Forbidden
[response body omitted]
```

```http
[INF] [CVE-2026-118539] Dumped HTTP request for http://patched/admin/commerce/orders/1/state/place
GET /admin/commerce/orders/1/state/place HTTP/1.1
Host: patched
Cookie: [REDACTED]
[DBG] [CVE-2026-118539] Dumped HTTP response http://patched/admin/commerce/orders/1/state/place
HTTP/1.1 403 Forbidden
[response body omitted]
```

## Commerce Core 2.40.0 (8.x-2.40)

Local raw debug SHA-256 (private, not published): `18decd5fe91d1b06a697a6795c03adfd059d1a0dbd029a3d20d47b7da0aa0110`.

```http
[INF] [CVE-2026-118539] Dumped HTTP request for http://legacy-vulnerable/admin/commerce/config/orders
GET /admin/commerce/config/orders HTTP/1.1
Host: legacy-vulnerable
Cookie: [REDACTED]
[DBG] [CVE-2026-118539] Dumped HTTP response http://legacy-vulnerable/admin/commerce/config/orders
HTTP/1.1 403 Forbidden
[response body omitted]
```

```http
[INF] [CVE-2026-118539] Dumped HTTP request for http://legacy-vulnerable/admin/commerce/orders/1/state/place
GET /admin/commerce/orders/1/state/place HTTP/1.1
Host: legacy-vulnerable
Cookie: [REDACTED]
[DBG] [CVE-2026-118539] Dumped HTTP response http://legacy-vulnerable/admin/commerce/orders/1/state/place
HTTP/1.1 200 OK
... name="form_id" value="commerce_order_default_state-transition-confirm_form" ... [remaining HTML omitted]
```

## Commerce Core 2.41.0 (8.x-2.41)

Local raw debug SHA-256 (private, not published): `86e5db0e619a601a31cb0b57bbe6bf54064a480ef217e069cb7defd1ce6cd93a`.

```http
[INF] [CVE-2026-118539] Dumped HTTP request for http://legacy-patched/admin/commerce/config/orders
GET /admin/commerce/config/orders HTTP/1.1
Host: legacy-patched
Cookie: [REDACTED]
[DBG] [CVE-2026-118539] Dumped HTTP response http://legacy-patched/admin/commerce/config/orders
HTTP/1.1 403 Forbidden
[response body omitted]
```

```http
[INF] [CVE-2026-118539] Dumped HTTP request for http://legacy-patched/admin/commerce/orders/1/state/place
GET /admin/commerce/orders/1/state/place HTTP/1.1
Host: legacy-patched
Cookie: [REDACTED]
[DBG] [CVE-2026-118539] Dumped HTTP response http://legacy-patched/admin/commerce/orders/1/state/place
HTTP/1.1 403 Forbidden
[response body omitted]
```

Redaction check: no `Set-Cookie` values, Drupal session identifiers, form build IDs, login credentials, customer profile data, or full HTML response bodies appear in this artifact. The original logs are retained only in a private local directory for audit and are not part of the contribution or evidence branch.
