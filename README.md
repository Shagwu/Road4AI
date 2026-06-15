# Road4AI

A layered multi-agent system for solo operators. CLI-native, local-first, built on tools that don't cost money to run. [page:2]

## 1. What Road4AI is

- Multi-agent stack for a solo builder (no paid APIs).
- Designed around real workflows: ideation, build, reasoning, memory, distribution.
- Runs from the terminal using tools like Gemini CLI, Claude, and your local models.

## 2. Architecture

### Agent layers

- Ideation + research: Gemini CLI  
- Structured builds: Codex  
- Reasoning + strategy: Claude  
- Memory: Hermes v2.0 (distributed context)  
- Distribution: Blotato (social automation) [page:2]

You can also include a short description of how agents talk to each other:
- Shared memory contract via Hermes v2.0.
- Each agent has a defined role, input/output schema, and stop conditions.

## 3. Tech stack

| Layer                 | Tool         | What it does                                    |
|----------------------|-------------|-------------------------------------------------|
| Ideation + research  | Gemini CLI  | First-pass thinking, fast iteration             |
| Structured builds    | Codex       | Code, refactoring, precise edits                |
| Reasoning + strategy | Claude      | Long-context reasoning and planning             |
| Memory               | Hermes v2.0 | Distributed context across all agents           |
| Distribution         | Blotato     | Scheduled content and social posting            |
| Git workflow         | GitNexus    | Version control and repo hygiene                | [page:2]

(That table mirrors the one already in your profile README, but here it’s clearly “system stack” for the project.) [page:2]

## 4. Getting started

This is where you give the “clone and run” steps, aligned with how you actually work:

```bash
# 1. Clone the repo
git clone https://github.com/Shagwu/Road4AI.git
cd Road4AI

# 2. Create and activate a virtualenv (if using Python)
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the main entrypoint
python main.py
```

Adjust these commands to match however Road4AI is actually started (Gemini CLI entry, Makefile, Bash script, etc.).

## 5. Configuration

Add a short section describing config files you plan to use:

- `config/agents.yml` – agent roles, tools, and prompts.  
- `config/memory.yml` – Hermes v2.0 settings and storage locations.  
- `.env` – environment variables (keys for Claude, Gemini, local endpoints, etc.).

Even if these files are still WIP, listing them sets expectations and gives you a roadmap.

## 6. Workflows

Describe 2–3 concrete workflows in bullet form, the way a solo builder would actually run them:

- Research and plan a new feature  
  1. Use Gemini CLI to generate first-pass plan and notes.  
  2. Hand off to Codex agent for scaffolding code.  
  3. Use Claude agent to review, refactor, and document.

- Content pipeline for Road4AI  
  1. Agents generate posts and scripts from build logs.  
  2. Hermes v2.0 keeps context across sessions.  
  3. Blotato handles scheduling and distribution.

## 7. Roadmap

Tie it back to what you already wrote in the profile:

- Hardening Hermes v2.0 (memory backbone across agents and tools). [page:2]  
- Making the system fully reproducible for other solo builders.  
- Adding templates for common agent workflows (content, research, coding).

## 8. Links

Finish with explicit links:

- Live site: `https://road4-ai.vercel.app` or `https://shagwu.github.io/Road4AI/` (whichever is canonical for you). [page:2]  
- Profile + narrative: `https://github.com/Shagwu`  
- Social: `@road4ai` on Instagram, TikTok, etc. [page:2]

### How this plays with your profile README

- Profile (`Shagwu/Shagwu`): stays opinionated and story-driven, with Road4AI as your flagship project and the “why.” [page:2]  
- Repo (`Shagwu/Road4AI`): becomes the technical **how** — architecture, stack, install, workflows, roadmap. [page:2]

If you’d like, I can draft a fully filled-in README in one shot that you can paste directly into `Road4AI/README.md`; if so, what is your current “truth” for how to run Road4AI locally (command + main entry file)?  

<user_response_autocomplete>
Entry is a Python script run with python main.py
Entry is via Gemini CLI commands and a shell script
I haven’t decided the exact entrypoint yet
