# Signal Harvester — Feed Test Log

Running record of every RSS feed ever tested for the Signal Harvester.
Append-only. Never delete a row — if a feed is later removed, add a new
row noting removal, don't erase the history.

Applies `HARVESTER_FEED_CRITERIA.md`. One row per feed per test date.

## Log

| Date | Feed Name | URL | HTTP Status | Entries | Last Entry Date | Verdict | Reason | Actioned By |
|---|---|---|---|---|---|---|---|---|
| 2026-07-17 | Hugging Face Blog | https://huggingface.co/blog/feed.xml | 200 | 829 | — | Pass (soft: volume filter) | Vendor blog, high volume, needs ingestion-side date filter | MiMo Auto |
| 2026-07-17 | Ollama Blog | https://ollama.com/blog/rss.xml | 200 | 54 | — | Auto-add | Vendor blog, unambiguous niche fit | MiMo Auto |
| 2026-07-17 | AI News (Synced) | https://syncedreview.com/feed/ | 200 | 10 | — | Hold (soft: relevance) | Broad AI news, not niche/local-LLM — needs CoS call | MiMo Auto |
| 2026-07-17 | Llama Meta AI | https://ai.meta.com/blog/rss/ | 404 | 0 | — | Hard reject | Dead endpoint | MiMo Auto |
| 2026-07-17 | LangChain Blog | https://blog.langchain.dev/rss/ | 200 | 0 | — | Hard reject | Empty feed | MiMo Auto |
| 2026-07-17 | LlamaIndex Blog | https://www.llamaindex.ai/blog/rss.xml | 404 | 0 | — | Hard reject | Dead endpoint | MiMo Auto |
| 2026-07-17 | LocalLLaMA (Reddit) | https://www.reddit.com/r/LocalLLaMA/top/.rss?t=day | 403 | 0 | — | Hard reject | Auth required (OAuth) — logged as Phase 5 RFC candidate | MiMo Auto |
| 2026-07-17 | r/MachineLearning (Reddit) | https://www.reddit.com/r/MachineLearning/top/.rss?t=day | 403 | 0 | — | Hard reject | Auth required (OAuth) | MiMo Auto |
| 2026-07-17 | Papers With Code | https://paperswithcode.com/rss | 200 | 0 | — | Hard reject | Empty, feed format likely changed | MiMo Auto |
| 2026-07-17 | Open Source AI | https://opensource.ai/rss.xml | ERR | — | — | Hard reject | Connection failure, domain likely dead | MiMo Auto |

## Untested (pending)

Feeds mentioned but not yet run through the test script:

- AI Alignment Forum — https://www.alignmentforum.org/feed.xml
- LessWrong AI — https://www.lesswrong.com/feed.xml?view=ai
- The Batch (DeepLearning.AI) — https://www.deeplearning.ai/the-batch/feed/
- Anthropic Research — https://www.anthropic.com/rss.xml

## Column notes

- **Entries**: raw count from the test pull, not a filtered/deduped count.
- **Last Entry Date**: newest entry's published date, used for the 30-day
  staleness hard gate. Fill in on next test pass — today's run didn't
  capture this field, worth re-running with it included.
- **Verdict**: one of `Auto-add`, `Pass (soft: <reason>)`, `Hold (soft: <reason>)`,
  `Hard reject`, `Removed`.
- **Actioned By**: agent or person who made the call — keeps the audit
  trail consistent with the rest of the governance docs (Karen findings,
  retroactive audits, etc.).
