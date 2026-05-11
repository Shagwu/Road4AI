# Blotato Tool Documentation

## Overview
Blotato is the social media distribution hub for Road4AI. It provides a unified API to schedule and publish content across LinkedIn, X (Twitter), Instagram, Threads, TikTok, and more.

## Key Capabilities
- **Multi-Platform Publishing:** Handles formatting for different platforms (threads, reels, posts).
- **Scheduling:** ISO 8601 based scheduling or "next available slot" queuing.
- **Source Extraction:** Transcribes YouTube/TikTok videos and scrapes articles to build content sources.

## Integration with Road4AI
- **Operator Agent (Gemini CLI):** Uses Blotato tools (e.g., `blotato_create_post`) to execute the content queue.
- **Queue System:** Reads from `state/current-queue.json` and writes success logs to `state/published-log.json`.

## Configuration
- Requires `BLOTATO_API_KEY` in the `.env` file.
- Uses `accountId` and `platform` identifiers stored in the agent's memory or fetched via `blotato_list_accounts`.

## Best Practices
- **Human-in-the-Loop:** Always preview the post content before calling `blotato_create_post`.
- **Media Handling:** For local files, use `blotato_create_presigned_upload_url` before posting.
