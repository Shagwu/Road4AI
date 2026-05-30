# Hermes v2.1 SkillOpt — Project Scope

**Version:** v2.1  
**Status:** In execution  
**Owner:** Sharon (Shagwu)  
**Started:** 2026-05-29  

---

## What we are building

A benchmark-driven optimization loop that improves Road4AI agent skills (SKILL.md files)
without manual rewriting and without sacrificing Sharon's voice or safety constraints.

The loop: benchmark → propose patch → verify voice → human approves → commit.

---

## What is in scope

- SkillOpt governance boundary document
- Social voice benchmark (10-20 labeled cases)
- Benchmark runner tool (run_skillopt_benchmark.py)
- One dry-run validation
- One live controlled optimization
- v2.1 launch proof package (content + release notes)

---

## What is out of scope

- Automated skill commits without human approval (never)
- Optimizing AGENTS.md, state files, or brand docs (protected)
- Multi-skill batch optimization before single-skill validation is proven
- Any change to Hermes v2.0 core memory layer (separate project)

---

## Success definition

Hermes v2.1 ships when:
1. At least one skill is measurably improved by SkillOpt
2. Voice benchmark score does not regress
3. All safety gates held throughout
4. Public proof package is live on LinkedIn and X

---

## Constraints

- Zero external paid APIs during development
- All benchmark runs must be reproducible locally
- Human-in-the-loop at every skill mutation — no exceptions
