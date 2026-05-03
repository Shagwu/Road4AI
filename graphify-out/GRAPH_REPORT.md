# Graph Report - /Users/shagwu/Downloads/Road4AI-main  (2026-05-03)

## Corpus Check
- 90 files · ~492,015 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 436 nodes · 572 edges · 78 communities detected
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 80 edges (avg confidence: 0.79)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]

## God Nodes (most connected - your core abstractions)
1. `MemoryBridgeV2` - 24 edges
2. `MemoryBridge` - 9 edges
3. `main()` - 7 edges
4. `parse_args()` - 7 edges
5. `remove_mcp()` - 7 edges
6. `test_v2_archive_expired_is_idempotent()` - 7 edges
7. `test_v2_prune_archived_is_idempotent()` - 7 edges
8. `ollama_chat()` - 6 edges
9. `_lookup_cost()` - 6 edges
10. `_preset_path()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `parse_args()`  [INFERRED]
  /Users/shagwu/Downloads/Road4AI-main/karen.py → /Users/shagwu/Downloads/Road4AI-main/verify_repo.py
- `parse_args()` --calls--> `main()`  [INFERRED]
  /Users/shagwu/Downloads/Road4AI-main/verify_repo.py → /Users/shagwu/Downloads/Road4AI-main/banana-claude/skills/banana/scripts/cost_tracker.py
- `parse_args()` --calls--> `main()`  [INFERRED]
  /Users/shagwu/Downloads/Road4AI-main/verify_repo.py → /Users/shagwu/Downloads/Road4AI-main/banana-claude/skills/banana/scripts/presets.py
- `Performs a strict 8-step audit on a content draft using the local Karen pipeline` --uses--> `MemoryBridgeV2`  [INFERRED]
  /Users/shagwu/Downloads/Road4AI-main/road4ai-cos/app/tools.py → /Users/shagwu/Downloads/Road4AI-main/hermes/bridge_v2.py
- `Updates the master COS_REPORT.md file with the latest status.          Args:` --uses--> `MemoryBridgeV2`  [INFERRED]
  /Users/shagwu/Downloads/Road4AI-main/road4ai-cos/app/tools.py → /Users/shagwu/Downloads/Road4AI-main/hermes/bridge_v2.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (25): estimate_cost(), main(), Estimate cost for a single image., main(), edit_image(), main(), Call Gemini API to edit an image., generate_image() (+17 more)

### Community 1 - "Community 1"
Cohesion: 0.14
Nodes (16): MemoryBridgeV2, Configure OpenTelemetry and GenAI telemetry with GCS upload., setup_telemetry(), _iso_utc(), test_v2_archive_expired_is_idempotent(), test_v2_lifecycle(), test_v2_prune_archived_is_idempotent(), test_v2_search() (+8 more)

### Community 2 - "Community 2"
Cohesion: 0.2
Nodes (14): cmd_create(), cmd_delete(), cmd_list(), cmd_show(), _ensure_dir(), _load_preset(), _preset_path(), Ensure presets directory exists. (+6 more)

### Community 3 - "Community 3"
Cohesion: 0.15
Nodes (14): log_output(), Test the chat stream functionality., Test the chat stream error handling., Test the feedback collection endpoint (/feedback) to ensure it properly     logs, Log the output from the given pipe., Start the FastAPI server using subprocess and log its output., Wait for the server to be ready., Pytest fixture to start and stop the server for testing. (+6 more)

### Community 4 - "Community 4"
Cohesion: 0.22
Nodes (13): check_ollama_available(), get_staged_diff(), main(), ollama_chat(), post_to_pr(), Call the local Ollama /api/generate endpoint.     Uses only stdlib (urllib) — no, Warn early if Ollama isn't reachable or the model isn't pulled., Get the staged git diff. Returns None if nothing is staged. (+5 more)

### Community 5 - "Community 5"
Cohesion: 0.23
Nodes (6): get_today_task(), main(), update_status(), MemoryBridge, test_memory_persistence_lifecycle(), test_memory_semantic_search()

### Community 6 - "Community 6"
Cohesion: 0.22
Nodes (13): cmd_estimate(), cmd_log(), cmd_reset(), cmd_summary(), cmd_today(), _load_ledger(), _lookup_cost(), Estimate cost for a batch. (+5 more)

### Community 7 - "Community 7"
Cohesion: 0.29
Nodes (5): BaseModel, collect_feedback(), Collect and log feedback.      Args:         feedback: The feedback data to log, Feedback, Represents feedback for a conversation.

### Community 8 - "Community 8"
Cohesion: 0.33
Nodes (4): get_current_time(), get_weather(), Simulates a web search. Use it get information on weather.      Args:         qu, Simulates getting the current time for a city.      Args:         city: The name

### Community 9 - "Community 9"
Cohesion: 0.53
Nodes (4): ingestApi(), main(), queryApi(), queryApiPost()

### Community 10 - "Community 10"
Cohesion: 0.6
Nodes (4): api(), daysToDateRange(), gaql(), main()

### Community 11 - "Community 11"
Cohesion: 0.7
Nodes (4): check_local_memory(), check_mcp_status(), check_zero_cost_integrity(), run_health_check()

### Community 12 - "Community 12"
Cohesion: 0.6
Nodes (3): ingestApi(), main(), queryApi()

### Community 13 - "Community 13"
Cohesion: 0.6
Nodes (3): appApi(), main(), trackApi()

### Community 14 - "Community 14"
Cohesion: 0.6
Nodes (3): api(), getDefaultDates(), main()

### Community 15 - "Community 15"
Cohesion: 0.6
Nodes (3): api(), buildQuery(), main()

### Community 16 - "Community 16"
Cohesion: 0.6
Nodes (3): api(), getToken(), main()

### Community 17 - "Community 17"
Cohesion: 0.6
Nodes (3): api(), getToken(), main()

### Community 18 - "Community 18"
Cohesion: 0.7
Nodes (3): api(), authenticate(), main()

### Community 19 - "Community 19"
Cohesion: 0.6
Nodes (3): api(), main(), webhookPost()

### Community 20 - "Community 20"
Cohesion: 0.6
Nodes (3): api(), getAccessToken(), main()

### Community 21 - "Community 21"
Cohesion: 0.6
Nodes (3): api(), main(), parseCSV()

### Community 22 - "Community 22"
Cohesion: 0.6
Nodes (3): main(), profileApi(), trackApi()

### Community 23 - "Community 23"
Cohesion: 0.6
Nodes (3): api(), getAccountId(), main()

### Community 24 - "Community 24"
Cohesion: 0.6
Nodes (3): api(), buildQuery(), main()

### Community 25 - "Community 25"
Cohesion: 0.6
Nodes (3): api(), getAdvertiserId(), main()

### Community 26 - "Community 26"
Cohesion: 0.6
Nodes (3): api(), main(), mpApi()

### Community 27 - "Community 27"
Cohesion: 0.5
Nodes (2): api(), main()

### Community 28 - "Community 28"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 29 - "Community 29"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 30 - "Community 30"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 31 - "Community 31"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 32 - "Community 32"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 33 - "Community 33"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 34 - "Community 34"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 35 - "Community 35"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 36 - "Community 36"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 37 - "Community 37"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 38 - "Community 38"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 39 - "Community 39"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 40 - "Community 40"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 41 - "Community 41"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 42 - "Community 42"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 43 - "Community 43"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 44 - "Community 44"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 45 - "Community 45"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 46 - "Community 46"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 47 - "Community 47"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 48 - "Community 48"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 49 - "Community 49"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 50 - "Community 50"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 51 - "Community 51"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 52 - "Community 52"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 53 - "Community 53"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 54 - "Community 54"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 55 - "Community 55"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 56 - "Community 56"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 57 - "Community 57"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 58 - "Community 58"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 59 - "Community 59"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 60 - "Community 60"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 61 - "Community 61"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 62 - "Community 62"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 63 - "Community 63"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 64 - "Community 64"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 65 - "Community 65"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 66 - "Community 66"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 67 - "Community 67"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 68 - "Community 68"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 69 - "Community 69"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 70 - "Community 70"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 71 - "Community 71"
Cohesion: 0.67
Nodes (2): process_data(), Safely retrieves the first element from a sequence.          Args:         data:

### Community 72 - "Community 72"
Cohesion: 0.67
Nodes (2): Placeholder - replace with real tests., test_dummy()

### Community 73 - "Community 73"
Cohesion: 0.67
Nodes (2): Integration test for the agent stream functionality.     Tests that the agent re, test_agent_stream()

### Community 74 - "Community 74"
Cohesion: 1.0
Nodes (0): 

### Community 75 - "Community 75"
Cohesion: 1.0
Nodes (0): 

### Community 76 - "Community 76"
Cohesion: 1.0
Nodes (0): 

### Community 77 - "Community 77"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **39 isolated node(s):** `Call the local Ollama /api/generate endpoint.     Uses only stdlib (urllib) — no`, `Warn early if Ollama isn't reachable or the model isn't pulled.`, `Get the staged git diff. Returns None if nothing is staged.`, `Send the diff to the local adversary model. Returns raw accusations.`, `Apply Karen's 8-step filter to the adversary's accusations.` (+34 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 74`** (2 nodes): `get_status()`, `road4ai_v3.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 75`** (1 nodes): `main.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 76`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 77`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `cmd_list()` connect `Community 2` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Why does `wait_for_server()` connect `Community 3` to `Community 1`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `MemoryBridgeV2` (e.g. with `Performs a strict 8-step audit on a content draft using the local Karen pipeline` and `Updates the master COS_REPORT.md file with the latest status.          Args:`) actually correct?**
  _`MemoryBridgeV2` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `MemoryBridge` (e.g. with `test_memory_persistence_lifecycle()` and `test_memory_semantic_search()`) actually correct?**
  _`MemoryBridge` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `parse_args()` (e.g. with `main()` and `main()`) actually correct?**
  _`parse_args()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `remove_mcp()` (e.g. with `.get()` and `.get()`) actually correct?**
  _`remove_mcp()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Call the local Ollama /api/generate endpoint.     Uses only stdlib (urllib) — no`, `Warn early if Ollama isn't reachable or the model isn't pulled.`, `Get the staged git diff. Returns None if nothing is staged.` to the rest of the system?**
  _39 weakly-connected nodes found - possible documentation gaps or missing edges._