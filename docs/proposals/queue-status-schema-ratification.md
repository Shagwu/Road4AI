# Queue Status Schema Ratification & Stuck-Record Archival Proposal

**Status:** DRAFT — for human review, not yet applied
**Risk level:** HIGH (touches AGENTS.md-adjacent schema and shared state)
**Scope:** (1) ratify `scheduled` into the governing status enum, (2) add `archived` as a terminal status, (3) archive the 4 stuck records identified in the pre-commit health check, (4) add guardrails so stale scheduled records cannot silently reappear.

This proposal does not modify AGENTS.md, state/current-queue.json, or any validator until explicitly approved. It is split into two independently approvable decisions: a schema ratification (Sections 1–3) and a follow-on archival task (Section 4), so the risky policy change is not bundled with a bulk data edit.

## 1. Decision being ratified

`scheduled` is already de facto policy: CLAUDE.md, runtime skills, and live queue records all treat it as a real, active status. AGENTS.md's documented enum does not list it. This is a documentation/schema gap, not a behavior change: the goal is to make the governing document match reality, under explicit review rather than silent normalization.

**Proposed resolution:** adopt `scheduled` as a first-class status, and add `archived` as a terminal status for records intentionally closed out without publishing. `archived` is not a deletion state; it preserves audit history.

## 2. Current vs. proposed enum

| | Current (AGENTS.md) | Proposed |
|---|---|---|
| Documented statuses | Verify against live AGENTS.md before merge | `draft`, `ready`, `approved`, `scheduled`, `published`, `archived` |
| `scheduled` | Undocumented, but load-bearing in code and skills | Queued for publish; `draft_path` and target platform resolved; awaiting external publish confirmation |
| `archived` | Not present | Terminal, non-publishing state for retained records intentionally closed out for traceability |

**Transition rule:** `scheduled` may transition only to `published` or `archived`. No status transition may leave `archived`.

## 3. Files requiring update

On approval, update only the following schema-aligned files:

- `AGENTS.md` — document `scheduled` and `archived`; state that `archived` is terminal.
- `rules/common/content-dedup-gate.md` — exclude `archived` records from active duplicate checks.
- `skills/queue-inspect.md` or equivalent — exclude `archived` from active summaries by default.
- Relevant queue schema validator(s) — accept the ratified enum and reject undocumented statuses.

## 4. Follow-on: four stuck records

This section requires separate approval after the schema decision.

For each record currently marked `scheduled`:

1. Check `state/published-log.json` for a matching Blotato-confirmed publish record.
2. If confirmed, correct the record to `published`; do not archive it.
3. If no publish record exists and `draft_path` does not resolve, classify it as genuinely stuck.
4. For genuinely stuck records, set `status: archived`, retain the existing history and paths, and add:
   - `archived_reason`
   - `archived_at`
5. Do not delete records or rewrite their historical references.

Example:

```json
{
  "status": "archived",
  "archived_reason": "draft_path missing, no publish record — closed out during schema reconciliation",
  "archived_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

## 5. Guardrails

- **Read-only staleness check:** flag any `scheduled` record older than the approved threshold (proposed: 14 days) that has no matching published-log entry. It must surface records for human review; it must not auto-archive.
- **CI queue-shape test:** assert every queue record has a status contained in the ratified enum.

## 6. Rollout sequence

1. Verify the current enum wording directly in live `AGENTS.md`.
2. Approve the schema decision.
3. Update AGENTS.md, documentation, validators, and tests in a dedicated schema commit.
4. Classify the four stuck records individually in a separate, narrowly scoped state commit.
5. Add the staleness check and CI enforcement.

Nothing in this proposal is applied automatically. Each implementation step remains subject to explicit approval for shared-state and governance-adjacent changes.
