---
name: public-sanitization-review
description: Use before Road4AI drafts about security, prompt injection, autonomy failures, private workflows, customer examples, or public launch content are approved or scheduled.
origin: Road4AI
tools:
  - Read
  - Edit
  - Bash
  - Grep
---

# Public Sanitization Review

## When to Activate

- A draft mentions security, prompt injection, exploit patterns, agent autonomy, credentials, private accounts, or workspace exports.
- A draft includes real prompts, customer examples, paths, handles, or operational IDs.
- Content is about to move from `ready` to `approved` or be scheduled.

Do not use this as a generic grammar edit. Its job is public safety and abstraction.

## The Mechanism

The review preserves the engineering lesson while removing material that should not be public or copy-pasteable.

## Workflow

1. Read the target draft.
2. Scan for sensitive data:
   - secrets, tokens, OAuth files, bearer strings;
   - local absolute paths;
   - real client, user, or account identifiers;
   - copy-pasteable exploit strings;
   - raw private prompts;
   - exact financial figures not essential to the lesson.
3. Replace unsafe details with approved placeholders.
4. Preserve the technical failure mode and decision tradeoff.
5. If a detail cannot be safely abstracted without changing the claim, flag `[HUMAN_REVIEW_REQUIRED]`.

## Output Format

```text
PUBLIC SANITIZATION REVIEW
--------------------------
Status: PASS | CHANGES_MADE | HUMAN_REVIEW_REQUIRED
Draft: <path>
Findings:
- <finding>
Changes:
- <change>
Remaining risk:
- <risk or none>
```

## Related Skills

- `content-pipeline`
