# Approval Gates

Road4AI uses manual approval for actions that change public output or operating authority.

## Content Lifecycle

- `drafts/ideas/`: rough ideas and early drafts.
- `drafts/ready/`: drafted and ready for user review.
- `drafts/approved/`: user-approved content only.
- `drafts/archived/`: published or retired drafts.

Only the user moves content into `drafts/approved/`.

## Publishing

Once content is approved, Claude Code may schedule via Blotato without a second scheduling confirmation, subject to:

- dedup gate passed;
- public sanitization passed;
- platform constraints passed;
- published log and queue status will be updated after Blotato confirms scheduling. Platform-side verification is not required.

## Governance

Changes to operating contracts require explicit human approval in the active session. This includes:

- `AGENTS.md`;
- rules that weaken or bypass approval gates;
- agent specs that change who may publish, approve, or mutate shared state.

## Public-Facing Content Gate

Changes to public-facing surfaces (`index.html`, `SYSTEM.md`, `manifesto.md`, `CONTRIBUTING.md`, or any file served to external users) require a source citation check before merge.

**Rule:** Any claim containing a number, metric, benchmark score, or quantitative result must include a source file path in the commit message or PR description. Example: "0.788 live Ollama (execution/runs/2026-07-07-005/live-report.md)".

**Why this exists:** PR #2 merged without adversarial review on public-facing content. The landing page update (2026-07-10) included fabricated numbers (0.6447, +22%, 0.7504) that had no matching source file. A mechanical source-citation check would have caught this without relying on an LLM review gate.

**What this is not:** This is not a Karen gate. Karen reviews code diffs. This is a commit-message-level check that any human or agent can verify by grepping the cited source file. If the source file doesn't exist or doesn't contain the claimed number, the commit fails the gate.

**Enforcement:** Manual. The committing agent must include source citations for quantitative claims. The reviewing agent (or human) must verify the cited file exists and contains the claimed value before merge.

