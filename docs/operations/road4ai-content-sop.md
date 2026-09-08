# Road4AI Content Session SOP

## Purpose

Use this SOP for every Road4AI content session. The Road4AI Team coordinates the Operator, Researcher, and Reviewer roles. Never queue, schedule, or publish content without my explicit approval.

## 1. Operator Session Start

Before content work begins:

- Confirm the working directory is `/Users/shagwu/Road4AI`.
- Read and follow `AGENTS.md`.
- Read `WORKING-CONTEXT.md`.
- Read the brand-voice guidance.
- Read the current content queue.
- Check the queue for duplicate content IDs and conflicting statuses.
- Run the struggle-ratio guardrail check using `tools/check_struggle_ratio.py`.
- Report the results clearly.
- Stop if a mandatory file is missing, unreadable, or a guardrail fails.

## 2. Research and Content Plan

For a topic-only session:

- Research claims only when necessary.
- Identify the target audience, core message, useful angle, and call to action.
- Create a concise plan before drafting.
- Present the plan for my approval.
- Do not draft, queue, schedule, or publish until I approve the plan.

For an existing-draft session:

- Review the draft for clarity, usefulness, brand voice, factual support, and audience fit.
- Suggest edits or provide a revised draft.
- Stop for my approval before any queue action.

## 3. Reviewer Pre-Queue Audit

Before writing to the content queue, the Reviewer must check:

- Factual accuracy and unsupported claims.
- Road4AI brand voice and audience fit.
- Clarity, structure, and originality.
- Duplicate topics, IDs, and conflicting queue statuses.
- The struggle-ratio guardrail.
- Whether the post is ready, needs revision, or should be rejected.

The Reviewer must report findings and stop for my explicit queue approval.

## 4. Queue-to-Publish Flow

After I explicitly approve the queue entry:

- Add the approved item to the queue.
- Verify that the correct ID, status, platform, post text, and metadata were saved.
- Report the completed queue update.
- Stop and ask whether I want to keep it queued or schedule it.

Before scheduling:

- Ask me for my preferred publish date and time.
- Never assume immediate scheduling.
- Never auto-schedule.

## 5. Explicit Publishing Confirmation

Immediately before publishing, show me:

- The final post text.
- Platform.
- Scheduled date and time.
- Time zone.
- Links, media, or attachments, if relevant.

Publish only after I explicitly confirm the exact version, platform, date, and time.

## 6. Session Closeout

After publication:

- Update relevant tracking records.
- Create a git commit with a `[hermes-context]` checkpoint.
- Record decisions made, completed work, remaining work, what was tried, confidence level, context type, and agent role.
- Report a concise session summary.
