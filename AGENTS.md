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
  - **Session Start**: Run `git log --grep="CHECKPOINT:" --format="%B" -3`. Parse each `[hermes-context]` block and brief the operator on what was last completed, what's remaining, and any low-confidence states needing review.
  - Read `drafts/approved/`.
  - Use Blotato tools to schedule/publish content.
  - Record publishing success in `state/published-log.json`.
  - Archive published drafts to `drafts/archived/`.

### Content Scout (Content Researcher)
- **Focus**: Knowledge extraction from transcripts, articles, and videos.
- **Workflow**:
  - Receive source (transcript, URL, or text).
  - Produce a 9-section knowledge extraction (Part 1).
  - Generate a clean `INBOX.MD` append block (Part 2).
  - Automatically append the signal block to `inbox.md`.

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
5. **Governance Gate**: Any mutation to `AGENTS.md` (operating contracts) MUST be reviewed and approved by the human conductor. Agents are strictly prohibited from committing changes to this file unprompted.
6. **Write Gate**: `AGENTS.md` must be treated as a protected governance file. Agents may read it, but must not write to it directly as part of normal task execution.
7. **Pre-Reveal Parallel Workstream**: Before the Hermes v2.0 reveal on 2026-05-26, the team must track and close these technical gaps in parallel:
   - Enforce filesystem-level write protection on `AGENTS.md`.
   - Enforce hard `NEVER` rules in agent specs so config mutations are surfaced with `[HUMAN_REVIEW_REQUIRED]`.
   - Finish the input sanitization defense layer before making public safety claims about transcript handling.

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

- **X (Twitter) Constraints:**
  - **Character Limit:** Every post in an X thread must be strictly under 280 characters. Any draft exceeding this limit must be flagged as "REJECTED" by the validation layer (Karen).
  - **Automated Scheduling:** Once content is moved to the `approved/` folder or marked as approved by the user, Gemini CLI should proceed immediately to schedule via Blotato. The manual approval of the draft content is the final gate; no separate confirmation is required for the scheduling action itself.
