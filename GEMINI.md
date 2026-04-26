## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)

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

### Content Skills (Road4AI)
- **social-content**: LinkedIn/Twitter post generation
- **content-strategy**: Road4AI content planning
- **copywriting**: Brand voice and messaging
