# Public Sanitization Rules

Before any public draft is approved or scheduled, scan for content that should be abstracted.

## Redact or Abstract

- Copy-pasteable exploit strings.
- Prompt injection payloads.
- Real user prompts that were not intended for publication.
- Private handles, private account names, and personal local paths.
- Exact financial details unless the number is core to the lesson and approved.
- Internal workspace, CRM, health, or customer data.

## Keep

- The engineering lesson.
- The failure mode.
- The architecture pattern.
- The decision tradeoff.
- The human-in-the-loop boundary.

## Replacement Patterns

- Real client or user: `<CLIENT_NAME>` or `<USER_ROLE>`.
- Live exploit: `<EXPLOIT_PATTERN>`.
- Local path: `<PRIVATE_PATH>`.
- Sensitive prompt: `<REAL_USER_PROMPT>`.
- Account or credential reference: `<PRIVATE_ACCOUNT_ID>` or `<SECRET_REFERENCE>`.

## Security Theater Trap Rule

When discussing a vulnerability or exploit publicly, describe the class of exploit and its effect. Do not include a string that a reader can paste directly into a system to reproduce the attack.

