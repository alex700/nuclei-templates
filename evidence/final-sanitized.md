# Sanitized two-branch validation evidence

Date: 2026-10-30. All targets were isolated local Drupal/Commerce installations. No external target was scanned.

## Working Installation

- Template SHA-256: `46b137565a7a9715259d3627ed64f0b4be6db520efd601bc0f31aa63e100b801`.
- Runner assertions: passed; Compose project cleanup: passed.
- Scanner: pinned Nuclei v3.11.1 image; template mounted read-only.

| Scenario | Findings | Administration control | State-transition GET |
| --- | ---: | ---: | ---: |
| vulnerable_customer | 1 | 403 | 200 |
| patched_customer | 0 | 403 | 403 |
| legacy_vulnerable_customer | 1 | 403 | 200 |
| legacy_patched_customer | 0 | 403 | 403 |

The vulnerable responses contain `commerce_order_default_state-transition-confirm_form`; the patched responses return access denied. The final request is GET only.

Additional negative controls:
- `wrong_password`: 0 findings.
- `missing_order`: 0 findings.
- `admin_account`: 0 findings.
- `legacy_vulnerable_missing_order`: 0 findings.
- `legacy_patched_missing_order`: 0 findings.
- `legacy_wrong_password`: 0 findings.
- `legacy_admin_account`: 0 findings.

## Clean Pinned Recreation

- Template SHA-256: `46b137565a7a9715259d3627ed64f0b4be6db520efd601bc0f31aa63e100b801`.
- Runner assertions: passed; Compose project cleanup: passed.
- Scanner: pinned Nuclei v3.11.1 image; template mounted read-only.

| Scenario | Findings | Administration control | State-transition GET |
| --- | ---: | ---: | ---: |
| vulnerable_customer | 1 | 403 | 200 |
| patched_customer | 0 | 403 | 403 |
| legacy_vulnerable_customer | 1 | 403 | 200 |
| legacy_patched_customer | 0 | 403 | 403 |

The vulnerable responses contain `commerce_order_default_state-transition-confirm_form`; the patched responses return access denied. The final request is GET only.

Additional negative controls:
- `wrong_password`: 0 findings.
- `missing_order`: 0 findings.
- `admin_account`: 0 findings.
- `legacy_vulnerable_missing_order`: 0 findings.
- `legacy_patched_missing_order`: 0 findings.
- `legacy_wrong_password`: 0 findings.
- `legacy_admin_account`: 0 findings.

Raw Nuclei debug output and application logs were used to verify these observations but are excluded from this reviewer artifact because they can contain lab-only session material. The four Composer locks and fixture source are included in the reproduction package.
