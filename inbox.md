# INBOX.MD — Raw Capture File
# Road4AI Content Brain Dump
# Rule: No formatting required. No pressure. Just drop it here.
# This file is read every Monday by the CoS planning ritual.

---

## HOW TO USE THIS

When something happens — a frustration, a win, a thought, something you 
read or watched — open this file and drop one line. That is it.

Do not worry about how it sounds.
Do not try to make it a post yet.
Just capture it before it disappears.

Examples of what belongs here:
- "spent 3 hours on X and the fix was stupidly simple"
- "that podcast mentioned Y and I have been thinking about it all day"
- "tried the new Z repo, it actually works, felt amazing"
- "someone asked me about W and I realised I do not have a good answer"
- "this thing I have been doing is apparently wrong, found out today"

---

## THIS WEEK'S CAPTURE

### Struggles (things that blocked me or frustrated me)
- 

### Wins (things that worked, even small ones)
- 

### Consumed (podcasts, repos, articles, tools that stuck with me)
- 

### Questions (things people asked me, or I asked myself)
- 

### Joy moments (the moment something clicked or worked perfectly)
- 

---

## SUNDAY NIGHT RITUAL (5 minutes max)

Before you close your laptop, answer these three questions.
Do not overthink them. First thought, best thought.

1. What frustrated me most this week and how did I get past it?


2. What actually worked this week that surprised me?


3. What did I consume (watch, read, listen to) that I am still thinking about?


---

## MONDAY HANDOFF TO GEMINI

Copy this block and paste it into Gemini CLI to start the planning ritual:

---
Run the Road4AI weekly content planning ritual.

Here is my inbox from this week (raw + Sunday answers):
[PASTE INBOX CONTENTS HERE]

Using this, plus my existing roadmap, brand voice, and content strategy, please:

1. Parse and understand
   - Parse the sections: Struggles, Wins, Consumed, Questions, Joy moments, and the Sunday Night answers.
   - Treat the Sunday Night answers as higher-priority signals for the coming week.

2. Find the strongest moments
   - Identify the 5 strongest content moments (the ones with a real story or specific insight).
   - For each, briefly explain why you chose it (what makes it compelling).

3. Map to content types, goals, and platforms
   - For each of the 5 moments:
     - Map it to one content type: Struggle / Win / Tutorial / Behind-the-scenes.
     - Suggest a primary platform (e.g. Instagram, X, LinkedIn, YouTube Short) based on the story and my usual content.
     - Suggest the main goal: Build in public / Teach / Nurture / Sell.

4. Write hooks in my voice
   - For each of the 5 moments:
     - Write a one-line hook in my voice (conspiratorial, punchy, personal).
     - Keep it specific to the actual moment (no generic hooks).

5. Update current-queue.json (backlog schema)
   - From the 5 moments, choose the top 3 that best fit my strategy for this week.
   - For each of those 3, add or update an item in state/current-queue.json with at least:
     - "title": a short, clear working title based on the hook
     - "hook": the one-line hook you wrote
     - "type": Struggle / Win / Tutorial / Behind-the-scenes
     - "platform": primary platform you recommend
     - "goal": Build in public / Teach / Nurture / Sell
     - "source": "inbox"
     - "status": "ready_for_drafting"
     - "priority": a number (1 = highest) for this week

   - When choosing these 3, enforce a healthy weekly mix where possible:
     - Aim for at least 1 Struggle, 1 Win, and 1 Tutorial or Behind-the-scenes.
     - If the inbox is very skewed (e.g. all struggles), explain the skew and suggest one balancing idea from my archive or roadmap.

6. Flag experimental ideas
   - From the full inbox, flag anything that could work as an experimental post this week:
     - New format, new angle, or something outside my usual content.
   - List up to 2 experimental ideas, each with:
     - A short description
     - Recommended platform
     - Why it is experimental

7. Confirm the plan
   - Summarise the 3 queued posts for this week in a small table with:
     - Content type, title, platform, goal, and priority.
   - Ask me to confirm or adjust before we move on to drafting.
---

---

## ARCHIVE — Previous Weeks

Move last week's capture here every Monday before starting fresh.
Keep it. These are your content assets, not throwaway notes.

### Week of [DATE]
[paste previous week's capture here]

---
