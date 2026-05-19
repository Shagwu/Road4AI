# Reveal Day Runbook: Hermes v2.0 (2026-05-26)

## 0. Pre-Flight Checklist (T-Minus 48 Hours)
- [ ] **Demo Capture**: Record terminal demo using `ask` command.
  - Setup: Black background, Emerald text (#50C878).
  - Verification: No PII, no local file paths exposed (use `~/Road4AI` alias).
  - Validation: Verify under 60ms latency is visible in recording.
- [ ] **Cinematic Video**: Final export of reveal video (Narration + Demo + Aesthetic B-roll).
- [ ] **Skool Early Access**: Post BTS teaser + link to v2.0 branch to Skool community.
- [ ] **README Polish**: Update `.github/README.md` with links to the reveal video and getting started guide.

## 1. Reveal Day Schedule (All times UTC)

| Time | Platform | Content | Action |
| :--- | :--- | :--- | :--- |
| 07:00 | X/Threads | "The Bridge is Open" (Short Hook + Teaser Video) | Bot (Blotato) |
| 08:00 | Skool | "Inside Hermes v2.0" (Deep-dive technical walkthrough) | Manual (Sharon) |
| 09:00 | LinkedIn | **MAIN REVEAL**: "Hermes v2.0: The Distributed Substrate" (Long-form + Cinematic Video) | Bot (Blotato) |
| 10:00 | YT/IG/TT | "The Self-Knowledge Loop" (Cinematic Short/Reel) | Bot (Blotato) |
| 12:00 | X | "How it works: Distributed HNSW in 5 tweets" (Thread) | Bot (Blotato) |
| 15:00 | All | Q&A Engagement (Reply to comments) | Manual (Sharon) |

## 2. Emergency Procedures
- **Blotato Failure**: Manual post via web UI.
- **Latency Spike**: Append disclaimer to Main Reveal: "Performance optimized for warm queries; cold starts may vary based on distributed network conditions."
- **Governance Breach**: Immediate `chmod -w AGENTS.md` and repo freeze if unauthorized mutation detected.

## 3. Post-Reveal (Next Day)
- [ ] Record feedback from Skool and LinkedIn.
- [ ] Sync `published-log.json`.
- [ ] Archive all reveal drafts.
