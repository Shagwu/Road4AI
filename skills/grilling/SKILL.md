---
name: grilling
description: Interview the user relentlessly about a plan, decision, or tool evaluation until every branch is resolved, before it enters Hermes memory or goes to Karen for review. Use whenever the user is about to commit to a design, architecture change, or Phase 5 tool adoption, or uses any "grill" trigger phrase. This is the shared primitive behind /grill-me and /wayfinder — do not duplicate its logic elsewhere, invoke it.
disable-model-invocation: false
---

# Grilling (Road4AI primitive)

Interview the user relentlessly about whatever plan, decision, or tool evaluation is on the table, until nothing important is left silently assumed. This is the reusable loop other skills call into — `/grill-me` and `/wayfinder` both delegate here rather than re-implementing the interview.

## Rules

1. **Walk the decision tree, not a checklist.** Find the parent decision first, resolve it, then walk into whichever child branches it opens up. Do not ask questions out of order just because they occurred to you.

2. **One question at a time.** Ask, then stop and wait for the answer. A batch of questions is disorienting and defeats the purpose — the point is depth on each branch, not coverage of all branches at once.

3. **Always propose a recommended answer.** The user should be reacting to a draft, not staring at a blank prompt. If you have no informed guess, say so honestly rather than inventing false confidence.

4. **Check the repo before asking.** Before putting a question to the user, check whether it's answerable from `AGENTS.md`, `state.yaml`, `project.yaml`, `.agents/harvester/*.md`, or a recent Hermes checkpoint (`git log --grep "[hermes-context]"`). Only escalate to a real question if the answer requires human judgment — a values call, a tradeoff, a "which one do we actually want."

5. **The decisions are the user's.** You can argue for your recommendation, but don't quietly substitute your judgment for theirs. Put it to them and wait.

## Closing a grilling session

When every branch is resolved (or the user says stop), do not just summarize in chat and move on — persist it, the same way Hermes persists everything else:

1. Write a `[hermes-context]` checkpoint block capturing each resolved decision as a one-line entry (see `hermes-checkpoint` skill for the exact commit format).
2. If the decision touches public-facing claims, architecture, or governance (the kind of thing that would normally need a Karen pass), the session is NOT closed until Karen clears it. Run `adversarial-review-karen` on the grilling output before writing the checkpoint. If Karen flags issues, address them before closing. No exceptions.
3. If the grilling surfaced no real fog — everything was already decided — say so plainly and skip the ceremony. Not every plan needs a full interrogation.

## When NOT to use this

- Routine content pipeline scheduling (that's governed by the Struggle-ratio mandate and voice conventions already, not a design decision)
- Anything that's a single, obvious call with no real tradeoff — grilling a non-decision just wastes the user's time
