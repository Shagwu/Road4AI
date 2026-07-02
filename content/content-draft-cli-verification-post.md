# Content Draft: "The CLI Lied To Me (Confidently)"
**Status:** DRAFT — needs Karen adversarial review before publishing
**Not Phase 4 reveal content — clear of the July 15 content hold**

---

## X Thread

**1/**
Ran a free coding model against my repo yesterday. Asked it to summarize the architecture.

It gave me a full breakdown. Function names. File paths. A whole registry system.

None of it existed.

**2/**
Not vague guessing either. Confident, specific, detailed. Read exactly like it had opened the files.

It hadn't. It pattern-matched to "what a repo like this usually looks like" and reported that as fact.

**3/**
Here's the part that matters: I only caught it because I asked a second time.

"Verify your assumptions before editing anything."

That one prompt made it go back, actually check, and admit almost everything in its first answer was wrong.

**4/**
So now every CLI agent I test has to clear two gates before I trust it with real work:

1. Summarize
2. Verify, out loud, with a confidence rating on every claim

If it can't survive its own re-check, it doesn't touch my code.

**5/**
Free tools are great until the one you rely on gets pulled overnight (ask me how I know). But "free" also means "unverified" until proven otherwise.

The fix isn't finding a model that never hallucinates. It's building a habit that catches it when it does.

---

## LinkedIn

I tested a free coding model on my repo this week, and it taught me something worth sharing.

I asked it to summarize how my multi-agent system routes tasks and registers tools. It came back with a clean, specific answer, file paths, function names, a registry pattern, the works.

Almost none of it was real. It hadn't actually read the code that carefully. It had pattern-matched to what a repo like mine "usually" looks like, and presented that guess with full confidence.

I only caught it because I asked it to verify itself before making any changes. That single follow-up prompt made it go back, actually check the files, and correct nearly every claim from its first pass.

That's the real lesson: the risk with free or cheap AI coding tools isn't that they're wrong sometimes. It's that they can be *confidently* wrong in a way that looks identical to being right, right up until you ask them to prove it.

So I wrote a short rule set I now run every new coding agent through:
→ Summarize first, plan second, never both in one pass
→ Every claim about the code gets tagged: confirmed, inferred, or guessed
→ No file edits without a separate approval step
→ If something can't be found in the repo, say so, don't fill the gap with a good guess

Small habit. Costs one extra prompt. Would've saved me from shipping a plan built on fiction.

If you're building with free-tier AI coding tools, the question isn't "is this model good." It's "what happens when I ask it to check its own work." That answer tells you everything.

---

## Notes for Karen pass
- Confirm no em dashes slipped through
- Verify no AI-sounding openers
- Check struggle-content ratio still holds for this week's queue
- Model name (gpt-oss-120b:free) — decide whether to name it explicitly or keep generic ("a free coding model") depending on how comfortable we are naming specific tools publicly
