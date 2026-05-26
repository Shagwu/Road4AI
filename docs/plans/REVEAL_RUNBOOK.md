# Reveal Day Runbook: Hermes v2.0 (2026-05-26)

## 0. Pre-Flight Checklist (T-Minus 48 Hours)
- [x] **Demo Capture**: Record terminal demo using `ask` command.
  - Setup: Black background, Emerald text (#50C878).
  - Verification: No PII, no local file paths exposed (use `~/Road4AI` alias).
  - Validation: Verify under 60ms latency is visible in recording.
- [x] **Cinematic Video**: Final export of reveal video (Narration + Demo + Aesthetic B-roll).
- [x] **Skool Early Access**: Post BTS teaser + link to v2.0 branch to Skool community.
- [x] **README Polish**: Update `.github/README.md` with links to the reveal video and getting started guide.

## 1. Reveal Day Schedule (All times UTC)

| Time | Platform | Content | Action | Status |
| :--- | :--- | :--- | :--- | :--- |
| 07:00 | X/Threads | "The Bridge is Open" (Short Hook + Teaser Video) | Bot (Blotato) | ✅ DONE |
| 08:00 | Skool | "Inside Hermes v2.0" (Deep-dive technical walkthrough) | Manual (Sharon) | ✅ DONE |
| 09:00 | LinkedIn | **MAIN REVEAL**: "Hermes v2.0: The Distributed Substrate" (Long-form + Cinematic Video) | Bot (Blotato) | ✅ DONE |
| 10:00 | YT/IG/TT | "The Self-Knowledge Loop" (Cinematic Short/Reel) | Bot (Blotato) | ✅ DONE |
| 12:00 | X | "How it works: Distributed HNSW in 5 tweets" (Thread) | Bot (Blotato) | ✅ DONE |
| 15:00 | All | Q&A Engagement (Reply to comments) | Manual (Sharon) | 🚀 ACTIVE |

## 2. Engagement Protocol (The Golden Hour)
- **LinkedIn/X**: For the first 60 minutes after the 09:00 Main Reveal, Sharon must be "Active-Online."
- **Response Rule**: Prioritize technical questions. Every comment gets a reply that reinforces a core pillar (Ownership/Scale/Integrity).
- **Skool Cross-Pollination**: If a question is too deep for a comment, reply with: "Great question — I just dropped the technical deep-dive on this in the Skool community [Link]."

## 3. Plan B: MV-Reveal (The Fallback)
If the Cinematic Video is not export-ready by May 24th:
- **Format**: Text-based narrative + High-Res GIF of the `ask` command in action.
- **Visual**: A static architectural diagram (Blue/Emerald) comparing v1.0 (Local) to v2.0 (Distributed).
- **Trigger**: Decision to move to Plan B must be made by 18:00 UTC on May 24th.

## 4. Emergency Procedures
- **Blotato Failure**: Manual post via web UI.
- **Latency Spike**: Append disclaimer to Main Reveal: "Performance optimized for warm queries; cold starts may vary based on distributed network conditions."
- **Governance Breach**: Immediate `chmod -w AGENTS.md` and repo freeze if unauthorized mutation detected.

## 3. Post-Reveal (Next Day)
- [ ] Record feedback from Skool and LinkedIn.
- [ ] Sync `published-log.json`.
- [ ] Archive all reveal drafts.
