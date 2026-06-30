# Phase 4 Teaser: Master Publication Checklist

**Timeline:** July 14 (Karen review) → July 15 (Publish) → July 16 (POC starts)

---

## July 14 (Evening): Karen Review

- [ ] Run Karen adversarial review:
  ```bash
  python tools/karen.py \
    --mode review \
    --content phase4_teaser_x_thread.md \
    --content phase4_teaser_linkedin.md \
    --content phase4_teaser_blog.md \
    --output state/karen_phase4_approval.jsonl \
    --governance_check yes
  ```

- [ ] Check `state/karen_phase4_approval.jsonl`:
  - [ ] `overall_status: "approved"` (or note any needed revisions)
  - [ ] No factual errors flagged
  - [ ] No governance compliance issues
  - [ ] Tone consistent across all three pieces

- [ ] If revisions needed:
  - [ ] Update relevant markdown file(s)
  - [ ] Re-run Karen gate
  - [ ] Confirm approval before proceeding to Step 2

---

## July 15 (Morning): Pre-Publication Checks

### Content Verification
- [ ] X thread: 5 tweets, properly numbered, each tweet under 280 characters
- [ ] LinkedIn: Single post, copy-paste ready, links verified
- [ ] Blog: Full markdown, meta description included, tags listed

### Link Verification
- [ ] GitHub v2.1.0 release link works: https://github.com/Shagwu/Road4AI/releases/tag/v2.1.0
- [ ] AGENTS.md Section 5 link works: https://github.com/Shagwu/Road4AI/blob/main/AGENTS.md#orchestration
- [ ] Blog platform ready (logged in, new post template ready)

### Optional Assets
- [ ] Blog featured image selected/created (optional but recommended):
  - [ ] Screenshot of AGENTS.md Section 5, OR
  - [ ] Screenshot of drift_monitor.py output (green status), OR
  - [ ] Simple diagram (Trend → Voice-Match → Memory-Ops → Halt)

### Social Media Readiness
- [ ] X/Twitter account ready (logged in, ready to post)
- [ ] LinkedIn account ready (logged in, ready to post OR Blotato configured)
- [ ] Blog platform ready (logged in, post editor open)

---

## July 15 (08:00 UTC): Publish X/Twitter Thread

**Platform:** X/Twitter (native composer for threading)

- [ ] Open Twitter.com
- [ ] Click "Compose Post"
- [ ] Paste Tweet 1 (Intro) + links to GitHub v2.1.0 and AGENTS.md Section 5
- [ ] Click "Reply to @yourhandle"
- [ ] Paste Tweet 2 (Signal Flow)
- [ ] Repeat for Tweets 3, 4, 5 (each replies to previous)
- [ ] Preview entire thread (all 5 tweets should show connected)
- [ ] Post thread
- [ ] Pin thread to profile for 24 hours
- [ ] Verify all 5 tweets are live and threaded correctly

**Duration:** ~5 minutes

---

## July 15 (12:00 UTC): Publish LinkedIn Post

**Platform:** LinkedIn (scheduled via Blotato OR manual)

**Option A: Blotato Scheduled**
- [ ] Copy entire LinkedIn post text to clipboard
- [ ] Open Blotato dashboard
- [ ] Create new post
- [ ] Paste text
- [ ] Upload optional image (AGENTS.md screenshot or v2.1.0 release page)
- [ ] Set publish time: 12:00 UTC July 15
- [ ] Schedule post

**Option B: Manual Post**
- [ ] Open LinkedIn.com
- [ ] Click "Start a post"
- [ ] Paste entire post text
- [ ] Upload optional featured image
- [ ] Click "Post"

- [ ] Verify post is live within 2 minutes of scheduled time
- [ ] Add links to comments (GitHub v2.1.0, AGENTS.md, blog post link)
- [ ] Enable commenting (default: on)

**Duration:** ~2 minutes

---

## July 15 (14:00 UTC): Publish Blog Post

**Platform:** Blog (Medium, Ghost, Substack, etc.)

- [ ] Log into blog platform
- [ ] Create new post
- [ ] Paste full markdown from `phase4_teaser_blog.md`
- [ ] Add featured image (optional but recommended)
- [ ] Fill in metadata:
  - [ ] Title: "Phase 4 Begins: Governance Under Fire"
  - [ ] Meta description: "How I built multi-domain AI skills with governance gates that actually hold. Phase 4 POC starts July 16. Real data, real transparency."
  - [ ] Tags: ai, governance, orchestration, open-source, learning-in-public, road4ai
- [ ] Set publish time: 14:00 UTC July 15
- [ ] Preview post (verify formatting, links, image)
- [ ] Publish
- [ ] Verify post is live at expected URL

**Duration:** ~5 minutes

---

## July 15 (14:15 UTC): Cross-Promotion

- [ ] Comment on LinkedIn post with blog link:
  - "Full technical breakdown here: [blog URL]"
- [ ] Retweet X thread with blog link:
  - "Full thread on Phase 4 setup: [blog URL]"
- [ ] Optional: Share blog link in relevant communities (Slack, Discord, Reddit, HN if applicable)

**Duration:** ~3 minutes

---

## July 15 (Evening): Archive & Document

- [ ] Create archive directory:
  ```bash
  mkdir -p archive/phase4_teaser_july15_2026
  cp phase4_teaser_x_thread.md archive/phase4_teaser_july15_2026/
  cp phase4_teaser_linkedin.md archive/phase4_teaser_july15_2026/
  cp phase4_teaser_blog.md archive/phase4_teaser_july15_2026/
  cp state/karen_phase4_approval.jsonl archive/phase4_teaser_july15_2026/
  ```

- [ ] Log publication:
  ```bash
  echo "Phase 4 teasers published July 15, 2026." >> state/publication_log.jsonl
  echo "X thread: 08:00 UTC, LinkedIn: 12:00 UTC, Blog: 14:00 UTC" >> state/publication_log.jsonl
  echo "Karen approved all three pieces before publication." >> state/publication_log.jsonl
  ```

- [ ] Verify all three live:
  - [ ] X thread: https://twitter.com/yourhandle (pinned to profile)
  - [ ] LinkedIn: https://linkedin.com/feed/update/[post-id]
  - [ ] Blog: https://yourblog.com/phase-4-begins-governance-under-fire

---

## July 16 (Morning): Phase 4 POC Starts

- [ ] Verify daily drift monitoring still running (launchd, 09:00 UTC)
- [ ] Verify Harvester CLI ready (GitHub + RSS routing live)
- [ ] Flip switch on Twitter integration (when ready, auth optional)
- [ ] First Phase 4 signal routed through orchestration
- [ ] Drift monitor watches first signal
- [ ] First Phase 4 checkpoint logged to Hermes

---

## Notes on Timing

**Why these times?**
- 08:00 UTC (X): Early morning, good for US West Coast + Europe overlap
- 12:00 UTC (LinkedIn): Noon UTC, lunch time in Europe, morning in US
- 14:00 UTC (Blog): Afternoon UTC, gives X + LinkedIn time to seed before full deep dive

**Why space them 4 hours apart?**
- X thread builds interest first (quick, punchy)
- LinkedIn expands reach (professional network)
- Blog provides depth (for people who want full context)

**Why publish day-before POC?**
- July 15 teaser sets expectations
- July 16 POC start fulfills them
- Momentum builds over 24 hours

---

## Success Criteria

**All three published by 15:00 UTC July 15:**
- ✅ X thread live and pinned (08:00 UTC)
- ✅ LinkedIn post live with links (12:00 UTC)
- ✅ Blog post live with metadata (14:00 UTC)
- ✅ No factual errors in final published versions
- ✅ All links working
- ✅ Tone consistent across platforms

**July 16 morning:**
- ✅ Phase 4 POC starts on schedule
- ✅ First signal routed through full pipeline
- ✅ Drift monitoring watches live
- ✅ All checkpoints logged to Hermes

**July 16–31:**
- ✅ Weekly Phase 4 updates published (incidents, learnings, governance decisions)
- ✅ Zero governance breaches
- ✅ Governance gates hold under real-world load

---

## Quick Reference: File Paths

All content files in `/home/claude/`:
- `phase4_teaser_x_thread.md` (5 tweets, Karen checklist included)
- `phase4_teaser_linkedin.md` (copy-paste ready, Karen checklist included)
- `phase4_teaser_blog.md` (full markdown, Karen checklist included)
- `phase4_teaser_karen_workflow.md` (this workflow file)

Ready for Karen review as-is. All checklists built in.

---

## Emergency Fallback

**If something breaks July 14–15:**

1. **Karen approval delayed:** Defer publication to July 16 (same day as POC start, less ideal but acceptable)
2. **X thread fails to post:** Just post 5 individual tweets linked to each other (not ideal threading, but still effective)
3. **LinkedIn post fails:** Post manually instead of via Blotato (same content, 1 minute delay)
4. **Blog platform down:** Post as Medium article instead, link to it from X + LinkedIn (changes platform, same content)
5. **One platform delayed:** Publish other two on schedule, catch third when ready (staggered but all three eventually live)

**Key:** All three pieces must go live. Timing is preferred (08:00, 12:00, 14:00 UTC), but publishing same-day matters more than perfect timing.

---

## Ready to Go

All content formatted, Karen workflow documented, publication checklist complete.

**Next step:** Run Karen review July 14 evening. Publish July 15. POC starts July 16.
