# Content Pipeline Workflow

This workflow ensures consistent collaboration between Codex and Gemini CLI.

## Phase 1: Planning (Codex)
1. **Analyze**: Read `docs/content-strategy.md` and `state/published-log.json`.
2. **Brainstorm**: Add 3-5 ideas to `state/current-queue.json`.
3. **Draft**: Pick an approved idea and write a draft in `drafts/ideas/`.
4. **Finalize**: Move the draft to `drafts/ready/` when it meets `docs/brand-voice.md`.

## Phase 2: Review (User)
1. **Edit**: Review the draft in `drafts/ready/`.
2. **Approve**: Move the file to `drafts/approved/` when it's ready to post.

## Phase 3: Execution (Gemini CLI)
1. **Fetch**: Read `drafts/approved/`.
2. **Execute**: 
   - Use `blotato_create_post` to schedule or publish.
   - For threads, use `additionalPosts`.
3. **Log**:
   - Update `state/published-log.json` with the `postSubmissionId` and platform.
   - Move the draft from `drafts/approved/` to `drafts/archived/`.
