---
title: "What a Confidence Score Should Actually Measure"
hook: "My confidence scorer was rewarding the source, not the signal."
type: Struggle
platform: LinkedIn
goal: Build in public
status: ready_for_drafting
karen_verdict: null
---

My confidence scorer was rewarding the source, not the signal.

The confidence formula in harvester_pipeline.py has an authority boost: if the source feed is HackerNews, add 0.15 to the score. Every other source gets 0.1.

The problem: none of our RSS feeds are HackerNews. TechCrunch, Ars Technica, Hugging Face, Ollama, AI Alignment Forum, LessWrong — they all get the same 0.1 authority boost. The HackerNews branch in the code is dead. It never fires.

But the formula still uses it as if it does. The confidence scores look real — three decimal places, calculated from keyword relevance and authority — but the authority component is measuring something that doesn't exist in our pipeline.

I found this while debugging why some signals scored 0.50 when I expected higher. Traced through the formula: relevance * 0.4 + keyword_boost + authority_boost + 0.2. The authority boost was always 0.1, never 0.15, because the condition `if "hackernews" in source_feed` never matched.

Not a bug in the sense that it produces wrong results — the scores are internally consistent. A bug in the sense that the formula is measuring something that isn't there, and anyone reading the code would assume HackerNews signals get a meaningful boost.

Fixed by removing the dead branch and making authority scoring source-agnostic. The scores didn't change. The honesty did.
