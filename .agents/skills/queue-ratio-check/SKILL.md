---
name: queue-ratio-check
description: Check the Struggle post ratio in the trailing-10 window, diagnose failures, and recommend or apply fixes. Use when the user asks about the ratio, runs a ratio check, or needs to fix a ratio failure.
origin: Road4AI
tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Queue Ratio Check

## When to Activate

- The user asks "what's the ratio?" or "check the struggle ratio"
- A ratio check fails and the user wants to fix it
- The user is about to schedule posts and wants to verify ratio compliance
- A weekly content planning session begins

Do not use this for content drafting, scheduling, or queue writes.

## The Mechanism

Road4AI maintains a 25-30% Struggle post ratio in the trailing-10 window (10 most recent posts by scheduled/published date). The ratio is a hard gate — scheduling is blocked until the ratio passes.

Two complementary guards exist:
1. `check_struggle_ratio.py` — checks trailing-window ratio (catches gradual drift)
2. `check_struggle_stall.py` — checks consecutive non-Struggle streaks (catches cliff breaks)

## Workflow

### Step 1: Run the ratio check

```bash
python3 tools/check_struggle_ratio.py
```

Exit code 0 = PASS, exit code 1 = FAIL.

### Step 2: Interpret the result

- **PASS (exit 0)**: Ratio is within 25-30% range. No action needed.
- **FAIL (exit 1)**: Ratio is below 25%. A Struggle post must be scheduled to restore compliance.

### Step 3: If FAIL, diagnose the failure

Run the stall detector to check for consecutive non-Struggle streaks:

```bash
python3 tools/check_struggle_stall.py
```

This catches cliff breaks (like the June 2 drought of 16 consecutive non-Struggle posts) that the ratio check alone wouldn't catch until the window filled.

### Step 4: If FAIL, recommend or apply fix

**Option A (recommended)**: Add a Struggle candidate to the queue and schedule it.

**Option B**: Reschedule an existing Struggle post to an earlier date to fill the window.

**Option C**: Wait for a Struggle post to naturally enter the window (only if the dip is transient and will self-correct within days).

### Step 5: Verify fix

Re-run `python3 tools/check_struggle_ratio.py` to confirm the fix worked.

## Output Contract

Return:
- current ratio (e.g., "3/10 = 30%")
- PASS/FAIL status
- stall detector results (if run)
- recommended action (if FAIL)
- verification result (after fix)

## Anti-Patterns

- Do not schedule non-Struggle posts when the ratio is failing.
- Do not ignore the stall detector — it catches failure modes the ratio check misses.
- Do not use calendar-day window — the ratio check uses post-based window (10 most recent posts by date).

## Related Skills

- `content-pipeline`
- `approve-and-schedule`
