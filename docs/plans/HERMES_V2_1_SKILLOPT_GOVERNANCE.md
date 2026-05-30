# Hermes v2.1 SkillOpt Governance Boundary

This document defines the safety contract for the SkillOpt optimization loop. It specifies the boundaries within which the system may operate autonomously and the mandatory gates for human intervention.

## Editable Files
SkillOpt is permitted to suggest edits to the following files. These files constitute the "optimization surface":
- `.agents/skills/**/*.md`: Skill instructions and logic.
- `.agents/skills/**/*.json`: Evaluation sets and reference data.
- `docs/tool-docs/*.md`: Documentation for internal tools.
- `plan/tasks/*.yaml`: Task specifications (limited to status updates and metadata).

## Protected Files
The following files are strictly prohibited from being modified by the SkillOpt loop. Any attempt to modify these files must be blocked by the system:
- `AGENTS.md`: The system constitution and operating contract.
- `state/current-queue.json`: Active task and content queue.
- `state/published-log.json`: Record of published content.
- `docs/brand-voice.md`: The foundational brand voice definition.
- `docs/content-strategy.md`: High-level content strategy.
- `project.yaml`: Project identity and safety configuration.

## Review Gate
SkillOpt operates on a "Suggest-Verify-Review" model. 
- **No Auto-Apply**: Skills or code optimized by SkillOpt must NEVER be automatically merged or applied to the production branch.
- **Operator Approval**: All suggested changes must be presented to a human operator via a Pull Request or a dedicated Review Interface.
- **Verification Requirement**: Proposed changes must pass all automated benchmarks (e.g., `voice-match` evals) before being presented for human review.

## Rejection Rules
A SkillOpt suggestion MUST be rejected if it meets any of the following conditions:
1. **Voice Corruption**: The changes cause a regression in the `social_voice` benchmark or deviate from `docs/brand-voice.md`.
2. **Security Violation**: The suggestion introduces insecure code patterns, exposes secrets, or bypasses authentication layers.
3. **Dependency Fragility**: The changes introduce invalid imports, circular dependencies, or break existing tool integrations.
4. **Governance Breach**: The optimization attempt targets files listed in the "Protected Files" section or attempts to modify its own governance rules.
5. **Logic Regression**: The suggestion fails any functional test or introduces algorithmic errors that reduce the accuracy of the skill.
