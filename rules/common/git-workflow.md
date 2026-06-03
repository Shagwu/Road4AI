# Git Workflow Rules

## Before Commits

- Review `git status --short`.
- Do not stage unrelated user changes.
- Do not revert changes you did not make.
- Confirm protected files were not modified accidentally.
- If `state/current-queue.json` was changed, include dedup status in the commit message or Hermes checkpoint.

## Checkpoint Commits

After successful queue writes, commit a Hermes checkpoint with `[hermes-context]` describing:

- what changed;
- dedup result;
- approval status;
- any low-confidence assumptions.

## Security Review Before Commit

Check for:

- hardcoded secrets or bearer tokens;
- OAuth files or local credential paths;
- private account IDs not needed in source;
- copy-pasteable exploit payloads;
- unsafe shell snippets in public-facing docs;
- accidental edits to `AGENTS.md` without approval.

