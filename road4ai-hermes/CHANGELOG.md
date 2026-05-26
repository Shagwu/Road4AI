# Changelog

All notable changes to the `road4ai-hermes` project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-26

### Added
- Initial standalone release of the Hermes memory substrate.
- `MemoryBridgeV2`: Distributed vector storage backend using ChromaDB.
- `HermesStorage`: Native integration for CrewAI knowledge systems.
- Linear relevance scoring logic (`1.0 - sqrt(dist)`).
- Lifecycle management: TTL (Time-to-Live), automatic archiving, and idempotent pruning.
- Comprehensive test suite (16 tests) covering lifecycle, search, and conflicts.
- `adapter.py`: Capture-and-store utility for LLM conversations.
- `legacy.py`: Compatibility layer for Hermes V1 implementations.

### Changed
- Decoupled from the main Road4AI repository into a standalone modular package.
- Migrated internal imports to the `road4ai_hermes` namespace.
