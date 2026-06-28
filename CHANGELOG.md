# Changelog

All notable changes to the Road4AI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-06-28

### Added
- **SkillOpt Integration**: Governed learning loop for optimizing selected Road4AI skills
- **Three-Model Benchmark Runner**: Target, evaluator, and optimizer models with cost tracking
- **Governance Boundary**: Protected files blocked from optimization (AGENTS.md, brand voice, operating contracts)
- **Human Review Gate**: Every proposed edit requires approval before application
- **Multi-Domain Orchestration Suite**: 12-case test suite for cross-domain interactions
- **Drift Monitoring Agent**: Real-time drift detection with green/yellow/blue tiering
- **Slack Notifications**: Alert integration for drift incidents (pending webhook approval)
- **Watch Mode**: Continuous drift monitoring on configurable intervals
- **Benchmark Collector**: Tool for collecting and labeling benchmark cases

### Validated
- **Social Voice Domain**: 0.950 baseline score, no optimization needed
- **Memory Ops Domain**: 0.915 baseline score, no optimization needed
- **QA Domain**: 0.803 baseline score, optimizer proposed 2 edits (applied)
- **Orchestration Suite**: 12/12 cases passing, zero API calls
- **Total Validation Cost**: $0.438 across all domains

### Governance
- Added orchestration rules to AGENTS.md (DO/ASK/NEVER for cross-domain operations)
- Confidence tiering: high (≥0.8) auto-stores, low (<0.8) queues for review
- Drift thresholds: ±5% alert, ±10% halt
- Sequential handoff pattern for v2.1 scope

### Tools
- `tools/skillopt_openai.py`: Cleaned up with social_voice defaults
- `tools/benchmark_collector.py`: New benchmark collection tool
- `tools/run_multi_domain_benchmark.py`: Orchestration suite runner
- `tools/drift_monitor.py`: Drift monitoring with CLI and watch mode

### Documentation
- Ground truth labeling guide with 30 cases across 3 domains
- Week 3 training run plan
- Week 6 blog post and release plan
- Drift monitoring spec (July 1-10 implementation)

## [2.0.0] - 2026-05-26

### Added
- **Hermes Memory Substrate**: Distributed vector storage with ChromaDB
- **Lifecycle Management**: TTL, automatic archiving, pruning
- **Self-Knowledge Index**: CLI-based retrieval with relevance scoring
- **Agent Roles**: Codex (planner), Claude Code (operator), Content Scout, Signal Harvester
- **Content Pipeline**: Queue-based content lifecycle (ideas → ready → approved → archived)
- **Platform Integration**: Blotato scheduling for LinkedIn, X, Instagram, Facebook, Threads, TikTok

### Changed
- Decoupled Hermes into standalone package
- Migrated to distributed vector storage
- Updated agent operating contract (AGENTS.md)
