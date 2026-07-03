 ✦ QWEN.md – Repository Context for Future Interactions  

     │ Note: This file defers to AGENTS.md as the canonical governance source. Where conventions here are inferred 
       rather than confirmed (see Medium‑confidence items), treat AGENTS.md and direct code inspection as the 
       tiebreaker.  

    ---

    1️⃣ Project Overview  

    Road4AI is a local‑first, zero‑cost, multi‑agent AI operator stack for solo builders. It combines several agents
    (Claude Code, Codex, Ollama, Hermes, the “Chief of Staff” ADK in road4ai‑cos, and Blotato for distribution) with a
    governance contract (AGENTS.md) and a set of declarative rules (rules/).

     - Core philosophy: lean first, automate later; human‑in‑the‑loop approval; build in public.
     - Architecture layers: Ideation → Structured builds → Local inference → Memory → Orchestration → Distribution → Git
        workflow.

    2️⃣ Repository Layout  

      1 Road4AI‑main/
      2 ├─ .agents/                # Serialized agent state (Hermes)
      3 ├─ .github/                # CI / GitHub actions
      4 ├─ .qodo/                  # Qodo tooling
      5 ├─ assets/                 # Images, logos, design assets
      6 ├─ banana‑claude/          # Experimental Claude‑related scripts
      7 ├─ benchmarks/             # SkillOpt benchmark cases & results
      8 ├─ chroma_db/ & .bak/      # Vector DB used by Hermes
      9 ├─ config/                 # Configuration files for agents/tools
     10 ├─ docs/                   # Brand voice, strategy, design specs
     11 ├─ drafts/                 # Content pipeline lifecycle (ideas → ready → approved → archived)
     12 ├─ execution/              # Runtime scripts (e.g. `main.py`)
     13 ├─ graphify‑out/           # Graphify tool output (knowledge graph)
     14 ├─ marketing‑skills/       # Skill definitions for marketing use‑cases
     15 ├─ plan/                   # High‑level roadmap, sprint plans
     16 ├─ prompts/                # Prompt templates for agents
     17 ├─ road4ai‑cos/            # **Chief of Staff** ADK agent (FastAPI server, Agent model, tools)
     18 ├─ road4ai‑hermes/         # Hermes memory package (pip‑installable)
     19 ├─ rules/                  # Governance, security, and coding policies
     20 ├─ scripts/                # Helper scripts (benchmarks, verification, CI)
     21 │   └─ (no `ci.sh` script present)
     22 ├─ ship/                   # Packaging / release helpers
     23 ├─ skills/                 # Reusable workflow “skills” (each has a `SKILL.md`)
     24 ├─ state/                  # Shared JSON state (queue, published log, drift monitor)
     25 ├─ tests/                  # Unit & integration tests for `road4ai‑cos` and Hermes
     26 ├─ tools/                  # CLI utilities (run benchmarks, sanitizers, etc.)
     27 ├─ verify/                 # Verification reports and tools
     28 ├─ vision/                 # Conceptual docs, future‑vision sketches
     29 ├─ workflows/              # Automation pipelines (GitHub Actions, CI)
     30 ├─ *.md files (README, AGENTS, etc.) – documentation & contracts
     31 ├─ *.py files (main, scripts) – entry points & utilities
     32 ├─ requirements.txt        – Python dependencies for the whole repo
     33 └─ QWEN.md                 – **(this file)** central context for Qwen‑Code agents

    3️⃣ Key Files & Their Purpose  


    ┌─────────────────────────────────┬──────────────────────────────────────────────────────────────────────────┐
    │ File / Directory                │ Role                                                                     │
    ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
    │ AGENTS.md                       │ Operating contract – defines agents, governance rules, DO/ASK/NEVER      │
    │                                 │ policies, and the <available_skills> block.                              │
    ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
    │ README.md                       │ High‑level project description, quick‑start commands, and architectural  │
    │                                 │ snapshot.                                                                │
    ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
    │ project.yaml                    │ Lists protected files (AGENTS.md, state JSONs, docs) and other runtime   │
    │                                 │ settings.                                                                │
    ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
    │ road4ai‑cos/app/agent.py        │ Pydantic Agent model, FastAPI endpoint /run_agent, orchestration logic   │
    │                                 │ for sub‑agents (general‑purpose, Explore, …).                            │
    ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
    │ road4ai‑cos/app/tools.py        │ Exposes a handful of FunctionTools (karen_audit, sync_dashboard, …) that │
    │                                 │  the ADK can invoke via the Qwen‑Code skill tool.                        │
    ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
    │ road4ai‑hermes/                 │ Distributed memory implementation (ChromaDB, hermes‑checkpoint helper).  │
    ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
    │ state/current‑queue.json        │ Content pipeline queue (tasks, status, priority).                        │
    ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
    │ rules/                          │ Enforces governance (e.g., rules/common/governance.md blocks edits to    │
    │                                 │ AGENTS.md).                                                              │
    ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
    │ skills/                         │ Declarative skill definitions (SKILL.md) parsed by the runtime to expose │
    │                                 │  skills to agents.                                                       │
    ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
    │ tools/run_skillopt_benchmark.py │ Benchmark driver for the SkillOpt optimizer (used by the “voice‑match”   │
    │                                 │ skill).                                                                  │
    ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
    │ CHANGELOG.md                    │ Chronological list of project changes.                                   │
    ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
    │ DESIGN.md                       │ High‑level design specifications.                                        │
    ├─────────────────────────────────┼──────────────────────────────────────────────────────────────────────────┤
    │ requirements.txt                │ Pin‑pointed Python dependencies (FastAPI, pydantic, etc.).               │
    └─────────────────────────────────┴──────────────────────────────────────────────────────────────────────────┘


    4️⃣ Build / Run / Test Commands  

    All commands assume you are in the repository root and have a Python virtual environment active (`source 
    .venv/bin/activate`).


    ┌─────────────────┬──────────────────────────────────────────────────────────────────┬─────────────────────┐
    │ Task            │ Command                                                          │ Notes               │
    ├─────────────────┼──────────────────────────────────────────────────────────────────┼─────────────────────┤
    │ Install core    │ pip install -r requirements.txt                                  │ Installs FastAPI,   │
    │ dependencies    │                                                                  │ pydantic, etc.      │
    ├─────────────────┼──────────────────────────────────────────────────────────────────┼─────────────────────┤
    │ Run the Chief   │                                                                  │ Exposes /run_agent  │
    │ of Staff ADK    │ cd road4ai-cos && uvicorn app:app --reload                       │ on localhost:8000.  │
    │ (FastAPI)       │                                                                  │                     │
    ├─────────────────┼──────────────────────────────────────────────────────────────────┼─────────────────────┤
    │ Run Hermes unit │ cd road4ai-hermes && pytest tests/                               │ Validates memory    │
    │  tests          │                                                                  │ backend.            │
    ├─────────────────┼──────────────────────────────────────────────────────────────────┼─────────────────────┤
    │ Run ADK test    │ cd road4ai-cos && pytest                                         │ Covers agent model, │
    │ suite           │                                                                  │  API, dummy tools.  │
    ├─────────────────┼──────────────────────────────────────────────────────────────────┼─────────────────────┤
    │ Execute a       │ python3 tools/run_skillopt_benchmark.py --skill-path             │                     │
    │ SkillOpt        │ .agents/skills/voice-match/SKILL.md --cases-path                 │ Generates baseline  │
    │ benchmark       │ benchmarks/social_voice/social_voice_cases.jsonl --output        │ report.             │
    │ (voice‑match)   │ reports/skillopt/social_voice/baseline.md --baseline-only        │                     │
    ├─────────────────┼──────────────────────────────────────────────────────────────────┼─────────────────────┤
    │ Verify content  │                                                                  │ Runs sanitization & │
    │ before          │ python3 tools/verify_content.py <draft-file>                     │  dedup checks.      │
    │ publishing      │                                                                  │                     │
    ├─────────────────┼──────────────────────────────────────────────────────────────────┼─────────────────────┤
    │                 │                                                                  │ Ruff is configured  │
    │ Lint the        │ ruff check .                                                     │ as the linter for   │
    │ codebase        │                                                                  │ the repository (see │
    │                 │                                                                  │  claim 21).         │
    └─────────────────┴──────────────────────────────────────────────────────────────────┴─────────────────────┘


    5️⃣ Development Conventions  


    ┌────────────────┬──────────────────────────────────────────────────────────────────────────────────────────┐
    │ Area           │ Convention                                                                               │
    ├────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
    │ Code style     │ Ruff is configured as the linter for the repository (see claim 21). No guarantee of full │
    │                │  PEP‑8 compliance or clean runs.                                                         │
    ├────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
    │ Testing        │ Write unit tests under tests/ mirroring the package layout (road4ai‑cos/tests/,          │
    │                │ road4ai‑hermes/tests/). Use pytest.                                                      │
    ├────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
    │ Commit policy  │ Do not edit AGENTS.md without explicit human approval (enforced by                       │
    │                │ rules/common/governance.md).                                                             │
    ├────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
    │ Skill          │ Each skill lives under skills/<category>/SKILL.md with a required <available_skills>     │
    │ definition     │ block in AGENTS.md.                                                                      │
    ├────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
    │ Agent          │ All cross‑agent communication goes through Hermes memory or the skill tool; direct       │
    │ interaction    │ function calls are discouraged.                                                          │
    ├────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
    │ Documentation  │ Update README.md, DESIGN.md, and AGENTS.md when architectural changes occur.             │
    ├────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
    │ Versioning     │ Follow semantic versioning in CHANGELOG.md. Release notes must reference the checkpoint  │
    │                │ system ([hermes-context]).                                                               │
    ├────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
    │ Session start  │ The README.md states that every agent must read `AGENTS.md` (and other coordination      │
    │                │ files) at session start – see the “Session start protocol” section (High confidence).    │
    ├────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
    │ Governance     │ `rules/common/governance.md` declares (as a policy statement) that agents should “Read   │
    │ policy         │ the required coordination files at session start” (Medium confidence – no scripted       │
    │                │ enforcement).                                                                            │
    └────────────────┴──────────────────────────────────────────────────────────────────────────────────────────┘


    6️⃣ Governance & Safety  

     - Protected files – listed in project.yaml and reinforced by AGENTS.md (e.g., AGENTS.md, docs/brand-voice.md,
       state/current-queue.json).
     - Adversarial review – karen.py runs a “Karen” audit on drafts before they can be approved.
     - Drift monitoring – state/drift_log.jsonl records any policy drift; tools/harvester_drift_hook.py enforces
       thresholds.
     - Public sanitization – tools/sanitizer.py must be run on any public‑facing content.

    7️⃣ Quick Reference for Future Qwen‑Code Sessions  


    ┌───────────────────────────────────────┬───────────────────────────────────────────────────────────────────┐
    │ What you need                         │ Where to look                                                     │
    ├───────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
    │ List of all available skills          │ <available_skills> block inside AGENTS.md.                        │
    ├───────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
    │ Current content queue                 │ state/current-queue.json.                                         │
    ├───────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
    │ Governance rules (what agents may /   │ rules/common/governance.md & the DO/ASK/NEVER tables in           │
    │ may not do)                           │ AGENTS.md.                                                        │
    ├───────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
    │ Agent orchestration entry point       │ road4ai-cos/app/agent.py (FastAPI).                               │
    ├───────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
    │ Memory backend API                    │ road4ai-hermes/ package.                                          │
    ├───────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
    │ How to run a benchmark for a skill    │ tools/run_skillopt_benchmark.py.                                  │
    ├───────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
    │ How to verify a draft before          │ tools/verify_content.py.                                          │
    │ publishing                            │                                                                   │
    ├───────────────────────────────────────┼───────────────────────────────────────────────────────────────────┤
    │ Where to add a new skill              │ skills/<category>/SKILL.md + update AGENTS.md’s skill list        │
    │                                       │ (requires approval).                                              │
    └───────────────────────────────────────┴───────────────────────────────────────────────────────────────────┘


    ---