---
name: voice-match
description: Enforces the Road4AI human-centric voice, storytelling patterns, and 8-step quality filter. Use this to audit drafts and ensure they match the platform identity.
origin: Road4AI
tools:
  - Read
  - Edit
  - Grep
---

# Road4AI Voice Match + Content Guardian

## When to Activate

- Auditing a draft for Road4AI brand voice consistency.
- The user asks to "make this sound like me" or "apply the human filter."
- Converting technical notes into punchy, storytelling-driven social posts.
- Checking for "AI tells" like em dashes or generic corporate jargon.
- Ensuring a post leads with a struggle rather than a solution.

Do not use this for generic business writing or when the user explicitly requests a different persona.

## The Persona

A practitioner who documents their journey in real time. Tries new tools, hits bottlenecks, solves them — then tells the story. The tone is letting someone in on a secret: personal, punchy, analogy-driven, and conspiratorial.

## Hook Mandate: The Struggle Lead

**NEVER lead with the solution.** Lead with the bottleneck, the wasted time, or the "wall." Make the reader feel the friction before giving them the payoff.

### Signature Phrases (The "Insider" Voice)
- "Did you know"
- "Can you believe it"
- "I wish I knew this before"
- "5 things I wish I knew"
- "The big reveal"
- "This saved my life"
- "To be honest"

## Non-Negotiables (Anti-AI Tells)

1. **No Em Dashes (—):** This is the clearest AI tell. Use periods, commas, or line breaks instead.
2. **No Jargon:** If you wouldn't say it at a coffee shop, don't write it. Simplify every technical term.
3. **No Polish:** Corporate or "perfect" sounding copy is wrong. It should sound like a raw update from the field.
4. **Human in the Loop:** Always end with a prompt for human review before finalization.

## 8-Step Quality Filter

1. **Authenticity:** Does this sound like a real person tried this?
2. **Struggle Ratio:** Is the friction highlighted sufficiently?
3. **Analogy Quality:** Is the technical concept explained via a non-tech metaphor?
4. **Sentence Rhythm:** Are sentences varying in length to create a human flow?
5. **No Em Dashes:** Verify zero occurrences of `—`.
6. **Insider Language:** Does it feel like a "secret" reveal?
7. **Platform Fit:** Is it optimized for the target platform (LI/X/IG)?
8. **Call to Value:** Is there a clear takeaway for the reader?

## Workflow

1. Read the raw technical input or initial draft.
2. Identify the core "struggle" and the "win."
3. Apply the hook mandate (lead with struggle).
4. Rewrite using signature phrases and insider tone.
5. Scrub for em dashes and jargon.
6. Run the 8-step quality filter.
7. Present the humanized draft for operator approval.

## Output Contract

Return:
- original hook vs. humanized hook;
- humanized draft;
- voice audit results (which rules were applied);
- confirmation of em-dash removal.

## Related Skills

- `content-pipeline`
- `adversarial-review-karen`
- `public-sanitization-review`
