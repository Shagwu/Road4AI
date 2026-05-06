# Monday Ideation Pipeline — Activation Prompt
# Drop this into Gemini CLI every Monday morning after your inbox.md is updated.
# ----------------------------------------------------------------

Read inbox.md from the project root.

Build a content ideation brief with 5–10 distinct angles extracted
from the brain dump. Group by theme and flag the 2–3 that feel
most alive or opinionated.

Then run a parallel content ideation sprint:
- Use @trend-researcher to scan what's hot in AI/Claude/Gemini CLI
  this week and surface timely hooks that match the brief angles
- Use @voice-match-ideator to generate 3 hook options per angle
  in Shagwu's exact voice (punchy, conspiratorial, no em dashes,
  passes the coffee-shop test)
- Use @format-selector to match each angle to the right platform
  and format (primary + repurpose recommendation)

Once all three subagents return their summaries, aggregate everything
into ideas.md with one block per idea:
- Hook draft (best option from voice-match-ideator)
- Platform + format (from format-selector)
- Trend peg if relevant (from trend-researcher)
- Rank: 🔥 this week / 🟡 next week / 🧊 back-burner
- Source signal from inbox.md

End ideas.md with the human review warning.

Do not post or schedule anything. Output only.

# ----------------------------------------------------------------
# OPTIONAL FLAGS (add to end of prompt as needed):
#
# "Focus only on TikTok/Reels format ideas this run."
# "Prioritise angles tied to Hermes v2.0 build reveal."
# "Filter for ideas that could attract sponsorship interest."
# "Limit to 5 ideas — tighter batch this week."
# ----------------------------------------------------------------
