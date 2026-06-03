# Hermes Python Coding Style

These rules apply to Road4AI Python code, especially Hermes and COS tooling.

## Baseline

- Target Python 3.10+ unless a nested project specifies otherwise.
- Prefer typed functions for public interfaces and shared utilities.
- Keep IO, parsing, and business rules separated where practical.
- Use deterministic scripts for gates that protect publishing, security, or queue mutation.

## Error Handling

- Fail loudly for invalid queue shape, invalid status transitions, and missing required fields.
- Surface human-review cases explicitly with `[HUMAN_REVIEW_REQUIRED]`.
- Do not hide repeated failures behind retries.

## Tests

- Add focused tests for queue mutation, sanitizer behavior, and agent workflow gates.
- Prefer small fixtures over large exported workspace data.

