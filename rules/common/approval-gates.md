# Approval Gates

Road4AI uses manual approval for actions that change public output or operating authority.

## Content Lifecycle

- `drafts/ideas/`: rough ideas and early drafts.
- `drafts/ready/`: drafted and ready for user review.
- `drafts/approved/`: user-approved content only.
- `drafts/archived/`: published or retired drafts.

Only the user moves content into `drafts/approved/`.

## Publishing

Once content is approved, Gemini CLI may schedule via Blotato without a second scheduling confirmation, subject to:

- dedup gate passed;
- public sanitization passed;
- platform constraints passed;
- published log and queue status will be updated after successful scheduling or publishing.

## Governance

Changes to operating contracts require explicit human approval in the active session. This includes:

- `AGENTS.md`;
- rules that weaken or bypass approval gates;
- agent specs that change who may publish, approve, or mutate shared state.

