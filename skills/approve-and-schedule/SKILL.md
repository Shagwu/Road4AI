---
name: approve-and-schedule
description: Move a draft from ready/ to approved/, update frontmatter, schedule via Blotato, verify queue sync, and archive. Single workflow for the full approval-to-scheduling-to-archive pipeline.
origin: Road4AI
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

# Approve and Schedule

## When to Activate

- User says "approve and schedule" or "schedule this post" for a draft in `drafts/ready/`
- User approves multiple drafts in batch and wants them all scheduled
- Moving content through the approval gate before Blotato scheduling

Do not use for drafts already in `drafts/approved/` (use schedule_post.py directly) or for content that hasn't been written yet.

## The Workflow

Seven steps, same every time. The order matters — each step depends on the previous one succeeding. Steps 4, 5, 7, and 8 are external actions or repository-state changes: stop and get Shagwu's explicit go-ahead before running each one, even mid-batch. Do not chain them autonomously.

### Step 1: Verify draft exists and is in `drafts/ready/`

```bash
ls drafts/ready/<filename>.md
```

If not found in `ready/`, check `approved/` (may already be approved) or `archived/` (already published).

### Step 2: Move to `drafts/approved/`

```bash
mv drafts/ready/<filename>.md drafts/approved/<filename>.md
```

### Step 3: Update frontmatter

The draft must have:
- `karen_verdict: APPROVED` (not null, not empty)
- No `scheduled: true` (would block re-scheduling)

If `karen_verdict` is null, the user must run Karen first. Do not bypass this gate.

### Step 4: Run schedule_post.py

**Stop here. Do not run this step without Shagwu's explicit approval of the specific action (immediate or scheduled, with exact date/time/timezone if scheduled) for this specific draft.**

```bash
python3 tools/schedule_post.py drafts/approved/<filename>.md --platform <platform> --schedule "<YYYY-MM-DDTHH:MM>" --tz "<IANA timezone>" --yes
```

- `--force` is no longer used here by default — the draft is already in `drafts/approved/`, and a stale/duplicate blotato_id should be investigated, not silently overridden. Only use `--force` if Shagwu has explicitly approved re-scheduling over an existing conflict.
- `--yes` skips only ancillary prompts (clone-media fallback, missing-media warning). The tool will still show one final confirmation summary — action, platform, exact date/time/timezone with UTC equivalent (if scheduled), Karen verdict, content preview — and require typing `y` before anything reaches Blotato. This is not skippable and is the point where Shagwu's approval is actually exercised for the external action.
- The script auto-generates visuals for LinkedIn posts
- X threads are detected automatically from `## Tweet N` headers
- Video generation can take up to 5 minutes — set timeout to 600000ms

### Step 5: Verify queue sync

After scheduling, verify the queue entry was updated. This is a read-only check — no queue write happens here; the queue write already happened as part of Step 4's own `sync_queue_status` call.

```bash
python3 -c "
import json
data = json.load(open('state/current-queue.json'))
for e in data['queue']:
    if '<filename-stem>' in e.get('id',''):
        print('status=%s  blotato_id=%s' % (e.get('status'), e.get('blotato_id','none')))
"
```

Both `status` should be `scheduled` and `blotato_id` should be populated. **If not, the sync failed. Halt here and report the failure to Shagwu — do not manually overwrite `state/current-queue.json` to force the values into place.** A failed sync means the queue no longer reliably reflects what Blotato actually did; that discrepancy needs human review, not a silent patch.

### Step 6: Run ratio check

```bash
python3 tools/check_struggle_ratio.py
```

If FAIL, do not proceed with more scheduling until a Struggle candidate is added.

### Step 7: Commit

**Stop here. Get Shagwu's explicit approval before staging or committing.**

```bash
git add drafts/approved/<filename>.md state/current-queue.json
git commit -m 'content: schedule <title>'
```

### Step 8: Archive scheduled draft

**Stop here. Get Shagwu's explicit approval before moving the file or patching the queue's draft_path.**

After Blotato confirms scheduling, move the draft from `drafts/approved/` to `drafts/archived/` and update the queue entry's `draft_path` to match:

```bash
mv drafts/approved/<filename>.md drafts/archived/<filename>.md

python3 -c "
import json
data = json.load(open('state/current-queue.json'))
for e in data['queue']:
    if '<filename-stem>' in e.get('id',''):
        e['draft_path'] = 'drafts/archived/<filename>.md'
json.dump(data, open('state/current-queue.json','w'), indent=2, ensure_ascii=False)
"
```

This prevents duplicate-approval risk AND keeps queue references accurate. Without the queue patch, `draft_path` points to a file that no longer exists at the old location — the exact pattern that caused the 7 phantom references in S-4.

## Replaces

The ad hoc approve-and-schedule pattern that was repeated across sessions:
1. `mv drafts/ready/ drafts/approved/` — manual file move
2. Edit frontmatter in each draft — manual per-file edit
3. `python3 tools/schedule_post.py ...` — Blotato scheduling
4. Inline python to check queue status — repeated queue-peek calls
5. `python3 tools/check_struggle_ratio.py` — ratio verification
6. `git add ... && git commit` — manual staging
7. `mv drafts/approved/ drafts/archived/` — manual archival

This skill consolidates those seven steps into a documented workflow with known guardrails.

When approving multiple drafts:

1. Move all files from `ready/` to `approved/` in one `mv` command
2. Update frontmatter on all files in a single python pass
3. Schedule each via Blotato (sequential — each takes 30s-5min)
4. Verify all queue entries synced
5. Run ratio check once at the end
6. Single commit for the batch
7. Archive all scheduled drafts in one `mv` command and patch all queue draft_paths

## Troubleshooting

**Queue entry not synced (status still ready_for_drafting, blotato_id null):**
The `sync_queue_status` function in schedule_post.py should handle this automatically. If it didn't, **halt and report to Shagwu.** Do not manually overwrite `state/current-queue.json` to patch the status or blotato_id — a failed automatic sync is a signal that something needs human review, not a value to paper over. Report: the draft filename, what Blotato returned (submission ID / status if available), and the actual current queue-entry contents.

**schedule_post.py says "DUPLICATION BLOCKED":**
The queue entry already has a blotato_id or status=scheduled. Report this to Shagwu. Only use `--force` if Shagwu has explicitly approved re-scheduling over the existing entry.

**Video generation timeout:**
LinkedIn video visuals can take 3-5 minutes. Retry with `--schedule` flag and a 600s timeout. If still failing, fall back to image visual.

**Karen verdict missing:**
Do NOT use `--force` to bypass Karen. The Karen gate is inviolable per AGENTS.md. Run `python3 karen.py` first.
