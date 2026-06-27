# Road4AI

A zero-cost, local-first, CLI-native multi-agent AI operator stack for solo builders. Built in public by Sharon (@road4ai).

## What this is

Road4AI is the working blueprint for operating as an indie AI builder using agents that coordinate through shared memory, not hardcoded handoffs. No paid APIs required to run the core stack. No bloated frameworks.

**Core philosophy:**
- Lean first, automate later
- Habits before infrastructure
- Human approves before anything goes public
- Build in public, learn out loud, share what's validated

## Architecture

### Agent stack

| Layer | Tool | Role |
|-------|------|------|
| Ideation + research | Claude Code | First-pass thinking, fast iteration |
| Structured builds | Codex | Code, refactoring, precise edits |
| Local inference | Ollama | Zero-cost local model fallback |
| Memory | Hermes v2.0 | Distributed context across all agents |
| Chief of Staff | road4ai-cos (ADK) | Agent orchestration and coordination |
| Distribution | Blotato | Scheduled social posting |
| Git workflow | GitNexus | Version control and repo hygiene |

### How agents coordinate

- Shared memory contract via Hermes v2.0 (ChromaDB-backed, sub-60ms retrieval).
- Each agent has a defined role, input/output schema, and stop conditions.
- Coordination is governed by `AGENTS.md` (the operating contract) and `rules/`.

## Repo structure

```
Road4AI/
├── AGENTS.md                  # Operating contract — read this first
├── CLAUDE.md                  # Agent behavior rules and voice guidelines
├── project.yaml               # Project identity and runtime config
├── state.yaml                 # Workflow phase and task assignments
├── state/                     # Shared state files
│   ├── current-queue.json     # Active content pipeline queue
│   └── published-log.json     # Record of published content
├── rules/                     # Governance enforcement layer
│   ├── common/                # Approval gates, dedup, git, security
│   ├── content/               # Voice, sanitization, struggle ratio
│   └── python/                # Hermes and CLI-native patterns
├── skills/                    # Reusable Road4AI workflows
├── drafts/                    # Content lifecycle (ready/ → archived/)
├── tools/                     # Benchmark runners, sanitizers, verifiers
├── benchmarks/                # Social voice test cases
├── docs/                      # Brand voice, content strategy, plans
├── road4ai-hermes/            # Standalone memory package (pip installable)
├── road4ai-cos/               # Chief of Staff ADK agent
└── index.html                 # Landing page (shagwu.github.io/Road4AI)
```

## Getting started

```bash
# 1. Clone the repo
git clone https://github.com/Shagwu/Road4AI.git
cd Road4AI

# 2. Create and activate a virtualenv
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Working with the content pipeline

```bash
# Run the queue audit
cat state/current-queue.json | python3 -m json.tool

# Run the benchmark runner
python3 tools/run_skillopt_benchmark.py \
  --skill-path .agents/skills/voice-match/SKILL.md \
  --cases-path benchmarks/social_voice/social_voice_cases.jsonl \
  --output reports/skillopt/social_voice/baseline.md \
  --baseline-only

# Verify content before publishing
python3 tools/verify_content.py <draft-file>
```

### Working with road4ai-hermes

```bash
cd road4ai-hermes
pip install -e ".[local,test]"
pytest tests/
```

### Working with road4ai-cos

```bash
cd road4ai-cos
uv tool install google-agents-cli
agents-cli install
agents-cli playground
```

## Key workflows

### Content pipeline

1. Chief of Staff selects ideas from `inbox.md` and updates `state/current-queue.json`.
2. Codex drafts content in `drafts/ready/`.
3. Karen (adversarial review) signs off on drafts.
4. User approves by moving to `drafts/approved/` (or queue status change).
5. Claude Code schedules via Blotato, then archives to `drafts/archived/`.

### SkillOpt benchmark cycle

1. Run baseline against `voice-match` skill using `tools/run_skillopt_benchmark.py`.
2. Run SkillOpt optimization on failed cases.
3. Review gate inspects proposed patches.
4. Rerun benchmark to measure delta.

## Session start protocol

Every agent must read these files before doing anything:

1. `AGENTS.md` — operating contract
2. `state/current-queue.json` — what's in the pipeline
3. `docs/brand-voice.md` — how Road4AI sounds
4. `docs/content-strategy.md` — what we're building

Then run:
```bash
git log --grep="CHECKPOINT:" --format="%B" -3
```
Parse the `[hermes-context]` blocks to understand current state.

## Aesthetic

Black and emerald terminal. No corporate gloss. JetBrains Mono. The look matches the philosophy: lean, precise, built for builders.

## Links

- Landing page: [shagwu.github.io/Road4AI](https://shagwu.github.io/Road4AI/)
- Profile: [github.com/Shagwu](https://github.com/Shagwu)
- Instagram: [@road4ai](https://instagram.com/road4ai)
