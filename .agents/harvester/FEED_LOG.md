# Signal Harvester — Feed Test Log

Running record of every RSS feed ever tested for the Signal Harvester.
Append-only. Never delete a row — if a feed is later removed, add a new
row noting removal, don't erase the history.

Applies `HARVESTER_FEED_CRITERIA.md`. One row per feed per test date.

## Log

| Date | Feed Name | URL | HTTP Status | Entries | Last Entry Date | Verdict | Reason | Actioned By |
|---|---|---|---|---|---|---|---|---|
| 2026-07-17 | TechCrunch AI | https://techcrunch.com/category/artificial-intelligence/feed/ | 200 | 18 | 2026-07-16 | Auto-add | Vendor blog, fresh entries, niche AI content | MiMo Auto |
| 2026-07-17 | Ars Technica | https://feeds.arstechnica.com/arstechnica/technology-lab | 200 | 20 | 2026-07-16 | Auto-add | Tech news, broad but high-signal, fresh | MiMo Auto |
| 2026-07-17 | MIT Tech Review | https://www.technologyreview.com/feed/ | 200 | 10 | 2026-07-16 | Auto-add | Research-backed AI coverage, fresh | MiMo Auto |
| 2026-07-17 | Hugging Face Blog | https://huggingface.co/blog/feed.xml | 200 | 829 | 2026-07-15 | Pass (soft: volume filter) | Vendor blog, high volume, needs ingestion-side date filter | MiMo Auto |
| 2026-07-17 | Ollama Blog | https://ollama.com/blog/rss.xml | 200 | 54 | 2026-07-09 | Auto-add | Vendor blog, unambiguous niche fit, fresh | MiMo Auto |
| 2026-07-17 | AI Alignment Forum | https://www.alignmentforum.org/feed.xml | 200 | 10 | 2026-07-15 | Auto-add | AI safety/governance research, fresh, niche fit | MiMo Auto |
| 2026-07-17 | LessWrong AI | https://www.lesswrong.com/feed.xml?view=ai | 200 | 10 | 2026-07-17 | Auto-add | AI research discussion, fresh, niche fit | MiMo Auto |
| 2026-07-17 | AI News (Synced) | https://syncedreview.com/feed/ | 200 | 10 | 2025-05-28 | Hold (soft: relevance + staleness) | Broad AI news, last entry May 2025, not niche/local-LLM — needs CoS call | MiMo Auto |
| 2026-07-17 | Llama Meta AI | https://ai.meta.com/blog/rss/ | 404 | 0 | — | Hard reject | Dead endpoint | MiMo Auto |
| 2026-07-17 | LangChain Blog | https://blog.langchain.dev/rss/ | 200 | 0 | — | Hard reject | Empty feed | MiMo Auto |
| 2026-07-17 | LlamaIndex Blog | https://www.llamaindex.ai/blog/rss.xml | 404 | 0 | — | Hard reject | Dead endpoint | MiMo Auto |
| 2026-07-17 | The Batch (DeepLearning.AI) | https://www.deeplearning.ai/the-batch/feed/ | 404 | 0 | — | Hard reject | Dead endpoint | MiMo Auto |
| 2026-07-17 | Anthropic Research | https://www.anthropic.com/rss.xml | 404 | 0 | — | Hard reject | Dead endpoint | MiMo Auto |
| 2026-07-17 | LocalLLaMA (Reddit) | https://www.reddit.com/r/LocalLLaMA/top/.rss?t=day | 403 | 0 | — | Hard reject | Auth required (OAuth) — logged as Phase 5 RFC candidate | MiMo Auto |
| 2026-07-17 | r/MachineLearning (Reddit) | https://www.reddit.com/r/MachineLearning/top/.rss?t=day | 403 | 0 | — | Hard reject | Auth required (OAuth) | MiMo Auto |
| 2026-07-17 | Papers With Code | https://paperswithcode.com/rss | 200 | 0 | — | Hard reject | Empty, feed format likely changed | MiMo Auto |
| 2026-07-17 | Open Source AI | https://opensource.ai/rss.xml | ERR | — | — | Hard reject | Connection failure, domain likely dead | MiMo Auto |

## Active Feeds (passed hard gates)

| Feed | Last Entry Date | Status |
|---|---|---|
| TechCrunch AI | 2026-07-16 | Active |
| Ars Technica | 2026-07-16 | Active |
| MIT Tech Review | 2026-07-16 | Active |
| Hugging Face Blog | 2026-07-15 | Active (volume filter needed) |
| Ollama Blog | 2026-07-09 | Active |
| AI Alignment Forum | 2026-07-15 | Active |
| LessWrong AI | 2026-07-17 | Active |

## Blocked / Deferred

| Feed | Reason | RFC Status |
|---|---|---|
| Reddit (r/LocalLLaMA, r/MachineLearning) | 403 auth required | Phase 5 RFC candidate |
| Synced AI News | Broad coverage, staleness (>1 year old entries) | Pending CoS call |

## Column notes

- **Entries**: raw count from the test pull, not a filtered/deduped count.
- **Last Entry Date**: newest entry's published date, used for the 30-day
  staleness hard gate. Captured via `last_entry_date` field in signal output.
- **Verdict**: one of `Auto-add`, `Pass (soft: <reason>)`, `Hold (soft: <reason>)`,
  `Hard reject`, `Removed`.
- **Actioned By**: agent or person who made the call — keeps the audit
  trail consistent with the rest of the governance docs (Karen findings,
  retroactive audits, etc.).
