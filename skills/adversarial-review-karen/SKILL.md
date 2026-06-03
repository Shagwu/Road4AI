---
name: adversarial-review-karen
description: Use for Road4AI adversarial review before merge, publication, or approval when staged changes or drafts need a high-signal local Karen audit.
origin: Road4AI
tools:
  - Bash
  - Read
  - Grep
---

# Adversarial Review Karen

## When to Activate

- Staged changes need a local adversarial review before commit or merge.
- A draft is moving toward `drafts/ready/` or user approval.
- A change touches governance, security, publishing, queue state, content voice, or platform constraints.
- The user asks for Karen, adversarial review, a ruthless review, or a local review gate.

Do not use this for ordinary copy edits, broad brainstorming, or unstaged exploratory work.

## The Mechanism

Karen is a two-model local review pipeline in `karen.py`.

- Adversary model: defaults to `mistral-nemo`.
- Filter model: defaults to `qwen2.5-coder:14b`.
- Runtime: local Ollama through `OLLAMA_HOST`, defaulting to the local Ollama server.
- Input: staged git diff.
- Mode detection: content mode is used when staged files are prose, markdown, JSON, TXT, or logs.

The adversary over-accuses. Karen filters those accusations through a strict review gate and keeps only issues that survive.

## Review Criteria

Karen checks for:

- real bugs, missing imports, null dereferences, stale closures, broken contracts, race conditions, and security issues;
- hallucinated claims about Road4AI systems not supported by project docs;
- content-mode false positives such as treating hashtags as injection patterns;
- platform limits, especially strict under-280-character X posts;
- signal-to-noise, removing pedantic or taste-only complaints.

## Workflow

1. Review `git status --short`.
2. Stage only the files intended for review.
3. Run:

```bash
python3 karen.py
```

4. If needed, override models:

```bash
python3 karen.py --adversary-model mistral-nemo --filter-model qwen2.5-coder:14b
```

5. Read both sections:
   - raw adversary accusations;
   - Karen's final verdict.
6. Fix any surviving issues before merge, approval, or publishing.
7. If Karen cannot run because Ollama or a model is unavailable, report the blocker and run deterministic checks that still apply.

## Output Contract

Return:

- review target and staged files;
- model pair used;
- verdict: `APPROVED`, `REQUEST_CHANGES`, or `BLOCKED`;
- severity-ranked surviving issues;
- dismissed false positives worth noting;
- required fixes before the next gate.

## Anti-Patterns

- Do not treat Karen as the human approval gate.
- Do not run Karen on unrelated staged changes.
- Do not use `--post-pr` unless the user explicitly wants a PR comment.
- Do not bypass deterministic gates such as public sanitization or queue validation because Karen approved the diff.

## Related Skills

- `public-sanitization-review`
- `hermes-checkpoint-patterns`

