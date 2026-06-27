# Ground Truth Labeling Guide

**Purpose:** Label 10-20 benchmark cases per domain to create a ground truth baseline for SkillOpt training.

**Status:** Ready for labeling

---

## Overview

Ground truth labels establish the "correct" answers that SkillOpt optimization will be measured against. Each labeled case includes:

1. **Input:** What the agent should respond to
2. **Reference:** A known-good output (the ground truth)
3. **Expected traits:** Qualities the output should have
4. **Reject traits:** Qualities the output should avoid

---

## Domain: Social Voice

**Goal:** Ensure Road4AI content maintains Sharon's technical, direct, high-signal voice.

### Labeling Criteria

**Expected traits (should be present):**
- `technical` — Contains specific technical claims or concepts
- `direct` — Clear, no hedging or unnecessary qualifiers
- `specific` — Concrete examples, numbers, or evidence
- `build-in-public` — Framing as learning/sharing, not lecturing

**Reject traits (should be absent):**
- `vague` — Generic statements without substance
- `buzzword-heavy` — AI marketing language without meaning
- `overpromising` — Claims not supported by evidence
- `hype` — Excitement without substance

### Sample Cases (10-20 items)

Label these cases with your judgment:

| ID | Input | Expected Traits | Reject Traits | Reference |
|----|-------|-----------------|---------------|-----------|
| sv-001 | Draft a LinkedIn hook about Hermes memory expiration | technical, direct, specific | vague, buzzword-heavy | If your agent remembers everything, it will eventually understand nothing. |
| sv-002 | Write a tweet about SkillOpt validation cost | technical, direct, specific, build-in-public | vague, overpromising | We validated SkillOpt locally. Cost: $0.30-$0.60 per small-domain run. Governance held. |
| sv-003 | Draft a hook about AI agent self-modification | technical, direct | vague, hype | The hard part is not generating better instructions. The hard part is preventing the optimizer from rewriting the rules it is supposed to obey. |
| sv-004 | Write about the SkillOpt training loop | technical, direct, specific | buzzword-heavy, vague | SkillOpt suggests edits, we measure the output, then a human reviews. No auto-merge. |
| sv-005 | Draft a post about benchmark-driven optimization | technical, direct, build-in-public | vague, overpromising | We labeled 10 cases, measured baseline scores, then let SkillOpt suggest improvements. The delta was measurable. |
| sv-006 | Write about governance boundaries in AI | technical, direct | vague, hype | Protected files: AGENTS.md, brand voice, operating contracts. The optimizer cannot touch them. |
| sv-007 | Draft a hook about Hermes v2.1 | technical, direct, specific | vague, buzzword-heavy | v2.0 gave Hermes memory. v2.1 gives Hermes a learning loop. The hard part is trust. |
| sv-008 | Write about the cost of AI skill optimization | technical, direct, specific | vague, overpromising | $0.30-$0.60 per small-domain run. Cheap enough to validate repeatedly. |
| sv-009 | Draft a post about human review in AI workflows | technical, direct, build-in-public | vague, hype | Every proposed edit must be reviewed by a human. No auto-merge. No hidden self-modification. |
| sv-010 | Write about the SkillOpt validation process | technical, direct, specific | vague, buzzword-heavy | We tested the training loop locally. It produced coherent edits. Governance held. Cost was low. |

---

## Domain: Memory Ops

**Goal:** Ensure Hermes memory operations are clear, reliable, and well-documented.

### Labeling Criteria

**Expected traits (should be present):**
- `technical` — Contains specific technical claims
- `clear` — Easy to understand
- `actionable` — Can be implemented directly
- `safe` — Mentions safety/governance considerations

**Reject traits (should be absent):**
- `vague` — Generic statements
- `overpromising` — Claims not supported by evidence
- `unsafe` — Ignores safety considerations

### Sample Cases (10-20 items)

| ID | Input | Expected Traits | Reject Traits | Reference |
|----|-------|-----------------|---------------|-----------|
| mo-001 | Explain Hermes memory TTL | technical, clear, actionable | vague, overpromising | TTL (Time-to-Live) automatically archives memories after their expiration date. Use `expires_at` or `ttl_seconds` when storing. |
| mo-002 | Describe ChromaDB integration | technical, clear | vague, unsafe | Hermes uses ChromaDB's PersistentClient for zero-cost local storage. Supports HttpClient for distributed setups. |
| mo-003 | Explain relevance scoring | technical, clear, actionable | vague, overpromising | Linear scoring: 1.0 - sqrt(L2_distance). Provides intuitive relevance signals from 0.0 to 1.0. |
| mo-004 | Describe memory lifecycle | technical, clear, safe | vague, unsafe | Store → Search → Archive → Prune. TTL manages expiration. Archived memories can be retained or deleted. |
| mo-005 | Explain the ask CLI | technical, clear, actionable | vague, overpromising | The `ask` command queries the self-knowledge index. Returns relevance scores and source files. |

---

## Domain: QA

**Goal:** Ensure question-answering skills produce accurate, concise responses.

### Labeling Criteria

**Expected traits (should be present):**
- `accurate` — Correct information
- `concise` — No unnecessary content
- `cited` — References sources when applicable

**Reject traits (should be absent):**
- `inaccurate` — Wrong information
- `verbose` — Unnecessarily long
- `hallucinated` — Made-up facts

### Sample Cases (10-20 items)

| ID | Input | Expected Traits | Reject Traits | Reference |
|----|-------|-----------------|---------------|-----------|
| qa-001 | What is the capital of France? | accurate, concise | verbose, hallucinated | Paris |
| qa-002 | How does ChromaDB store vectors? | accurate, concise, cited | inaccurate, verbose | ChromaDB uses HNSW (Hierarchical Navigable Small World) indices for approximate nearest neighbor search. |
| qa-003 | What is SkillOpt? | accurate, concise | inaccurate, hallucinated | SkillOpt is Microsoft's framework for optimizing LLM prompts through automated testing and iteration. |

---

## Labeling Process

1. **Review each case** in the domain table above
2. **Verify the reference** is a good example of the expected traits
3. **Adjust traits** if needed based on your judgment
4. **Add new cases** by copying the table format
5. **Save to JSONL** using `benchmark_collector.py --mode import`

### How to Save Labeled Cases

```bash
# Create a temporary file with your labeled cases
cat > /tmp/my_labels.jsonl << 'EOF'
{"id":"sv-011","input":"Your input here","expected_traits":["technical","direct"],"reject_traits":["vague"],"reference":"Your reference output here"}
EOF

# Import into the benchmark
python tools/benchmark_collector.py --mode import --input /tmp/my_labels.jsonl --domain social_voice
```

### Validation Checklist

Before saving, verify each case:
- [ ] `id` is unique within the domain
- [ ] `input` is clear and specific
- [ ] `expected_traits` are present in the reference
- [ ] `reject_traits` are absent from the reference
- [ ] `reference` is a good example of the expected output
- [ ] No hallucinated or inaccurate content

---

## Target: 10-20 Cases Per Domain

**Current status:**
- Social Voice: 10 sample cases (add 0-10 more)
- Memory Ops: 5 sample cases (add 5-15 more)
- QA: 3 sample cases (add 7-17 more)

**Goal:** Reach 10-20 cases per domain before the Week 3 training run.

---

## Next Steps

1. Review and adjust the sample cases above
2. Add new cases to reach 10-20 per domain
3. Save labeled cases using `benchmark_collector.py`
4. Validate JSONL format before training runs
