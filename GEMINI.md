## Scope Restriction Mandate
- **Primary Root**: `/Users/shagwu/Downloads/Road4AI-main`
- **Constraint**: All file reads (`read_file`), searches (`grep_search`, `glob`), and directory listings (`list_directory`) MUST be strictly scoped to the Primary Root or its subdirectories.
- **Exclusion**: Ignore all files in the parent directory (`/Users/shagwu/`) or sibling directories unless they are explicitly passed as a tool input for a specific cross-project task.

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)

## Governance Protection
- `AGENTS.md` is the system's "constitution." NEVER allow an agent to mutate this file without explicit human confirmation. Any proposed contract changes must be flagged as an `Inquiry` first. 
- **Non-Delegable Authority**: The Orchestrator (Chief of Staff) is prohibited from delegating `AGENTS.md` mutation permissions to any other agent. The "Manual Approval Gate" is a top-level constraint that cannot be bypassed by agent-to-agent negotiation.

## Engineering Skills (Superpowers Framework)

The following skills enforce professional engineering methodology.
Load them via: activate_skill <skill-name>

### Core engineering mandates
- **tdd**: RED-GREEN-REFACTOR cycle. Always write the failing test first.
  Load when: writing any new feature, fixing any bug.

- **writing-plans**: PLAN.md before multi-file changes.
  Load when: any task touching more than one file.

- **using-git-worktrees**: Isolated workspaces for agent tasks.
  Load when: starting any HNSW or CrewAI integration work.

- **subagent-driven-development**: Delegate batch tasks to sub-agents.
  Load when: refactoring 3+ files or running parallel tasks.

- **requesting-code-review**: Two-stage review before merging.
  Load when: any feature is ready to commit to main.

## Context Engineering Architecture (KV-Cache Optimization)

### 1. Session-Init Sequence (Mandatory before work)
Every session must open with the following sequence to seal the prefix cache:
- **Step 1: Inject Constitution**: Read `AGENTS.md` in full via `ctx_batch_execute`. HALT if missing.
- **Step 2: Inject Brand Voice**: Read `docs/brand-voice.md` in full.
- **Step 3: Seal the Cache**: Mark `# -- CACHE_END --`. No further edits above this point.
- **Step 4: Confirm**: Log token counts to console to verify anchor weight.

### 2. Conflict Resolution Hierarchy
When dynamic state (`war-room-status.json`) and Hermes memory (`git log`) diverge, the following priority applies:
1. **Priority 1**: Hermes Checkpoint (Git log) - Most auditable.
2. **Priority 2**: `state/war-room-status.json` - Operational state.
3. **Priority 3**: `state/current-queue.json` - Task-level state.
**Rule**: If `war-room-status` is newer than the last Hermes checkpoint, HALT and write a catch-up checkpoint before proceeding.

### 3. Baseline Validation
Periodically run the Condition A vs Condition B experiment to verify the >80% cache hit rate. Record results in `state/cache-efficiency-log.jsonl`.

### Content Skills (Road4AI)
- **social-content**: LinkedIn/Twitter post generation
- **content-strategy**: Road4AI content planning
- **copywriting**: Brand voice and messaging
