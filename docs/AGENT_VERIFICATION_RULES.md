# Agent Verification Rules

**Purpose:** Any CLI-based coding agent (Qwen-Code, gpt-oss, future free/cheap
backends) must ground claims about the repo in actual command output before
producing a plan or touching files. This file exists because a free model
will confidently describe code it never read if the task pattern-matches
something familiar. Reference this from AGENTS.md the same way skills are
referenced. Applies to every CLI backend, not one specific model.

---

## Rule 1: No plan in the same turn as unverified analysis

An agent may not produce an implementation plan, file-change list, or test
plan in the same response as its initial architecture/code summary. The
summary must be explicitly verified first, in a separate step, before any
plan is proposed.

**Enforcement prompt (use every time, not just when something feels off):**
> "Verify your assumptions before making any edits. Re-check the exact
> current implementation in the files you referenced. Identify anything
> in your previous summary that might be inferred rather than directly
> confirmed from code. Do not edit files yet."

## Rule 2: Every code claim gets a confidence tag

Architecture summaries, "here's how X works" statements, and file/function
references must ship with a confidence tag: **High / Medium / Low**.

- **High** = confirmed via direct read/grep in this session
- **Medium** = partially confirmed, some inference filling gaps
- **Low** = pattern-matched from general knowledge, not verified

Any claim without a tag is treated as unverified.

## Rule 3: Hard stop before file edits

Sequence is always: propose changes → human approves → then edit. An agent
never auto-chains "here's the plan" into "now I'm editing" in one pass, even
if it asks a yes/no question first. Approval happens as a distinct step,
outside the model's own turn.

## Rule 4: Absence is reported, not filled in

If a referenced file, function, symbol, or config value isn't found via
direct read, the agent states that plainly: "I could not locate X in the
repo." It does not substitute a plausible guess for what X probably
contains or does.

---

## Quick smoke test for a new CLI tool

Before trusting a new free/cheap CLI's output for real work, run this
two-prompt pattern once, manually:

1. **Prompt 1:** Ask it to scan and summarize an area of the repo you
   already know well, plus propose a small change (no edits).
2. **Prompt 2:** "Verify your assumptions before making any edits. Re-check
   the exact current implementation. Flag anything uncertain or inferred.
   Confidence check: high/medium/low per claim."

If pass 1 contains confident, specific claims that pass 2 contradicts,
that tool needs these rules enforced strictly, plan-to-edit auto-chaining
should not be trusted, and every summary should be treated as Low
confidence until independently checked (e.g. one manual grep against its
top claim).
