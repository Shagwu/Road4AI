---
name: open-items-compiler
description: Compile governance, infrastructure, and operational gaps into a tracked open-items document. Use when the user asks to audit the system, find gaps, or compile open items.
origin: Road4AI
tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Open Items Compiler

## When to Activate

- The user asks to "audit the system" or "find gaps"
- The user asks to "compile open items" or "what's broken?"
- A governance or infrastructure review is needed
- The user wants to track technical debt or known issues

Do not use this for content creation, scheduling, or routine operations.

## The Mechanism

This skill systematically scans the Road4AI system for governance, infrastructure, and operational gaps. It produces a tracked document (`.agents/open-items.md`) with severity ratings and ownership.

## Workflow

### Step 1: Scan governance files

Check these files for inconsistencies, outdated rules, or missing enforcement:
- `AGENTS.md` — protected constitution
- `rules/common/approval-gates.md` — approval gates
- `rules/content/` — content rules
- `WORKING-CONTEXT.md` — current sprint constraints

### Step 2: Scan shared state files

Check these files for schema drift, missing writers, or structural issues:
- `state/current-queue.json` — active pipeline queue
- `state/published-log.json` — published post record
- `state/harvester_gate.json` — harvester gate state
- `state/signal_log.jsonl` — signal log

### Step 3: Scan tools for dead code

Check these tools for unused imports, dead functions, or broken references:
- `tools/*.py` — all Python tools
- Look for `ImportError` patterns, unused constants, unreachable code

### Step 4: Scan skills for drift

Check skill files against actual tool behavior:
- `.agents/skills/*/SKILL.md` — runtime skills
- `skills/*/SKILL.md` — canonical skills
- Verify referenced file paths exist
- Verify referenced functions/tools are still available

### Step 5: Scan launchd agents

Check scheduled automation for health:
- `~/Library/LaunchAgents/com.road4ai.*.plist` — launchd plists
- Verify exit codes are 0
- Check for stale configurations

### Step 6: Compile findings

For each gap found, record:
- **ID**: sequential identifier (e.g., `#1`, `#2`)
- **Severity**: HIGH / MEDIUM / LOW
- **Category**: governance / infrastructure / operational
- **Description**: one-line summary
- **Evidence**: file paths, line numbers, or commit hashes
- **Recommended fix**: action to resolve
- **Status**: open / resolved / deferred

### Step 7: Write open-items document

Write findings to `.agents/open-items.md` with:
- Header with compilation date
- Summary count by severity
- Detailed items grouped by category
- Resolution tracking

### Step 8: Commit

```bash
git add .agents/open-items.md
git commit -m "system: compile open items checkpoint"
```

## Output Contract

Return:
- total gaps found
- breakdown by severity (HIGH/MEDIUM/LOW)
- breakdown by category (governance/infrastructure/operational)
- top 3 highest-priority items
- link to `.agents/open-items.md`

## Anti-Patterns

- Do not fix gaps during compilation — document only, fixes are separate work.
- Do not include subjective quality issues — focus on structural/operational gaps.
- Do not duplicate items already tracked in existing open-items documents.
- Do not modify governance files during the scan.

## Related Skills

- `content-pipeline`
- `hermes-checkpoint-patterns`
