# Blotato Tool Documentation

## Overview
Blotato is the social media distribution hub for Road4AI. It provides a unified API to schedule and publish content across LinkedIn, X (Twitter), Instagram, Threads, TikTok, and more.

## Key Capabilities
- **Multi-Platform Publishing:** Handles formatting for different platforms (threads, reels, posts).
- **Scheduling:** ISO 8601 based scheduling or "next available slot" queuing.
- **Image Generation:** Generates images from prompts as part of post creation.
- **Source Extraction:** Transcribes YouTube/TikTok videos and scrapes articles to build content sources.

## Integration with Road4AI
- **Operator Agent (Claude Code):** Uses Blotato MCP tools to execute the content queue.
- **Queue System:** Reads from `state/current-queue.json` and writes success logs to `state/published-log.json`.

## MCP Setup
Blotato is connected via HTTP MCP transport. Configured in `.claude/settings.local.json` under `enabledMcpjsonServers`.

```bash
# Add Blotato MCP (already configured)
claude mcp add --transport http blotato https://mcp.blotato.com/mcp --header "blotato-api-key: <KEY>"
```

### Available MCP Tools
- `blotato_create_post` — Create and schedule a post (supports image generation prompts)
- `blotato_list_accounts` — List connected social accounts
- `blotato_create_presigned_upload_url` — Get upload URL for local media files

## Account IDs
Stored in `config/blotato-accounts.json`:
- LinkedIn: 2383
- X/Twitter: 14446
- Instagram: 3879
- Facebook: 3672
- Threads: 1071
- TikTok: 4569
- YouTube: 2813

## Configuration
- API key stored in `.env` as `BLOTATO_API_KEY`.
- Account and platform identifiers fetched via `blotato_list_accounts` or read from `config/blotato-accounts.json`.

## Best Practices
- **Human-in-the-Loop:** Always preview the post content before calling `blotato_create_post`.
- **Image Generation:** Pass an image prompt directly to `blotato_create_post` instead of generating images separately.
- **Media Handling:** For local files, use `blotato_create_presigned_upload_url` before posting.
- **Post-Scheduling Hygiene:** After Blotato confirms scheduling, move the draft to `drafts/archived/` and update queue paths immediately.
