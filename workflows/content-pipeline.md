# Content Pipeline Workflow

This workflow ensures consistent collaboration between Codex and Claude Code.

## Phase 1: Planning (Codex)
1. **Analyze**: Read `docs/content-strategy.md` and `state/published-log.json`.
2. **Brainstorm**: Add 3-5 ideas to `state/current-queue.json`.
3. **Draft**: Pick an approved idea and write a draft in `drafts/ideas/`.
4. **Finalize**: Move the draft to `drafts/ready/` when it meets `docs/brand-voice.md`.

## Phase 2: Review (User)
1. **Edit**: Review the draft in `drafts/ready/`.
2. **Approve**: Move the file to `drafts/approved/` when it's ready to post.

## Phase 3: Execution (Claude Code)
1. **Fetch**: Read `drafts/approved/`.
2. **Execute**: 
   - Use `blotato_create_post` to schedule or publish.
   - For threads, use `additionalPosts`.
3. **Log**:
   - Update `state/current-queue.json` with the `postSubmissionId`, platform, and scheduled time.
   - Move scheduled drafts from `drafts/approved/` to `drafts/archived/` after Blotato confirms they are scheduled, so Claude and the human operator cannot mistake them for unscheduled approvals and create duplicate calendar entries.
   - Update `state/published-log.json` with Blotato scheduling confirmation (blotato_id, scheduled_time). Do not verify whether posts appeared on platforms.
