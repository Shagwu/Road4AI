# Road4AI Agent Operating Contract

This document governs the collaboration between **Gemini CLI** and **Codex** (and other agents) working on the Road4AI repository.

## The Golden Rule: Read First
**Every session MUST start by reading these core coordination files:**
1. `AGENTS.md` (this file)
2. `state/current-queue.json`
3. `docs/brand-voice.md`
4. `docs/content-strategy.md`

For governance or content sessions, also read:
5. `WORKING-CONTEXT.md`
6. Relevant files under `rules/`

## Rules System

`rules/` is the canonical enforcement layer for repeatable Road4AI policy.

- `rules/common/`: governance, approval gates, dedup, git, and security.
- `rules/content/`: voice, public sanitization, and content mix.
- `rules/python/`: Hermes and CLI-native engineering patterns.

Agents must use these files as standing instructions. If a rule conflicts with this file, `AGENTS.md` wins and the conflict must be reported.

## Autonomy Levels

### DO

- Read the required coordination files before work begins.
- Run the queue audit at the start of content sessions.
- Draft, edit, validate, and organize content within the lifecycle folders.
- Use deterministic checks for deduplication, sanitization, and platform constraints.
- Preserve the existing shape of shared state files unless the user approves a migration.

### ASK

- Before editing `AGENTS.md`, changing approval gates, publishing content, deploying code, or modifying credentials.
- Before resolving or bypassing a dedup conflict.
- Before moving content into a new lifecycle stage when ownership is unclear.

### NEVER

- Modify `AGENTS.md` without explicit per-session human approval.
- Move content into `drafts/approved/` on behalf of the user.
- Publish, schedule, or mark content as approved before the approval gate is satisfied.
- Delete queue entries silently.
- Include secrets, private data, or copy-pasteable exploit payloads in public content.

## Agent Roles

### Codex (Planner & Drafter)
- **Focus**: Strategy, planning, content drafting, and reasoning.
- **Workflow**:
  - Analyze the codebase and content strategy.
  - Propose new content ideas to `state/current-queue.json`.
  - Create drafts in `drafts/ideas/`.
  - Move finalized drafts to `drafts/ready/`.

### Gemini CLI (Operator & Publisher)
- **Focus**: Execution, tool integration (Blotato, Workspace), and publishing.
- **Workflow**:
  - **Session Start**: Run `git log --grep="CHECKPOINT:" --format="%B" -3`. Parse each `[hermes-context]` block and brief the operator on what was last completed, what's remaining, and any low-confidence states needing review.
  - Read `drafts/approved/`.
  - Use Blotato tools to schedule/publish content.
  - Record scheduling details in `state/current-queue.json`.
  - Archive scheduled drafts to `drafts/archived/` immediately after Blotato confirms scheduling, then update queue paths so the approved folder stays empty.
  - Record final publishing success in `state/published-log.json` when live URLs or final statuses are available.

### Content Scout (Content Researcher)
- **Focus**: Knowledge extraction from transcripts, articles, and videos.
- **Workflow**:
  - Receive source (transcript, URL, or text).
  - Produce a 9-section knowledge extraction (Part 1).
  - Generate a clean `INBOX.MD` append block (Part 2).
  - Automatically append the signal block to `inbox.md`.

### Signal Harvester [L8 Autonomy]
- **Role**: Autonomous web reading across platforms (Twitter, Reddit, GitHub, YouTube, RSS). Feeds normalized signals into Hermes, caches deduplicated results.

**DO:**
- Query Agent-Reach CLI for signals on demand or scheduled
- Normalize results → structured JSON, ingest into Hermes
- Maintain 24h dedup cache (no re-scraping same source)
- Return confidence scores + source metadata to dependent agents

**ASK:**
- Before adding confidence signal to Hermes checkpoint (human review gate?)
- Platform expansion beyond Twitter/GitHub POC (rate limits?)
- Cache eviction policy changes

**NEVER:**
- Store platform credentials or auth tokens
- Post/write/modify any content (read-only always)
- Scrape without 2s delay between requests
- Bypass platform ToS (headless browsing only where legal/documented)

## Parallel vs. Sequential Work

### Parallel

Use parallel workstreams when operations are independent:

- Content ideation: Trend Researcher, Format Selector, and Voice-Match Ideator can run simultaneously.
- Security/content safety: sanitizer review, trope audit, and platform constraint validation can run simultaneously.
- Repository exploration: file reads, searches, and independent inspections should be parallelized where possible.

### Sequential

Keep dependent gates sequential:

1. Ideation and source extraction.
2. Dedup gate.
3. Human review when required.
4. Drafting.
5. Public sanitization and platform validation.
6. User approval.
7. Scheduling or publishing.
8. Queue and published-log updates.

## Workflow Surface Policy

Road4AI is skills-first.

- Canonical reusable workflows live in `skills/<skill-name>/SKILL.md`.
- Durable operating policy lives in `rules/`.
- Slash commands or harness-specific command folders are legacy compatibility surfaces and should not be expanded unless explicitly requested.
- New agents or skills should only be added when they solve a repeatable Road4AI problem.

## Shared State Architecture
We use the file system as our shared memory:
- `state/current-queue.json`: Active tasks and ideas.
- `state/published-log.json`: Record of everything already posted.
- `drafts/`: Folders represent the lifecycle stage (Idea -> Ready -> Approved -> Archived).
- `WORKING-CONTEXT.md`: Current sprint, constraints, backlog, and completed context.
- `rules/`: Governance and enforcement rules.
- `skills/`: Reusable Road4AI workflows.

## Coordination Protocol
1. **Deduplication**: Before drafting, check `state/published-log.json` and `state/current-queue.json`.
2. **Monday Ritual**: Every Monday, the Chief of Staff (Gemini CLI) parses `inbox.md` to identify the top 5 content moments, maps them to types (Struggle/Win/Tutorial/BTS), and updates `state/current-queue.json`.
3. **Approval**: Only the user moves files from `ready/` to `approved/`.
4. **Approved Folder Hygiene**: `drafts/approved/` is a scheduling inbox, not storage. Once approved content is scheduled in Blotato, move it to `drafts/archived/` immediately to prevent human duplicate approval or reposting.
5. **Traceability**: Every scheduled post must have a corresponding entry in `state/current-queue.json`; every published post must have a corresponding entry in `state/published-log.json` when final publication details are available.
6. **Governance Lock**: The system's 'Manual Approval Gate.' Any mutation to `AGENTS.md` (operating contracts) MUST be reviewed and approved by the human conductor. Agents are strictly prohibited from negotiating or mutating their own operating contracts without a per-session human confirmation, preventing autonomous drift in system-wide rules.
7. **Write Gate**: `AGENTS.md` must be treated as a protected constitution. Agents may read it, but must not write to it directly as part of normal task execution. This ensures the integrity of the system-wide hierarchy.
8. **Pre-Reveal Parallel Workstream**: Before the Hermes v2.0 reveal on 2026-05-26, the team must track and close these technical gaps in parallel:
   - Enforce filesystem-level write protection on `AGENTS.md`.
   - Enforce hard `NEVER` rules in agent specs so config mutations are surfaced with `[HUMAN_REVIEW_REQUIRED]`.
   - Finish the input sanitization defense layer before making public safety claims about transcript handling.
9. **Public Sanitization**: Any draft discussing security, prompt injection, autonomy failures, private workflows, or customer examples must pass public sanitization review before approval or scheduling.
10. **Security Before Commit**: Before committing, check for hardcoded secrets, bearer tokens, OAuth files, private local paths, private account IDs, copy-pasteable exploit payloads, and accidental protected-file edits.
11. **Queue Shape Preservation**: `state/current-queue.json` currently uses a top-level `queue` array. Preserve this shape unless the user explicitly approves a schema migration.

## Content Queue Schema (state/current-queue.json)

The content backlog lives in `state/current-queue.json`.

This file is an array of objects. Each object represents a single content item that can be drafted, edited, or published.

### Required fields

- `id` (string)
  - A unique identifier for this item (e.g. `"2026-04-29-struggle-bottleneck-x"`).
  - If not provided, the Chief of Staff may generate one from the date + type + a short slug.

- `title` (string)
  - Short, human-readable working title.
  - Should be clear enough that a human can recognise the idea at a glance.

- `hook` (string)
  - One-line hook in Sharon's voice (conspiratorial, punchy, personal).
  - This is the starting line or main promise of the post.

- `type` (string; enum)
  - One of: `"Struggle"`, `"Win"`, `"Tutorial"`, `"Behind-the-scenes"`.

- `platform` (string)
  - Primary platform this item is meant for (e.g. `"Instagram"`, `"X"`, `"LinkedIn"`, `"YouTube Short"`).

- `goal` (string; enum-ish)
  - Main intent of the content.
  - Use one of: `"Build in public"`, `"Teach"`, `"Nurture"`, `"Sell"`.

- `status` (string; enum)
  - Current stage in the pipeline.
  - Allowed values:
    - `"idea"` – captured but not yet prioritised.
    - `"ready_for_drafting"` – selected for this week; needs a first draft.
    - `"draft_in_progress"` – Codex or Sharon is working on it.
    - `"ready_for_edit"` – draft exists, needs edit/Karen filter.
    - `"ready_for_publishing"` – approved, ready to schedule/post.
    - `"published"` – already posted.

- `status_updated_at` (string; ISO date)
  - When the `status` field was last changed. Required for tracking drafting velocity.

- `priority` (integer)
  - A simple numeric priority where `1` is highest.
  - For weekly planning, `1–3` are usually “this week”; higher numbers are backlog.

### Helpful optional fields

- `source` (string)
  - Where this idea came from, e.g. `"inbox"`, `"roadmap"`, `"audience_question"`, `"experiment"`.

- `week` (string)
  - Target week in `YYYY-WW` format, e.g. `"2026-18"` for week 18 of 2026.
  - The CoS can fill or update this during the weekly planning ritual.

- `created_at` (string; ISO date)
  - When this queue item was created.

- `updated_at` (string; ISO date)
  - When this queue item was last modified.

- `notes` (string)
  - Any extra context: raw quote, outline, links to reference content.

- `experimental` (boolean)
  - `true` if this is an experimental idea (new format/angle), else `false`.

### Agent behaviour rules

- When the Chief of Staff (Gemini CLI) or Codex adds new items from `INBOX.MD`:
  - Always set: `title`, `hook`, `type`, `platform`, `goal`, `source`, `status`, `priority`.
  - Set `source` to `"inbox"` for items derived from `INBOX.MD`.
  - Prefer to set `status` to `"ready_for_drafting"` for the top 3 chosen for this week.

- When enforcing the weekly mix:
  - The CoS should, where possible, ensure that among items with `priority` 1–3:
    - At least 1 item has `type = "Struggle"`.
    - At least 1 item has `type = "Win"`.
    - At least 1 item has `type = "Tutorial"` or `"Behind-the-scenes"`.

- When moving items through the pipeline:
  - Drafting moves `status`:
    - from `"ready_for_drafting"` → `"draft_in_progress"` → `"ready_for_edit"`.
  - After the Karen filter / final edit:
    - `"ready_for_edit"` → `"ready_for_publishing"`.
  - Once posted:
    - `"ready_for_publishing"` → `"published"` and a record should be added to `state/published-log.json`.

- The CoS should avoid silently deleting items.
  - Old or unused ideas can be deprioritised (higher `priority` number) or marked clearly in `status` or `notes` (e.g. “parked”).

- **Struggle Posts**:
  - **Authenticity:** Struggle posts do not require resolution or code fixes; the "Struggle" *is* the content.
  - **Ratio:** Maintain a 25-30% Struggle ratio in the top 10 queue items.

### Content Dedup Gate

This is a **blocking rule**. No entry may be written to `state/current-queue.json` until all four checks below pass. If any check fails, the agent must STOP and report the conflict to the operator before proceeding.

This rule applies to every agent in the COS system: gemini-cli, claude, codex, cos. No exceptions for "quick" additions or "minor" queue updates.

#### The Four Checks

1. **CHECK 1 — Title fuzzy match**: Scan all existing queue entries for title similarity (> 0.7).
2. **CHECK 2 — Hook semantic overlap**: Hooks share the same core scenario or inciting moment (e.g., same event, metaphor, or reveal).
3. **CHECK 3 — Published lookback (30 days)**: Scan entries with `status: published` and `status_updated_at` within 30 days for topic or system component overlap.
4. **CHECK 4 — Source story dedup**: New entry traces back to an `inbox.md` capture or roadmap item that already has a queue entry.

#### How to report a conflict

When any check fails, output this block before stopping:

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

Do not attempt to resolve the conflict automatically. Wait for operator instruction.

#### On session start — state audit

At the start of every content session, before any new work begins, run this audit:
1. Read `state/current-queue.json`.
2. Check for duplicate `id` values.
3. Check for entries where `status: ready_for_publishing` and a similar entry exists with `status: published`.
4. Report findings to operator.

Format:
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

#### Hermes checkpoint after queue write

After any successful queue write, commit a Hermes checkpoint with the `[hermes-context]` tag detailing the decision and dedup status.

#### Karen review trigger

If Karen is active, she must sign off on any queue entry that:
- Was flagged by one of the four checks but operator approved anyway.
- Is a reframe of a published post.
- Has a hook similarity score above 0.5 with any published entry.

- **X (Twitter) Constraints:**
  - **Character Limit:** Every post in an X thread must be strictly under 280 characters. Any draft exceeding this limit must be flagged as "REJECTED" by the validation layer (Karen).
  - **Automated Scheduling:** Once content is moved to the `approved/` folder or marked as approved by the user, Gemini CLI should proceed immediately to schedule via Blotato. The manual approval of the draft content is the final gate; no separate confirmation is required for the scheduling action itself. After Blotato scheduling is confirmed, move the scheduled draft to `drafts/archived/` and update queue paths so `drafts/approved/` does not invite duplicate human approval or duplicate calendar entries.
