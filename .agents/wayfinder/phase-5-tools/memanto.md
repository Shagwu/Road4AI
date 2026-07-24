## Question
Should Road4AI adopt Memanto semantic memory as a Hermes replacement or supplement?

## Type
grilling

## Status
resolved

## Resolution
Deferred. Hermes works at current scale (1-3 agents, human-in-the-loop). Memanto adds Docker dependency, which conflicts with Road4AI philosophy: habits before infrastructure. Revisit when 5+ concurrent autonomous agents or 1,000+ checkpoints make `git log --grep` unwieldy.

**Note:** This resolution was a one-line scheduling deferral from the Phase 5 groundwork lock, not a full evaluation. If Memanto comes back up, it deserves a fresh grilling pass — this ticket alone should not be treated as sufficient.
