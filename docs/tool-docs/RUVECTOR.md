# RuVector Tool Documentation

## Overview
RuVector is the intelligent routing and vector similarity engine for Road4AI. It uses hyperbolic embeddings (Poincaré ball) to map relationships between concepts, code patterns, and tasks.

## Key Capabilities
- **Semantic Routing:** Directs tasks to the optimal agent or model based on task embedding.
- **Similarity Search:** Finds related code snippets or past content ideas in the `reasoning-bank`.
- **HNSW Acceleration:** High-speed vector lookup using the RaBitQ quantized index.

## Integration with Road4AI
- **Reflexion Memory:** RuVector powers the episodic replay system, allowing agents to "remember" successful trajectories.
- **MoE Routing:** Classifies user intent and routes it through the specialized agent swarm.

## Usage
- Controlled via the `mcp-ruflo` extension tools.
- Models are initialized with hyperbolic curvature to better represent hierarchical data structures.
