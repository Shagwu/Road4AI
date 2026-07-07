---
id: 2026-05-11-triage-win-li
title: From 0% to 100%: The Triage Win
type: Win
platform: LinkedIn
goal: build_in_public
hook: Last week, my incident triage agent was hallucinating 40% of the root causes. This morning, it hit a 100% pass rate on the evaluation suite.
status: ready_for_publishing
karen_verdict: APPROVED (after audit)
scheduled: true
---

# From 0% to 100%: The Triage Win

Building agents that "work sometimes" is easy. Building agents that hit a 100% pass rate on a production evaluation suite is engineering.

Last Monday, I was ready to scrap the Incident Triage agent. It would look at a stack trace, guess a root cause, and hallucinate 4 out of 10 times.

The fix wasn't a better prompt. It was better **Evaluation**.

I stopped building the agent and started building the test. I created an eval suite (a "gold set") of 50 historic incidents—real production failures with known fixes.

I ran the agent through the suite and watched it fail. Then I used the **ADK (Agent Development Kit)** to add a mandatory "Log Inspection" tool and a "Pattern Matcher" callback.

The results:
- **Phase 1:** 60% accuracy (Baseline)
- **Phase 2:** 85% accuracy (Added context windows)
- **Phase 3:** 100% pass rate on the 50-incident gold set.

The lesson: You don't "improve" an agent. You constrain it until the objective function is the only path forward.

If you aren't running your agents against a ground-truth eval set, you're not building software. You're just hoping.

#AI #Engineering #Reliability #BuildInPublic #ADK
