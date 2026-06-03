# CLI-Native Guidelines

Road4AI tools should remain useful from the command line.

## Design

- Prefer explicit commands with clear inputs and outputs.
- Support dry-run behavior for state mutation where practical.
- Print actionable errors.
- Keep machine-readable output available for gates and tests.

## Avoid

- Hidden network calls in validation commands.
- Commands that silently mutate queue state.
- Tooling that only works through one agent harness.

