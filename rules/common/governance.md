# Road4AI Governance Rules

These rules apply to all agents working in this repository.

## Operating Contract

- `AGENTS.md` is the primary operating contract.
- Governance changes require explicit human approval in the current session.
- Agents must not silently rewrite, weaken, or negotiate their own rules.
- If a requested action conflicts with `AGENTS.md`, stop and surface the conflict.

## Autonomy Levels

### DO

- Read the required coordination files at session start.
- Run the queue audit before content work.
- Draft, edit, validate, and organize content within the current lifecycle folders.
- Create supporting governance files after explicit approval.
- Use existing project patterns before inventing new structures.

### ASK

- Before changing `AGENTS.md`, publishing content, deploying code, or modifying credentials.
- Before resolving a dedup conflict.
- Before replacing a human approval gate with automation.

### NEVER

- Modify `AGENTS.md` without explicit per-session human approval.
- Move content into `drafts/approved/` on behalf of the user.
- Publish or schedule content before the approval gate is satisfied.
- Delete queue items silently.
- Include live secrets, tokens, private account IDs, or copy-pasteable exploit payloads in public drafts.

## Enforcement Preference

Rules and hooks are preferred over prompt-only reminders for critical checks. If a gate protects publishing, queue mutation, security, or governance, encode it in a deterministic checklist, script, or hook wherever practical.

