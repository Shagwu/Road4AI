# Road4AI Agent Operating Contract

This document governs the collaboration between **Gemini CLI** and **Codex** (and other agents) working on the Road4AI repository.

## The Golden Rule: Read First
**Every session MUST start by reading these core coordination files:**
1. `AGENTS.md` (this file)
2. `state/current-queue.json`
3. `docs/brand-voice.md`
4. `docs/content-strategy.md`

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
  - Read `drafts/approved/`.
  - Use Blotato tools to schedule/publish content.
  - Record publishing success in `state/published-log.json`.
  - Archive published drafts to `drafts/archived/`.

## Shared State Architecture
We use the file system as our shared memory:
- `state/current-queue.json`: Active tasks and ideas.
- `state/published-log.json`: Record of everything already posted.
- `drafts/`: Folders represent the lifecycle stage (Idea -> Ready -> Approved -> Archived).

## Coordination Protocol
1. **Deduplication**: Before drafting, check `state/published-log.json` and `state/current-queue.json`.
2. **Monday Ritual**: Every Monday, the Chief of Staff (Gemini CLI) parses `inbox.md` to identify the top 5 content moments, maps them to types (Struggle/Win/Tutorial/BTS), and updates `state/current-queue.json`.
3. **Approval**: Only the user moves files from `ready/` to `approved/`.
4. **Traceability**: Every published post must have a corresponding entry in `state/published-log.json`.

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
 underlying technical issue.
  - **Authenticity:** Struggle posts do not require resolution or code fixes; the "Struggle" *is* the content.
  - **Ratio:** Maintain a 25-30% Struggle ratio in the top 10 queue items.

- The CoS should avoid silently deleting items.
  - Old or unused ideas can be deprioritised (higher `priority` number) or marked clearly in `status` or `notes` (e.g. “parked”).
