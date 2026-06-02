# Graph Report - /Users/shagwu/Downloads/Road4AI-main  (2026-06-02)

## Corpus Check
- 115 files · ~550,037 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 647 nodes · 946 edges · 98 communities detected
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 163 edges (avg confidence: 0.75)
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
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]
- [[_COMMUNITY_Community 90|Community 90]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 95|Community 95]]
- [[_COMMUNITY_Community 96|Community 96]]
- [[_COMMUNITY_Community 97|Community 97]]

## God Nodes (most connected - your core abstractions)
1. `MemoryBridgeV2` - 48 edges
2. `BenchmarkRunner` - 35 edges
3. `BenchmarkRunner` - 25 edges
4. `LLMCapture` - 11 edges
5. `HermesStorage` - 11 edges
6. `SkillOptClient` - 10 edges
7. `make_repo()` - 10 edges
8. `parse_args()` - 9 edges
9. `AgentEngineApp` - 9 edges
10. `Feedback` - 9 edges

## Surprising Connections (you probably didn't know these)
- `MemoryBridgeV2` --uses--> `Performs a strict 8-step audit on a content draft using the local Karen pipeline`  [INFERRED]
  /Users/shagwu/Downloads/Road4AI-main/road4ai-hermes/src/road4ai_hermes/bridge.py → /Users/shagwu/Downloads/Road4AI-main/road4ai-cos/app/tools.py
- `MemoryBridgeV2` --uses--> `Updates the master COS_REPORT.md file with the latest status.          Args:`  [INFERRED]
  /Users/shagwu/Downloads/Road4AI-main/road4ai-hermes/src/road4ai_hermes/bridge.py → /Users/shagwu/Downloads/Road4AI-main/road4ai-cos/app/tools.py
- `main()` --calls--> `parse_args()`  [INFERRED]
  /Users/shagwu/Downloads/Road4AI-main/karen.py → /Users/shagwu/Downloads/Road4AI-main/verify_repo.py
- `parse_args()` --calls--> `main()`  [INFERRED]
  /Users/shagwu/Downloads/Road4AI-main/verify_repo.py → /Users/shagwu/Downloads/Road4AI-main/banana-claude/skills/banana/scripts/cost_tracker.py
- `parse_args()` --calls--> `main()`  [INFERRED]
  /Users/shagwu/Downloads/Road4AI-main/verify_repo.py → /Users/shagwu/Downloads/Road4AI-main/banana-claude/skills/banana/scripts/presets.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (28): BaseKnowledgeStorage, MemoryBridgeV2, HermesStorage, Saves a chunk of knowledge to the Hermes v2.0 substrate., Retrieves relevant context from the Hermes v2.0 substrate., Deletes specific entries from the substrate.         Note: Hermes V2 wrapper for, Resets the entire collection. DANGEROUS: use with caution., HermesStorage is the integration bridge. It inherits from CrewAI's BaseKnowledge (+20 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (13): BenchmarkRunner, main(), UsageSnapshot, make_repo(), test_dry_run_writes_validation_report(), test_live_mode_requires_usage_pricing_models_and_key(), test_non_skill_markdown_is_rejected(), test_pricing_model_validation() (+5 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (14): LLMCapture, Lightweight LLM wrapper that optionally captures conversations to Hermes v2 brid, Run a chat completion and optionally capture the conversation to Hermes bridge., Record a user<->AI conversation as a memory.          Parameters:         - user, Best-effort persistence/flush for underlying Chroma client if supported., demo(), example_initialize_bridge(), HermesMemoryTool (+6 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (18): AdkApp, AgentEngineApp, Initialize the agent engine app with logging and telemetry., Collect and log feedback., Registers the operations of the Agent., BaseModel, collect_feedback(), Collect and log feedback.      Args:         feedback: The feedback data to log (+10 more)

### Community 4 - "Community 4"
Cohesion: 0.16
Nodes (3): BenchmarkRunner, main(), UsageSnapshot

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (16): SelfIndexer, check_ollama_available(), get_staged_diff(), main(), ollama_chat(), post_to_pr(), Call the local Ollama /api/generate endpoint.     Uses only stdlib (urllib) — no, Warn early if Ollama isn't reachable or the model isn't pulled. (+8 more)

### Community 6 - "Community 6"
Cohesion: 0.13
Nodes (12): create_skillopt_client(), SkillOpt API Client: OpenAI Standard Implementation  Drop-in replacement for Ski, Evaluate skill on test cases using target model.                  Args:, Build prompt for skill optimizer., Build prompt for agent rollout., Simple scoring: check if expected answer is in output., Parse optimizer response into structured edits., Unified client for SkillOpt training with OpenAI or Azure endpoints. (+4 more)

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (12): estimate_cost(), main(), Estimate cost for a single image., main(), edit_image(), main(), Call Gemini API to edit an image., generate_image() (+4 more)

### Community 8 - "Community 8"
Cohesion: 0.2
Nodes (14): cmd_create(), cmd_delete(), cmd_list(), cmd_show(), _ensure_dir(), _load_preset(), _preset_path(), Ensure presets directory exists. (+6 more)

### Community 9 - "Community 9"
Cohesion: 0.15
Nodes (14): log_output(), Test the chat stream functionality., Test the chat stream error handling., Test the feedback collection endpoint (/feedback) to ensure it properly     logs, Log the output from the given pipe., Start the FastAPI server using subprocess and log its output., Wait for the server to be ready., Pytest fixture to start and stop the server for testing. (+6 more)

### Community 10 - "Community 10"
Cohesion: 0.22
Nodes (13): cmd_estimate(), cmd_log(), cmd_reset(), cmd_summary(), cmd_today(), _load_ledger(), _lookup_cost(), Estimate cost for a batch. (+5 more)

### Community 11 - "Community 11"
Cohesion: 0.29
Nodes (11): check_setup(), load_settings(), main(), Load Claude Code settings.json., Save Claude Code settings.json., Check if MCP is already configured., Remove MCP configuration., Configure MCP server in Claude Code settings. (+3 more)

### Community 12 - "Community 12"
Cohesion: 0.2
Nodes (8): Stand-in for the AIDefence sanitization layer.     In the real deployment, this, sanitize_input(), karen_audit(), Scans input text for PII (names, emails, keys) and AI threats (prompt injection), Performs a strict 8-step audit on a content draft using the local Karen pipeline, Updates the master COS_REPORT.md file with the latest status.          Args:, sanitization_gate(), sync_dashboard()

### Community 13 - "Community 13"
Cohesion: 0.31
Nodes (7): get_recent_commits(), _github_request(), Reads the content of a file from GitHub.          Args:         repo: Repository, Searches for code in GitHub repositories.          Args:         query: The sear, Gets recent commits for a repository or a specific file.          Args:, read_github_file(), search_github_code()

### Community 14 - "Community 14"
Cohesion: 0.38
Nodes (5): get_today_task(), main(), update_status(), file_lock(), Simple file-based advisory lock to prevent race conditions in swarms.

### Community 15 - "Community 15"
Cohesion: 0.33
Nodes (4): get_current_time(), get_weather(), Simulates a web search. Use it get information on weather.      Args:         qu, Simulates getting the current time for a city.      Args:         city: The name

### Community 16 - "Community 16"
Cohesion: 0.53
Nodes (4): ingestApi(), main(), queryApi(), queryApiPost()

### Community 17 - "Community 17"
Cohesion: 0.6
Nodes (4): api(), daysToDateRange(), gaql(), main()

### Community 18 - "Community 18"
Cohesion: 0.7
Nodes (4): check_local_memory(), check_mcp_status(), check_zero_cost_integrity(), run_health_check()

### Community 19 - "Community 19"
Cohesion: 0.7
Nodes (4): check_json_integrity(), check_queue_consistency(), check_x_draft_length(), main()

### Community 20 - "Community 20"
Cohesion: 0.6
Nodes (3): ingestApi(), main(), queryApi()

### Community 21 - "Community 21"
Cohesion: 0.6
Nodes (3): appApi(), main(), trackApi()

### Community 22 - "Community 22"
Cohesion: 0.6
Nodes (3): api(), getDefaultDates(), main()

### Community 23 - "Community 23"
Cohesion: 0.6
Nodes (3): api(), buildQuery(), main()

### Community 24 - "Community 24"
Cohesion: 0.6
Nodes (3): api(), getToken(), main()

### Community 25 - "Community 25"
Cohesion: 0.6
Nodes (3): api(), getToken(), main()

### Community 26 - "Community 26"
Cohesion: 0.7
Nodes (3): api(), authenticate(), main()

### Community 27 - "Community 27"
Cohesion: 0.6
Nodes (3): api(), main(), webhookPost()

### Community 28 - "Community 28"
Cohesion: 0.6
Nodes (3): api(), getAccessToken(), main()

### Community 29 - "Community 29"
Cohesion: 0.6
Nodes (3): api(), main(), parseCSV()

### Community 30 - "Community 30"
Cohesion: 0.6
Nodes (3): main(), profileApi(), trackApi()

### Community 31 - "Community 31"
Cohesion: 0.6
Nodes (3): api(), getAccountId(), main()

### Community 32 - "Community 32"
Cohesion: 0.6
Nodes (3): api(), buildQuery(), main()

### Community 33 - "Community 33"
Cohesion: 0.6
Nodes (3): api(), getAdvertiserId(), main()

### Community 34 - "Community 34"
Cohesion: 0.6
Nodes (3): api(), main(), mpApi()

### Community 35 - "Community 35"
Cohesion: 0.5
Nodes (2): api(), main()

### Community 36 - "Community 36"
Cohesion: 0.5
Nodes (2): Placeholder - replace with real tests., test_dummy()

### Community 37 - "Community 37"
Cohesion: 0.83
Nodes (3): check_file(), check_json(), main()

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
Nodes (2): api(), main()

### Community 72 - "Community 72"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 73 - "Community 73"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 74 - "Community 74"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 75 - "Community 75"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 76 - "Community 76"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 77 - "Community 77"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 78 - "Community 78"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 79 - "Community 79"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 80 - "Community 80"
Cohesion: 0.67
Nodes (2): api(), main()

### Community 81 - "Community 81"
Cohesion: 0.67
Nodes (2): process_data(), Safely retrieves the first element from a sequence.          Args:         data:

### Community 82 - "Community 82"
Cohesion: 1.0
Nodes (2): check(), main()

### Community 83 - "Community 83"
Cohesion: 1.0
Nodes (0): 

### Community 84 - "Community 84"
Cohesion: 1.0
Nodes (0): 

### Community 85 - "Community 85"
Cohesion: 1.0
Nodes (0): 

### Community 86 - "Community 86"
Cohesion: 1.0
Nodes (0): 

### Community 87 - "Community 87"
Cohesion: 1.0
Nodes (1): HermesStorage is the integration bridge. It inherits from CrewAI's BaseKnowledge

### Community 88 - "Community 88"
Cohesion: 1.0
Nodes (1): Saves a chunk of knowledge to the Hermes v2.0 substrate.

### Community 89 - "Community 89"
Cohesion: 1.0
Nodes (1): Retrieves relevant context from the Hermes v2.0 substrate.

### Community 90 - "Community 90"
Cohesion: 1.0
Nodes (1): Deletes specific entries from the substrate.         Note: Hermes V2 wrapper for

### Community 91 - "Community 91"
Cohesion: 1.0
Nodes (1): Resets the entire collection. DANGEROUS: use with caution.

### Community 92 - "Community 92"
Cohesion: 1.0
Nodes (1): Call the local Ollama /api/generate endpoint.     Uses only stdlib (urllib) — no

### Community 93 - "Community 93"
Cohesion: 1.0
Nodes (1): Warn early if Ollama isn't reachable or the model isn't pulled.

### Community 94 - "Community 94"
Cohesion: 1.0
Nodes (1): Get the staged git diff. Returns None if nothing is staged.

### Community 95 - "Community 95"
Cohesion: 1.0
Nodes (1): Send the diff to the local adversary model. Returns raw accusations.

### Community 96 - "Community 96"
Cohesion: 1.0
Nodes (1): Apply Karen's 8-step filter to the adversary's accusations.

### Community 97 - "Community 97"
Cohesion: 1.0
Nodes (1): Post Karen's verdict as a comment on the current open PR via GitHub CLI.

## Knowledge Gaps
- **70 isolated node(s):** `Call the local Ollama /api/generate endpoint.     Uses only stdlib (urllib) — no`, `Warn early if Ollama isn't reachable or the model isn't pulled.`, `Get the staged git diff. Returns None if nothing is staged.`, `Send the diff to the local adversary model. Returns raw accusations.`, `Apply Karen's 8-step filter to the adversary's accusations.` (+65 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 83`** (2 nodes): `get_status()`, `road4ai_v3.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 84`** (1 nodes): `main.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 85`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 86`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 87`** (1 nodes): `HermesStorage is the integration bridge. It inherits from CrewAI's BaseKnowledge`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 88`** (1 nodes): `Saves a chunk of knowledge to the Hermes v2.0 substrate.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 89`** (1 nodes): `Retrieves relevant context from the Hermes v2.0 substrate.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 90`** (1 nodes): `Deletes specific entries from the substrate.         Note: Hermes V2 wrapper for`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 91`** (1 nodes): `Resets the entire collection. DANGEROUS: use with caution.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 92`** (1 nodes): `Call the local Ollama /api/generate endpoint.     Uses only stdlib (urllib) — no`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 93`** (1 nodes): `Warn early if Ollama isn't reachable or the model isn't pulled.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 94`** (1 nodes): `Get the staged git diff. Returns None if nothing is staged.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 95`** (1 nodes): `Send the diff to the local adversary model. Returns raw accusations.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 96`** (1 nodes): `Apply Karen's 8-step filter to the adversary's accusations.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 97`** (1 nodes): `Post Karen's verdict as a comment on the current open PR via GitHub CLI.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MemoryBridgeV2` connect `Community 0` to `Community 2`, `Community 12`, `Community 5`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `cmd_list()` connect `Community 8` to `Community 0`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `MemoryBridgeV2` (e.g. with `Test how MemoryBridgeV2 handles conflicting writes to the same ID.          @kno` and `Test that retrieval order remains stable for identical distances.     @known_lim`) actually correct?**
  _`MemoryBridgeV2` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `BenchmarkRunner` (e.g. with `test_dry_run_writes_validation_report()` and `test_protected_file_is_rejected()`) actually correct?**
  _`BenchmarkRunner` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `LLMCapture` (e.g. with `DummyResponse` and `DummyOpenAI`) actually correct?**
  _`LLMCapture` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `HermesStorage` (e.g. with `MemoryBridgeV2` and `test_hermes_storage_lifecycle()`) actually correct?**
  _`HermesStorage` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Call the local Ollama /api/generate endpoint.     Uses only stdlib (urllib) — no`, `Warn early if Ollama isn't reachable or the model isn't pulled.`, `Get the staged git diff. Returns None if nothing is staged.` to the rest of the system?**
  _70 weakly-connected nodes found - possible documentation gaps or missing edges._