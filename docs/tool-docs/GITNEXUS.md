# GitNexus Tool Documentation

## Overview
GitNexus is the primary tool for codebase analysis, architectural mapping, and knowledge graph generation in the Road4AI project. It builds a multi-layered graph of the repository, including AST data, dependency flows, and semantic relationships.

## Key Capabilities
- **Knowledge Graphing:** Generates `graph.json` and `graph.html` in `graphify-out/`.
- **Code Search:** Powering the `cavecrew-investigator` subagent to locate specific symbols or patterns.
- **Architectural Mapping:** Identifies "god nodes" and community clusters via `GRAPH_REPORT.md`.

## Integration with Road4AI
- Before any major architectural change, Claude Code or Codex reads `graphify-out/GRAPH_REPORT.md`.
- After modifications, run `graphify update .` to keep the graph synced.

## Troubleshooting
- If the graph is stale, run `graphify clean && graphify analyze .`.
- If indexing fails, check for circular dependencies in Python imports using `graphify detect-cycles`.
