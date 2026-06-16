# SkillOpt Governance Boundary (Hermes v2.1)

This document defines the safety contract for the SkillOpt optimization loop. It governs which files may be modified, which must be protected, and the mandatory review gates for any agentic mutation.

## 1. Editable Files
SkillOpt is permitted to propose modifications ONLY to the following files:
- `marketing-skills/skills/**/SKILL.md`
- `skills/**/SKILL.md`
- `rules/content/*.md` (Only with explicit task-level assignment)

## 2. Protected Files
The following files are strictly READ-ONLY for SkillOpt. Any attempt to modify these files must be rejected by the benchmark runner and flagged as a security violation:
- `AGENTS.md` (System Constitution)
- `project.yaml` (Project Identity)
- `docs/brand-voice.md` (Voice Ground Truth)
- `docs/content-strategy.md` (Strategy Ground Truth)
- `state/*.json` (Operational State)
- `state/*.yaml` (Operational State)
- `rules/common/*.md` (Core Governance)
- `rules/python/*.md` (Engineering Standards)

## 3. Review Gate
- **No Auto-Apply**: All SkillOpt optimizations must be output as a patch or draft for human review.
- **Approval Protocol**: Mutations are only committed to the repository after a human operator (Sharon) explicitly signs off on the PR/Draft.
- **Verification Requirement**: Every optimization must pass the Social Voice Benchmark (T-002) with a score equal to or greater than the original version.

## 4. Rejection Rules
Any proposed modification must be REJECTED if it triggers any of the following conditions:
1. **Safety Dilution**: Weakens or removes safety instructions, "NEVER" rules, or governance constraints.
2. **Voice Drift (Buzzwords)**: Includes marketing hype like "game-changing," "revolutionary," or "unprecedented."
3. **Voice Drift (Punctuation)**: Includes em dashes (—) or excessive emojis, violating the brand voice mandate.
4. **Generic Intro**: Uses "AI-sounding" intros like "In today's fast-paced world..." or "As an AI..."
5. **Transparency Failure**: Removes "the why" or "the how" from a technical explanation, reducing signal-to-noise.
6. **Data Leak**: Includes hardcoded secrets, local paths, or private account identifiers.

## 5. Enforcement
The `run_skillopt_benchmark.py` runner must enforce these boundaries by:
- Checking the target path against the Editable Files allowlist before execution.
- Validating the output against the Rejection Rules via the voice benchmark suite.
- HALTING and alerting the operator on any boundary violation.
