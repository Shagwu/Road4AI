# Phase 4 Teaser: Karen Review & Publication Workflow

**Review Date:** July 14, 2026 (Evening)  
**Publication Date:** July 15, 2026  
**POC Start:** July 16, 2026

---

## Karen Review Workflow

### Step 1: Run Karen Adversarial Review

```bash
python tools/karen.py \
  --mode review \
  --content phase4_teaser_x_thread.md \
  --content phase4_teaser_linkedin.md \
  --content phase4_teaser_blog.md \
  --output state/karen_phase4_approval.jsonl \
  --governance_check yes
```

This runs mistral-nemo (adversary) + qwen2.5-coder:14b (filter) against all three pieces.

### Step 2: Karen Looks For These Issues

**Factual Accuracy:**
- Voice-match baseline: 0.788 (live Ollama, zero failures) ✓
- Memory-ops baseline: 0.915 (v2.1 confirmed) ✓
- Drift thresholds: ±5% alert / ±10% halt ✓
- July 1–14 monitoring: 10 days, green status, no breaches ✓
- Harvester: GitHub + RSS live, Twitter auth optional ✓

**Tone & Narrative:**
- Learning-in-public framing: Honest, transparent, no spin ✓
- Conspiratorial/coffee-shop voice: Punchy, direct, personal ✓
- Governance as the real story: Not just "skills improve," but "governance holds" ✓
- No em dashes used (hard rule) ✓
- No exact quotes from docs (paraphrase instead) ✓

**Governance Compliance:**
- No promises we can't keep ("governance holds" is framed as question/test, not guarantee) ✓
- No leaking protected info (AGENTS.md rules are public) ✓
- Karen review gate enforced before publish ✓

**Overstatement Check:**
- "Does governance hold?" = honest question ✓
- "Documenting every incident" = commitment to transparency ✓
- "Learning in public" = appropriate framing ✓
- "Zero unjustified incidents" = realistic (not zero incidents, zero unjustified) ✓

### Step 3: Review Output

Karen returns `state/karen_phase4_approval.jsonl` with:

```json
{
  "timestamp": "2026-07-14T20:15:00Z",
  "pieces_reviewed": 3,
  "overall_status": "approved" | "rejected" | "needs_revision",
  "per_piece": [
    {
      "piece": "phase4_teaser_x_thread.md",
      "status": "approved" | "rejected",
      "issues": [],
      "confidence": 0.95
    },
    ...
  ],
  "summary": "All three pieces factually accurate, tone consistent, governance compliant.",
  "revisions_needed": []
}
```

**If approved:** Proceed to publication (Step 4)  
**If needs revision:** Update content, re-run Karen gate, publish July 15 (or defer if major issues)  
**If rejected:** Investigate, revise significantly, re-run Karen gate

### Step 4: Pre-Publish Checklist

Before hitting publish on any platform:

- [ ] Karen approval logged in `state/karen_phase4_approval.jsonl`
- [ ] All three files have `Karen Review Checklist` section completed
- [ ] GitHub v2.1.0 release link verified (live: https://github.com/Shagwu/Road4AI/releases/tag/v2.1.0)
- [ ] AGENTS.md Section 5 link verified (live, orchestration rules visible)
- [ ] X thread formatted (5 tweets, properly numbered, threaded)
- [ ] LinkedIn post copy-pasted to clipboard (ready to paste to Blotato or LinkedIn)
- [ ] Blog post in markdown, ready for your blog platform
- [ ] Blog featured image selected or created (optional but recommended)
- [ ] Slack webhook (if approved) configured in .env (optional, non-blocking)

---

## Publication Schedule (July 15)

| Time | Platform | Content | Method | Duration |
|------|----------|---------|--------|----------|
| 08:00 UTC | X/Twitter | 5-tweet thread | Manual (native composer) | 5 min |
| 12:00 UTC | LinkedIn | Single post | Blotato scheduled OR manual | 2 min |
| 14:00 UTC | Blog | Full teaser + header | Manual (copy-paste to blog platform) | 5 min |

**Total execution time:** ~12 minutes

---

## Publication Instructions by Platform

### X/Twitter (08:00 UTC)

**Format:** 5-tweet thread (use native Twitter composer for proper threading)

**Steps:**
1. Open Twitter.com
2. Click "Compose Post"
3. Paste Tweet 1 (Intro)
4. Click "Reply to @yourhandle"
5. Paste Tweet 2 (Signal Flow)
6. Repeat for Tweets 3, 4, 5

**Before posting:**
- Add links to GitHub v2.1.0 and AGENTS.md Section 5 in first tweet or thread description
- Preview entire thread (should show all 5 tweets connected)
- Pin thread to profile for 24 hours after posting

**Expected engagement:** 50–150 retweets, focus on governance + transparency angle

---

### LinkedIn (12:00 UTC)

**Format:** Single post with links in comments

**Option A (Blotato Scheduled):**
```bash
# Copy entire post text to Blotato
# Set publish time: 12:00 UTC July 15
# Include image (optional): screenshot of AGENTS.md Section 5
```

**Option B (Manual Post):**
1. Open LinkedIn
2. Click "Start a post"
3. Paste entire post text
4. Add featured image (optional)
5. Click "Post"

**Before posting:**
- Add links to comments (GitHub v2.1.0, AGENTS.md, blog post)
- Optional: Include screenshot of v2.1.0 release page or AGENTS.md orchestration rules

**Expected engagement:** 20–50 comments (questions about governance, orchestration, Phase 4)

---

### Blog (14:00 UTC)

**Format:** Full markdown post, published on your blog platform

**Steps:**
1. Log into blog platform (Medium, Ghost, Substack, etc.)
2. Create new post
3. Paste full markdown from `phase4_teaser_blog.md`
4. Add featured image (optional but recommended):
   - Screenshot of AGENTS.md Section 5
   - OR screenshot of drift_monitor.py output
   - OR simple diagram (Trend → Voice-Match → Memory-Ops → Halt)
5. Fill in metadata:
   - Title: "Phase 4 Begins: Governance Under Fire"
   - Meta description: "How I built multi-domain AI skills with governance gates that actually hold."
   - Tags: ai, governance, orchestration, open-source, learning-in-public, road4ai
6. Set publish time: 14:00 UTC July 15
7. Click "Publish"

**After publishing:**
- Share link in LinkedIn comments (on your 12:00 UTC post)
- Retweet X thread (08:00 UTC) with blog link
- Share link in relevant communities (Slack, Discord, Reddit if applicable)

---

## Post-Publication (July 15, Evening)

**Checkpoint & Archive:**
```bash
# Create publication record
mkdir -p archive/phase4_teaser_july15_2026
cp phase4_teaser_x_thread.md archive/phase4_teaser_july15_2026/
cp phase4_teaser_linkedin.md archive/phase4_teaser_july15_2026/
cp phase4_teaser_blog.md archive/phase4_teaser_july15_2026/
cp state/karen_phase4_approval.jsonl archive/phase4_teaser_july15_2026/

# Log publication
echo "Phase 4 teasers published July 15, 2026. All platforms live." >> state/publication_log.jsonl
```

**Verify All Three Live:**
- [ ] X thread posted, pinned, all 5 tweets visible
- [ ] LinkedIn post live, links in comments
- [ ] Blog post published, indexed (check URL directly)

---

## If Karen Rejects or Needs Revision

**Scenario 1: Minor revisions needed**
- Karen flags specific issue (e.g., "overstatement on governance certainty")
- Update content in the relevant markdown file
- Re-run Karen gate (Step 3)
- If approved, publish same day (July 15)

**Scenario 2: Major revision needed**
- Karen flags significant issue (e.g., factual inaccuracy, governance compliance breach)
- Stop. Don't publish.
- Investigate root cause (check numbers, revalidate claims)
- Revise content substantially
- Re-run Karen gate
- Decide: publish July 15 (if ready) or defer to July 16

**Scenario 3: Rejection**
- Karen marks content as "rejected" (high confidence in issue)
- Do not publish without COS investigation
- Reach out to COS (me): "Karen rejected Phase 4 teasers. Issue: [X]. Need guidance."
- Investigate, revise, re-run

---

## Success Criteria

**July 15 (Publication):**
- ✅ Karen approved all three pieces
- ✅ All three published across platforms
- ✅ Links to GitHub/AGENTS.md live and accessible
- ✅ Tone consistent across all platforms
- ✅ No factual errors caught in real-time

**July 16 (POC Start):**
- ✅ Harvester goes live on Twitter (or GitHub + RSS if Twitter auth pending)
- ✅ Daily drift monitoring continues (baseline observation + live signals)
- ✅ First Phase 4 POC data logged to Hermes

**July 16–31 (Phase 4 In Progress):**
- ✅ Weekly updates published (yellow/blue incidents, decisions, learnings)
- ✅ Zero governance breaches
- ✅ Governance gates hold under real-world signal load

---

## Files Ready for Karen Review

- `/home/claude/phase4_teaser_x_thread.md`
- `/home/claude/phase4_teaser_linkedin.md`
- `/home/claude/phase4_teaser_blog.md`

All three include Karen Review Checklists at the end.

**Next step:** Run Karen gate July 14 evening, publish July 15, POC starts July 16.
