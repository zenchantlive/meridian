# Layered Memory JSONL Schema

This schema defines one JSON object per line for layered memory storage.

## Required fields

- `id` (string): Stable entry identifier.
- `created_at` (string): ISO-8601 UTC timestamp.
- `scope` (string): One of `project_agent`, `project_global`, `user_agent`, `user_global`.
- `entry_type` (string): Logical category such as `fact`, `decision`, `preference`, or `note`.
- `content` (string): Memory payload text.
- `project_id` (string): Project namespace used to prevent cross-project leakage.

## Conditional field

- `agent_id` (string): Required when `scope` is `project_agent` or `user_agent`.

## Optional fields

- `tags` (array of strings), default `[]`
- `confidence` (number), default `0.7`
- `source` (string), default `"unknown"`
- `expires_at` (string or null), default `null`

## Validation behavior

- Invalid JSON lines are skipped.
- Records missing required fields are skipped.
- Records with unsupported scope are skipped.
- Agent-scoped records without `agent_id` are skipped.
- Each skipped entry produces a structured warning object with:
  - `code`
  - `message`
  - `path`
  - `line`
  - context keys such as `missing_fields`, `scope`, or `error`.
