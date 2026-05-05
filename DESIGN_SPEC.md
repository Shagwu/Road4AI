# DESIGN_SPEC.md - Incident Triage Agent

## Overview
An interactive agent designed to help engineers triage incidents by summarizing alerts and suggesting potential fixes based on codebase context. It integrates with GitHub to fetch recent changes, issues, and logs if applicable.

## Example Use Cases
- **Input**: "Alert: High latency on /api/v1/checkout"
- **Output**: Summary of recent PRs affecting checkout logic, relevant GitHub issues, and a suggested diagnostic path or fix.

## Tools Required
- **GitHub Tool**: To search repositories, list commits, read file contents, and check issue status.
- **Code Search**: (Internal) To find relevant files in the local repository.

## Constraints & Safety Rules
- The agent MUST NOT modify code or merge PRs autonomously.
- It should prioritize security and not leak any credentials found in logs or code.

## Success Criteria
- Accurately identifies the PRs most likely related to a given alert.
- Provides concise, technical summaries without fluff.
- Suggested fixes are idiomatically consistent with the codebase.

## Reference Samples
- `data-science`: For the sub-agent analysis pattern.
- `ambient-expense-agent`: For understanding event/alert contexts (if we move to reactive later).
