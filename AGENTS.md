# Road4AI Agent Operating Contract

This is the constitution for all agents working in this repo. Every session reads this first.

## Session Start

1. Read this file (`AGENTS.md`).
2. Read `state/current-queue.json`.
3. Read `docs/brand-voice.md`.
4. Run `git log --grep="CHECKPOINT:" --format="%B" -3` and parse `[hermes-context]` blocks to understand current state.
5. For governance or content sessions, also read `WORKING-CONTEXT.md` and relevant `rules/` files.

## Autonomy Levels

**DO** (no approval needed):
- Read coordination files before work begins.
- Run the queue audit at the start of content sessions.
- Draft, edit, validate, and organize content within lifecycle folders.
- Use deterministic checks for dedup, sanitization, and platform constraints.
- Preserve existing shape of shared state files unless the user approves a migration.

**ASK** (get explicit human approval first):
- Before editing `AGENTS.md`, changing approval gates, publishing content, deploying code, or modifying credentials.
- Before resolving or bypassing a dedup conflict.
- Before moving content into a new lifecycle stage when ownership is unclear.

**NEVER** (hard stop):
- Modify `AGENTS.md` without explicit per-session human approval.
- Move content into `drafts/approved/` on behalf of the user.
- Publish, schedule, or mark content as approved before the approval gate is satisfied.
- Delete queue entries silently.
- Include secrets, private data, or copy-pasteable exploit payloads in public content.
- Use `git add -A` or `git add .`. Stage files explicitly by name.
- Push unless `HERMES_PUSH=true` is explicitly set.

## Agent Roles

### Codex (Planner & Drafter)
- Strategy, planning, content drafting, reasoning.
- Propose content ideas to `state/current-queue.json`.
- Create drafts in `drafts/ideas/`, move finalized to `drafts/ready/`.

### Claude Code (Operator & Publisher)
- Execution, tool integration (Blotato), publishing.
- Session start: parse `CHECKPOINT` git log for handoff state.
- Read `drafts/approved/`, schedule via Blotato, archive immediately after scheduling confirmation.
- Update `state/published-log.json` with live URLs.

### Content Scout
- Knowledge extraction from transcripts, articles, videos.
- Produces 9-section extraction, generates `INBOX.MD` append block.

### Signal Harvester [L8 Autonomy]
- Autonomous web reading (Twitter, Reddit, GitHub, YouTube, RSS). Read-only. Never store credentials, never scrape without 2s delay.

## Shared State Architecture

| File | Purpose |
|------|---------|
| `state/current-queue.json` | Active content pipeline queue (top-level `queue` array) |
| `state/published-log.json` | Record of everything already posted |
| `drafts/` | Lifecycle folders: `ideas/` → `ready/` → `approved/` → `archived/` |
| `WORKING-CONTEXT.md` | Current sprint, constraints, backlog |
| `rules/` | Governance and enforcement rules |
| `skills/` | Canonical reusable workflows (Option B: source → runtime install) |
| `project.yaml` | Project identity, runtime config, protected files |
| `state.yaml` | Workflow phase, task assignments |

## Coordination Protocol

1. **Deduplication**: Before drafting, check `state/published-log.json` and `state/current-queue.json`.
2. **Monday Ritual**: Every Monday, CoS parses `inbox.md` for top 5 content moments, maps to types (Struggle/Win/Tutorial/BTS), updates queue.
3. **Approval**: Only the user moves files from `ready/` to `approved/`.
4. **Approved Folder Hygiene**: Once approved content is scheduled in Blotato, move to `drafts/archived/` immediately. Never leave scheduled content in `approved/`.
5. **Traceability**: Every scheduled post needs a queue entry; every published post needs a published-log entry.
6. **Governance Lock**: Any mutation to `AGENTS.md` MUST be reviewed and approved by the human conductor. No agent-to-agent negotiation of operating contracts.
7. **Write Gate**: Agents may read `AGENTS.md` but must not write to it as part of normal task execution.
8. **Public Sanitization**: Drafts discussing security, prompt injection, autonomy failures, or customer examples must pass public sanitization review before approval.
9. **Security Before Commit**: Check for hardcoded secrets, bearer tokens, OAuth files, private local paths, copy-pasteable exploit payloads, and accidental protected-file edits.
10. **Queue Shape Preservation**: `state/current-queue.json` uses a top-level `queue` array. Preserve this shape unless the user explicitly approves a schema migration.

## Content Queue Schema

The queue lives in `state/current-queue.json` as an array of objects. Required fields:

- `id` (string): unique identifier, e.g. `"2026-04-29-struggle-bottleneck-x"`.
- `title` (string): short, human-readable working title.
- `hook` (string): one-line hook in Sharon's voice (conspiratorial, punchy, personal).
- `type` (enum): `"Struggle"` | `"Win"` | `"Tutorial"` | `"Behind-the-scenes"`.
- `platform` (string): primary platform (e.g. `"Instagram"`, `"X"`, `"LinkedIn"`, `"YouTube Short"`).
- `goal` (enum-ish): `"Build in public"` | `"Teach"` | `"Nurture"` | `"Sell"`.
- `status` (enum): `"idea"` | `"ready_for_drafting"` | `"draft_in_progress"` | `"ready_for_edit"` | `"ready_for_publishing"` | `"published"`.
- `status_updated_at` (ISO date): when status last changed.
- `priority` (integer): 1 is highest; 1–3 usually "this week".

Optional: `source`, `week` (YYYY-WW), `created_at`, `updated_at`, `notes`, `experimental` (boolean).

**Struggle posts**: do not require resolution; the struggle IS the content. Maintain 25–30% Struggle ratio in top 10 queue items.

## Content Dedup Gate

**Blocking rule.** No entry may be written to `state/current-queue.json` until all four checks pass. Applies to every agent, no exceptions.

1. **Title fuzzy match**: scan existing entries for similarity > 0.7.
2. **Hook semantic overlap**: same core scenario, metaphor, or reveal.
3. **Published lookback (30 days)**: scan published entries within 30 days for topic overlap.
4. **Source story dedup**: confirm source does not already have a queue entry.

When any check fails, output this block and stop:

```
DEDUP CONFLICT DETECTED
─────────────────────────────────────────
Check failed : [1 | 2 | 3 | 4] — [Title | Hook | Published | Source]
New entry    : {new_entry.id} — "{new_entry.title}"
Conflicts with: {existing.id} — "{existing.title}" [{existing.status}]
Reason       : [one sentence plain-language explanation]
─────────────────────────────────────────
Action required: Operator must confirm, merge, or cancel before queue write proceeds.
```

## Queue Audit (Session Start)

At the start of every content session:

1. Read `state/current-queue.json`.
2. Check for duplicate `id` values.
3. Check for `status: ready_for_publishing` entries with similar `status: published` entries.
4. Report:

```
QUEUE AUDIT
───────────────────────────────
Total entries : {n}
Published     : {n}
Ready         : {n}
Drafting      : {n}
Conflicts found: [none | list them]
───────────────────────────────
```

After successful queue writes, commit a Hermes checkpoint with `[hermes-context]`.

## Hermes Checkpoint Format

```text
CHECKPOINT: <one-line description>

[hermes-context]
Decisions: <what was locked in>
Remaining: <what's next>
Tried: <what failed and why — omit if nothing failed>
Confidence: high | medium | low
Context_type: build | content | system | research
Agent: <claude | codex | cos>
[/hermes-context]
```

## Platform Constraints

- **X (Twitter)**: Every post in a thread must be strictly under 280 characters. Exceeding this must be flagged as "REJECTED".
- **Automated Scheduling**: Once content is approved (moved to `approved/` or marked approved by user), Claude Code schedules via Blotato immediately. No separate confirmation needed for the scheduling action itself.

## Rules System

`rules/` is the canonical enforcement layer:

- `rules/common/`: governance, approval gates, dedup, git, security.
- `rules/content/`: voice, public sanitization, struggle ratio.
- `rules/python/`: Hermes and CLI-native engineering patterns.

If a rule conflicts with this file, `AGENTS.md` wins and the conflict must be reported.

## Parallel vs Sequential

**Parallel** (independent operations): content ideation (Trend Researcher, Format Selector, Voice-Match Ideator), security/sanitization checks, repository exploration.

**Sequential** (dependent gates): ideation → dedup gate → human review → drafting → sanitization → user approval → scheduling → queue updates.

## Workflow Surface Policy

Road4AI is skills-first. Canonical workflows live in `skills/<skill-name>/SKILL.md`. Durable policy lives in `rules/`. Slash commands are legacy and should not be expanded.
