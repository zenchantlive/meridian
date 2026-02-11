# Redaction And Data-Boundary Policy

This policy defines what can be written to layered memory and how leakage is prevented.

## Write boundaries

- Default: user-global layers are write-blocked.
- User-global writes require explicit opt-in: `allow_user_global_write: true`.
- Project-local layers remain the default write target.

## Redaction policy

- Redaction runs before writing sensitive content to global layers.
- Default sensitive keys include:
  - `api_key`
  - `token`
  - `password`
  - `secret`
  - `private_key`
- Matching values are replaced with `[REDACTED]`.

## Project boundary rule

- Every record must carry `project_id`.
- Visibility filter: records are visible only when `record.project_id == active_project_id`.
- This prevents unintended cross-project memory bleed, even if user-global layers are enabled.
