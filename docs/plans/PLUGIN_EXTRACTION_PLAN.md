# Plugin Extraction Plan: `road4ai-hermes`

**Goal:** Extract `MemoryBridgeV2` and `HermesStorage` into a standalone, installable Python package to enable the Road4AI "Ecosystem Shift."

## 🏗️ Target Architecture

The new package will be named `road4ai-hermes`. It will contain:
- `MemoryBridgeV2`: The core distributed memory substrate.
- `HermesStorage`: The CrewAI knowledge storage integration.
- Standardized lifecycle management (TTL, archiving, pruning).

## 📋 Extraction Steps

### 1. Repository Structure
Create a new directory structure for the standalone package:
```text
road4ai-hermes/
├── pyproject.toml          # Dependency and build management
├── README.md               # Package-specific docs
├── src/
│   └── road4ai_hermes/
│       ├── __init__.py
│       ├── bridge.py       # (Formerly bridge_v2.py)
│       └── crewai.py       # (Formerly crewai_storage.py)
└── tests/
    ├── test_bridge.py
    └── test_crewai.py
```

### 2. Dependency Management (`pyproject.toml`)
Define the core requirements for the plugin:
- `chromadb>=0.4.0`
- `numpy`
- `pydantic`
- `sentence-transformers` (optional/extra for local embedding support)

### 3. Source Migration
- Move `hermes/bridge_v2.py` to `src/road4ai_hermes/bridge.py`.
- Move `hermes/crewai_storage.py` to `src/road4ai_hermes/crewai.py`.
- Update internal imports to use the new package namespace.

### 4. Integration Strategy (The "Bridge")
Once the package is extracted:
1. Publish to PyPI (or install via git URL for early testing).
2. Remove the `hermes/` directory from the main `Road4AI` repo.
3. Add `road4ai-hermes` to `requirements.txt`.
4. Update all imports in the main repo:
   - `from hermes.bridge_v2 import MemoryBridgeV2` → `from road4ai_hermes.bridge import MemoryBridgeV2`

## 🚀 Execution Timeline (Week 5)

- **Phase 1: Scaffolding:** Create `pyproject.toml` and basic structure in a separate branch.
- **Phase 2: Test Migration:** Port all existing tests in `hermes/tests/` to the new package and verify they pass.
- **Phase 3: Cleanup:** Remove local `hermes/` folder and update main project dependencies.
- **Phase 4: Release:** Draft initial release notes and "Ecosystem Shift" announcement.

## ⚖️ Integrity & Safety
- **TDD:** No code moves without its corresponding test.
- **Compatibility:** Maintain V1 aliases during the transition to prevent breaking existing operator workflows.

---
© 2026 Road4AI. Built, not just prompted. 🔧