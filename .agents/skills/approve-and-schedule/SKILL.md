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

Seven steps, same every time. The order matters — each step depends on the previous one succeeding.

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

```bash
python3 tools/schedule_post.py drafts/approved/<filename>.md --platform <platform> --schedule "<ISO-time>" --yes --force
```

- `--force` is needed when the queue entry already has a stale blotato_id
- The script auto-generates visuals for LinkedIn posts
- X threads are detected automatically from `## Tweet N` headers
- Video generation can take up to 5 minutes — set timeout to 600000ms

### Step 5: Verify queue sync

After scheduling, verify the queue entry was updated:

```bash
python3 -c "
import json
data = json.load(open('state/current-queue.json'))
for e in data['queue']:
    if '<filename-stem>' in e.get('id',''):
        print('status=%s  blotato_id=%s' % (e.get('status'), e.get('blotato_id','none')))
"
```

Both `status` should be `scheduled` and `blotato_id` should be populated. If not, the sync failed — see Troubleshooting.

### Step 6: Run ratio check

```bash
python3 tools/check_struggle_ratio.py
```

If FAIL, do not proceed with more scheduling until a Struggle candidate is added.

### Step 7: Commit

```bash
git add drafts/approved/<filename>.md state/current-queue.json
git commit -m 'content: schedule <title>'
```

### Step 8: Archive scheduled draft

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
The `sync_queue_status` function in schedule_post.py should handle this automatically. If it didn't, manually update:
```bash
python3 -c "
import json
data = json.load(open('state/current-queue.json'))
for e in data['queue']:
    if '<entry-id>' in e.get('id',''):
        e['status'] = 'scheduled'
        e['blotato_id'] = '<blotato-id-from-output>'
json.dump(data, open('state/current-queue.json','w'), indent=2, ensure_ascii=False)
"
```

**schedule_post.py says "DUPLICATION BLOCKED":**
The queue entry already has a blotato_id or status=scheduled. Use `--force` if the user explicitly approved re-scheduling.

**Video generation timeout:**
LinkedIn video visuals can take 3-5 minutes. Retry with `--schedule` flag and a 600s timeout. If still failing, fall back to image visual.

**Karen verdict missing:**
Do NOT use `--force` to bypass Karen. The Karen gate is inviolable per AGENTS.md. Run `python3 karen.py` first.
