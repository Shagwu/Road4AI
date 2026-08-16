---
name: road4ai-operator-site-workflow
description: Build, iteratively enhance, package, and share polished responsive frontend websites from a reference repository or setup description. Use for repository-driven landing pages, operator-console interfaces, repeated UI refinement, skill packaging, GitHub publishing, community releases, design systems, generated assets, interactive controls, responsive verification, and checkpoint delivery.
---

# Road4AI Operator-Site Workflow

Use this skill when a user wants a website built from a GitHub repository, README, live reference, setup description, or an existing frontend that will be refined through several small feature requests.

## Core operating model

Treat the source repository and any user-provided reference as the content ground truth. Treat the website as a frontend product, not a documentation dump. Preserve the source’s actual names, architecture, links, and workflows; do not invent capabilities, customer reviews, ratings, testimonials, or unsupported claims.

Work in short, auditable phases:

1. Inspect the reference and extract its purpose, architecture, key tools, links, and user workflow.
2. Define the visual direction before writing frontend code. Record the chosen direction in `ideas.md` in the user’s language.
3. Initialize or identify the managed web project. Read your environment's project scaffolding or template guidance before editing, if one exists.
4. Generate the required visual assets early. Use custom generated assets for prominent hero or branded areas, and use the returned asset URLs immediately. Keep large assets outside the project source tree.
5. Establish the shared layout and design tokens before adding feature sections.
6. Implement the main page using reusable components and real source content.
7. Add interactions as product behavior, not decoration: keyboard access, visible focus, hover states, clipboard feedback, toggles, filters, command inputs, and reduced-motion behavior where applicable.
8. Verify representative desktop and mobile layouts with screenshots. Check text contrast, responsive wrapping, navigation escape routes, valid links, and the most important interaction states.
9. Save one coherent checkpoint after the requested change is implemented and verified. Deliver the checkpoint reference to the user.

## Reference inspection

When a URL is supplied, open it first. If the published page is unavailable, inspect the source repository and its README, then clearly treat the repository as ground truth. Capture findings in a short project note before implementation. Prefer the repository’s documented links and paths over assumptions.

Extract at minimum:

| Area | Capture |
| --- | --- |
| Identity | Project name, maintainer identity, positioning, tone |
| Architecture | Main agents, modules, workflows, memory or approval model |
| Setup | Installation commands, requirements, first-run sequence |
| Tools | Hardware assumptions, software tools, external services |
| Proof points | Existing artifacts, repositories, docs, or linked demos |
| Constraints | Local-first requirements, human gates, portability, unsupported claims |

## Design direction

For a non-replication request, record three genuinely different approaches in `ideas.md`, then select one and expand it. Do not mix directions casually. The chosen direction must specify the movement, principles, color reasoning, layout paradigm, signature motifs, interaction philosophy, animation rules, typography, brand essence, voice, logo concept, and ownable brand color.

For an operator or AI-infrastructure setup, a terminal-inspired direction is appropriate when it reinforces the source. Prefer an asymmetric composition, dark graphite surfaces, signal emerald, restrained amber for approval or warning states, monospace display typography paired with a readable body face, and precise motion. Avoid generic centered marketing layouts, excessive rounded cards, purple gradients, and invented social proof.

Add a short style reminder comment to every edited page or stylesheet. Ask before each major choice: “Does this reinforce or dilute the design philosophy?”

## Content composition

Use a clear narrative rather than repeating README prose. A strong operator-site sequence is:

1. Hero: what the system is and why it exists.
2. Stack or manifest: the actual agents, modules, and responsibilities.
3. Philosophy: the operating principles, such as shared context and human approval.
4. Workflow: how input becomes shipped output.
5. Setup terminal: real installation commands with copy affordances.
6. Operator Kit: hardware and software inventory, with a filter when useful.
7. Start or links: repository entry points and practical next actions.

Make commands and links real. When the source does not prescribe hardware, say so instead of fabricating a specification.

## Interaction patterns

Implement small interactions with explicit state and graceful failure:

- **Typing terminal:** Reveal setup commands in sequence with a restrained cursor animation. Respect `prefers-reduced-motion`.
- **Copy command:** Copy only the intended command and show temporary confirmation. Provide a fallback or failure state when Clipboard API access is unavailable.
- **Operator Kit filter:** Support `all`, `hardware`, and `software` views with accessible pressed states and counts.
- **Theme toggle:** Persist the user’s dark/light choice locally, expose an accessible label, and maintain readable contrast in both themes.
- **Simulated console:** Keep command history in component state. Normalize input, support Enter submission, and provide concise responses for `help`, `status`, `clear`, `whoami`, `contact`, `projects`, and `about`. Unknown commands should explain how to recover. Render external links as real anchors with `target="_blank"` and `rel="noreferrer"`.
- **Responsive behavior:** Stack complex grids on narrow screens, keep controls tappable, and prevent long command or link strings from overflowing.

Keep animations under roughly 300ms for ordinary UI state changes. Animate transform and opacity where possible. Use stronger timing only for rare entrance or delight moments. Never hide essential content behind animation.

## Frontend implementation rules

Use the project template’s existing components before creating new primitives. Keep page composition in `client/src/pages/`, reusable UI in `client/src/components/`, and tokens in `client/src/index.css`. Do not modify backend, server, API, database, or authentication code when the request is frontend-only.

Use your project's asset workflow. Store source media in your environment's designated static-assets location, upload it through whatever asset pipeline your platform provides, and reference the returned URL exactly. Do not place large images or media in `client/public/` or the project source tree.

Keep layout, theme, and interaction state out of render-time side effects. Use `useEffect` for DOM theme attributes, persistence, timers, and cleanup. Stabilize arrays and objects used by stateful logic. Preserve keyboard focus rings and semantic button/link behavior.

## Iterative enhancement workflow

When the user requests a follow-up feature to an existing site:

1. Restate the requested behavior in one sentence.
2. Add explicit unchecked items to `todo.md` before editing.
3. Update the plan with implementation and verification phases.
4. Edit the smallest cohesive set of frontend files; preserve working design language.
5. Verify the feature at representative desktop and mobile sizes.
6. Mark the relevant todo items complete.
7. Save a new checkpoint and deliver only the checkpoint reference unless the user asks for additional files.

Do not restart the project from scratch for a focused enhancement. If a change breaks the project and direct edits cannot recover it, use your environment's checkpoint or rollback mechanism if one exists, or a safe `git revert`, instead of destructive `git reset` commands.

## Package and share the workflow skill

When this workflow is itself being turned into a reusable skill, keep the package separate from any application repository and keep the required `SKILL.md` at the package root. Remove unused example files and verify that the package contains no secrets, private URLs, personal data, or environment-specific paths that community members cannot use.

Run whatever skill validator your environment provides before delivery, if one is available. For example:

```bash
python scripts/quick_validate.py <skill-name>
```

If no validator exists, manually re-read the SKILL.md against this checklist before distribution.

For GitHub distribution, place the skill directory in a public repository, inspect the staged diff, and push a clean initial commit:

```bash
git init
git add SKILL.md references/ scripts/ templates/
git commit -m "Add reusable website workflow skill"
git branch -M main
git remote add origin https://github.com/<your-account>/<skill-repository>.git
git push -u origin main
```

Use version tags for meaningful changes. A first public package can use `v0.1.0`; use patch versions for clarifications, minor versions for backward-compatible capabilities, and major versions for breaking package or behavior changes. Create release notes that summarize what the skill does, when it triggers, what changed, and whether users need to migrate.

Share the package through two paths: attach `SKILL.md` directly for users on platforms that support previewing, downloading, or adding skills to a collection; and share the public GitHub repository URL for community members who want to inspect, clone, fork, or contribute. Include a short announcement, one example request, the validator command if one exists, contribution expectations, and a license appropriate to the intended reuse.

Invite improvements through issues or pull requests. Require contributors to keep the skill concise, preserve source-grounded content, avoid fabricated social proof, document bundled resources, and validate any scripts or references they add.

## Verification checklist

Before delivery, verify that:

- The dev server is running and the page renders without TypeScript or browser-console errors.
- Desktop and mobile screenshots show the intended hierarchy and no clipped or invisible content.
- All navigation links and external repository URLs are valid and intentional.
- Buttons have visible hover, active, focus, and feedback states.
- Clipboard, filter, theme, and simulated-console interactions fail gracefully.
- Light and dark themes maintain contrast for text over actual rendered backgrounds.
- Reduced-motion users are not forced to watch non-essential animations.
- No fabricated testimonials, ratings, reviews, or unsupported claims were added.
- The final checkpoint contains the complete requested feature, not an intermediate state.
