---
id: 2026-09-08-operator-nim-evidence-audit-li
title: Building the Read-Only Road4AI Operator
platform: LinkedIn
type: Behind-the-scenes
goal: Build in public
status: ready_for_publishing
priority: 1
karen_verdict: APPROVED
karen_date: 2026-09-05
visual_type: carousel
scheduled: true
---

**Blotato image prompt:**
Dark terminal slide. Left side shows an emerald green badge: "Role Separation: Audit vs Execute". Right side shows a timeline graphic with timestamps labeled "Temporal Evidence Rule: State must match event timestamp". Bold white text centered: "Two rules that stopped our operator agent from hallucinating state." Small emerald footer: "Road4AI Operator Engine".

---

Model deprecation is a routine engineering reality for agent systems.

Our previously configured local and cloud endpoints hit end of life last week. Instead of patching temporary endpoints, we rewired the Hermes memory substrate through NVIDIA NIM microservices to standardize our inference layer.

With inference stabilized, we built the next layer: the dedicated Road4AI Operator bot.

To ensure the operator could never drift or hallucinate system health, we hardened it against real evidence-audit benchmarks with two non-negotiable rules:

1. Strict Role Separation:
The operator is strictly read-only. It inspects Git context, verifies queue states, and checks audit manifests, but it has zero write permissions to operational state. The agent that audits the system cannot be the agent that mutates the constitution.

2. Temporal Evidence Enforcement:
An agent claim without a verified timestamped receipt is treated as an automatic failure. If the operator claims a post was scheduled or an audit passed, it must cite the exact provider receipt and log timestamp. No loose assumptions, no stale cache lookups.

Running these evidence checks surfaced every edge case where an LLM would normally invent a successful status.

When you remove the model's ability to edit its own report card and force it to prove claims with chronological receipts, reliability stops being a prompt trick and becomes a verifiable property of your system.
