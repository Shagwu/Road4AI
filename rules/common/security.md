# Security Rules

## Sensitive Data

Never publish or commit:

- API keys, tokens, cookies, private keys, or bearer strings;
- OAuth credential files;
- local absolute paths containing personal identifiers;
- raw customer, CRM, health, finance, or workspace exports;
- live account identifiers unless they are explicitly intended for operational logs.

## Public Examples

Public posts and docs must use safe abstractions for:

- prompt injection strings;
- exploit payloads;
- real user prompts;
- client names;
- private handles;
- exact financial figures when not essential.

Use placeholders such as `<CLIENT_NAME>`, `<REAL_USER_PROMPT>`, `<EXPLOIT_PATTERN>`, and `<PRIVATE_PATH>`.

## Review Trigger

Any public content discussing security, autonomy, prompt injection, or unsafe agent behavior must pass public sanitization review before approval or publishing.

