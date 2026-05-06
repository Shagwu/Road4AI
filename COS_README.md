# Road4AI — Content Ideation Agent Squad

Multi-agent ideation pipeline for Road4AI content production.
Built on Gemini CLI's native subagent (hub-and-spoke) architecture.

---

## File structure

```
.gemini/
  agents/
    chief-of-staff.md       ← orchestrator (main agent persona)
    trend-researcher.md     ← specialist: finds what's hot this week
    voice-match-ideator.md  ← specialist: hooks in Shagwu's voice
    format-selector.md      ← specialist: platform + format matching

prompts/
  monday-ideation.md        ← weekly activation prompt (copy/paste into CLI)
```

---

## Setup (one-time)

**1. Enable subagents in Gemini CLI settings**

Add this to `~/.gemini/settings.json`:

```json
{
  "experimental": {
    "subagents": true
  }
}
```

**2. Copy agent files into your Road4AI project**

```bash
cp -r .gemini/ /path/to/road4ai-project/.gemini/
```

**3. Confirm agents are detected**

Start Gemini CLI from your project root and run:
```
/agents list
```
You should see: trend-researcher, voice-match-ideator, format-selector

---

## Weekly ritual

**Sunday:** Brain dump everything into `inbox.md` at the project root.
Stream-of-consciousness is fine. Bullet points, half-sentences, whatever.

**Monday morning:** Open Warp, `cd` into your Road4AI project, start Gemini CLI.
Copy the prompt from `prompts/monday-ideation.md` and paste it in.

Watch the three specialist agents run in parallel.
Check the `ideas.md` output.
Approve, edit, or bin each idea.
Feed approved ideas into your existing Codex drafting step.

---

## Connecting to your existing pipeline

```
inbox.md
    ↓
[ideation agents — this squad]
    ↓
ideas.md  (you review)
    ↓
Codex drafts post
    ↓
Gemini reviews for voice
    ↓
Blotato schedules
```

---

## Tweaking the agents

- **Voice feels off?** Edit the non-negotiables section in `voice-match-ideator.md`
- **Wrong platforms being picked?** Update the platform rules in `format-selector.md`
- **Trend sources missing?** Add preferred newsletters/accounts to `trend-researcher.md`
- **ideas.md format not right?** Adjust the output template in `chief-of-staff.md`

---

## Notes

- Subagents run in isolated contexts — they do not see each other's work mid-run.
  The Chief of Staff aggregates their outputs after all three complete.
- The trend-researcher uses web_search. Make sure your Gemini CLI session
  has web search tool access enabled.
- Nothing in this pipeline posts or schedules automatically.
  Human review is baked in as a hard stop before anything leaves ideas.md.
