#!/usr/bin/env python3
"""Schedule a Road4AI post via Blotato MCP.

Usage:
  python tools/schedule_post.py drafts/approved/post-li.md
  python tools/schedule_post.py drafts/approved/post.md --platform li,x,ig
  python tools/schedule_post.py drafts/approved/post.md --all --yes
  python tools/schedule_post.py drafts/approved/post.md --schedule "2026-06-28T09:00:00Z"
  python tools/schedule_post.py drafts/approved/post.md --schedule "+2h"
  python tools/schedule_post.py drafts/approved/post.md --next-slot
  python tools/schedule_post.py --check drafts/ready/post.md
  python tools/schedule_post.py --list

Guardrails:
  - Draft must be in drafts/approved/ (use --force to override)
  - Karen verdict must be APPROVED in frontmatter (use --force to override)
"""

import json
import re
import sys
import os
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

PLATFORMS = {
    "li": ("2383", "linkedin"),
    "x": ("14446", "twitter"),
    "ig": ("3879", "instagram"),
    "fb": ("3672", "facebook"),
    "threads": ("1071", "threads"),
    "tt": ("4569", "tiktok"),
}

MCP_ENDPOINT = "https://mcp.blotato.com/mcp"


def load_api_key():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("BLOTATO_API_KEY="):
                val = line.split("=", 1)[1].strip()
                if val and not val.startswith("#"):
                    return val
    return os.environ.get("BLOTATO_API_KEY", "")


def parse_frontmatter(content):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip()
    return fm


def check_guardrails(filepath, force=False):
    content = Path(filepath).read_text()
    fm = parse_frontmatter(content)
    rel = str(filepath)

    issues = []

    if not force:
        if "drafts/approved/" not in rel and "drafts/archived/" not in rel:
            issues.append(f"NOT in drafts/approved/ or drafts/approved/: {rel}")
            issues.append("Content must be in drafts/approved/ before scheduling. User must approve first.")

        karen = fm.get("karen_verdict", "")
        if "APPROVED" not in karen.upper():
            issues.append(f"Karen verdict missing or not APPROVED: {karen or '(none)'}")

    return fm, issues


def parse_schedule(value):
    if not value:
        return None

    now = datetime.now(timezone.utc)

    if value.startswith("+"):
        match = re.match(r"\+(\d+)([hm])", value)
        if match:
            amount = int(match.group(1))
            unit = match.group(2)
            delta = timedelta(hours=amount) if unit == "h" else timedelta(minutes=amount)
            return (now + delta).isoformat()

    if value.startswith("-"):
        match = re.match(r"-(\d+)([hm])", value)
        if match:
            amount = int(match.group(1))
            unit = match.group(2)
            delta = timedelta(hours=amount) if unit == "h" else timedelta(minutes=amount)
            return (now - delta).isoformat()

    if value.lower() == "tomorrow":
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=9, minute=0, second=0, microsecond=0).isoformat()

    match = re.match(r"tomorrow-(\d+)h", value.lower())
    if match:
        hour = int(match.group(1))
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=hour, minute=0, second=0, microsecond=0).isoformat()

    match = re.match(r"(\d+)-(\d+)h", value.lower())
    if match:
        days = int(match.group(1))
        hour = int(match.group(2))
        target = now + timedelta(days=days)
        return target.replace(hour=hour, minute=0, second=0, microsecond=0).isoformat()

    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.isoformat()
    except ValueError:
        pass

    print(f"Cannot parse schedule time: {value}")
    print("Examples: 2026-06-28T09:00:00Z, +2h, +30m, tomorrow, tomorrow-14h, 2-9h")
    sys.exit(1)


def parse_draft(filepath):
    content = Path(filepath).read_text()

    image_prompt = ""
    # Match bold format: **Blotato image prompt:**
    prompt_match = re.search(
        r"\*\*Blotato image prompt:\*\*\s*\n(.+?)(?=\n---|\n\n#|\n\n\*\*)",
        content,
        re.DOTALL,
    )
    if prompt_match:
        image_prompt = prompt_match.group(1).strip()
    # Match heading format: ## Image Prompt ...
    if not image_prompt:
        heading_match = re.search(
            r"^##\s+Image Prompt.*\n(.+?)(?=\n---|\n\n##|\n\n#|\Z)",
            content,
            re.MULTILINE | re.DOTALL,
        )
        if heading_match:
            image_prompt = heading_match.group(1).strip()

    lines = content.split("\n")
    start = 0
    for i, line in enumerate(lines):
        if line.strip() == "---" and i > 3:
            start = i + 1
            break
    post_text = "\n".join(lines[start:]).strip()
    post_text = re.sub(r"\n---\n.*", "", post_text, flags=re.DOTALL).strip()

    return post_text, image_prompt


def parse_thread(filepath):
    """Parse a thread markdown file into individual tweets.

    Looks for ## Tweet N headers or similar patterns to split content.
    Returns list of tweet texts, or None if not a thread.
    """
    content = Path(filepath).read_text()

    # Check if this is a thread (has ## Tweet N pattern)
    tweet_pattern = re.compile(r"^##\s+Tweet\s+\d+", re.MULTILINE)
    if not tweet_pattern.search(content):
        return None

    # Split by tweet headers
    parts = re.split(r"(?=^##\s+Tweet\s+\d+)", content, flags=re.MULTILINE)

    tweets = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Skip if it's not a tweet section (e.g., Karen checklist, publication instructions)
        if not re.match(r"^##\s+Tweet\s+\d+", part):
            continue
        # Remove the header line
        lines = part.split("\n")
        tweet_lines = []
        started = False
        for line in lines:
            if re.match(r"^##\s+Tweet\s+\d+", line):
                started = True
                continue
            if started:
                # Stop at next section or checklist
                if line.startswith("## ") or line.startswith("---") or line.startswith("## Karen"):
                    break
                tweet_lines.append(line)

        tweet_text = "\n".join(tweet_lines).strip()
        if tweet_text:
            tweets.append(tweet_text)

    return tweets if tweets else None


def detect_platform_from_filename(filepath):
    name = Path(filepath).stem
    for suffix, (account_id, platform) in PLATFORMS.items():
        if name.endswith(f"-{suffix}"):
            return [suffix]
    return []


def resolve_platforms(flag_value, filename_hints, use_all):
    if use_all:
        return list(PLATFORMS.keys())
    if flag_value:
        parts = [p.strip().lower() for p in flag_value.split(",")]
        invalid = [p for p in parts if p not in PLATFORMS]
        if invalid:
            print(f"Unknown platforms: {', '.join(invalid)}")
            print(f"Available: {', '.join(PLATFORMS.keys())}")
            sys.exit(1)
        return parts
    if filename_hints:
        return filename_hints
    return []


def mcp_call(api_key, method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }
    resp = requests.post(
        MCP_ENDPOINT,
        json=payload,
        headers={
            "Accept": "application/json, text/event-stream",
            "blotato-api-key": api_key,
        },
        timeout=120,
    )
    if resp.status_code != 200:
        return {"error": {"message": f"HTTP {resp.status_code}: {resp.text[:200]}"}}
    try:
        return resp.json()
    except ValueError:
        return {"error": {"message": f"Invalid JSON response: {resp.text[:200]}"}}


def generate_visual(api_key, prompt, title="Road4AI Visual"):
    """Generate a visual via Blotato and return image URLs."""
    print(f"  Generating visual: {title}...", end=" ", flush=True)
    result = mcp_call(api_key, "tools/call", {
        "name": "blotato_create_visual",
        "arguments": {
            "templateId": "9f4e66cd-b784-4c02-b2ce-e6d0765fd4c0",
            "prompt": prompt,
            "title": title,
        },
    })
    if "error" in result:
        print(f"FAILED: {result['error']}")
        return []
    inner = result.get("result", result)
    content = inner.get("content", [])
    if not content:
        print("FAILED: no response")
        return []
    resp_data = json.loads(content[0].get("text", "{}"))
    visual_id = resp_data.get("item", {}).get("id")
    if not visual_id:
        print("FAILED: no visual ID")
        return []

    # Poll until done
    import time
    for attempt in range(30):
        time.sleep(5)
        status_result = mcp_call(api_key, "tools/call", {
            "name": "blotato_get_visual_status",
            "arguments": {"id": visual_id},
        })
        if "error" in status_result:
            continue
        status_inner = status_result.get("result", status_result)
        status_content = status_inner.get("content", [])
        if not status_content:
            continue
        status_data = json.loads(status_content[0].get("text", "{}"))
        status = status_data.get("item", {}).get("status", "")
        if status == "done":
            urls = status_data.get("item", {}).get("imageUrls", [])
            print(f"done ({len(urls)} image(s))")
            return urls
        elif status in ("failed", "error"):
            print(f"FAILED: {status}")
            return []
    print("TIMEOUT")
    return []


def schedule_post(api_key, account_id, platform, text, scheduled_time=None, next_slot=False, image_urls=None, additional_posts=None):
    arguments = {
        "accountId": account_id,
        "platform": platform,
        "text": text,
    }
    if scheduled_time:
        arguments["scheduledTime"] = scheduled_time
    elif next_slot:
        arguments["useNextFreeSlot"] = True
    if image_urls:
        arguments["mediaUrls"] = image_urls
    if additional_posts:
        arguments["additionalPosts"] = additional_posts

    params = {
        "name": "blotato_create_post",
        "arguments": arguments,
    }
    result = mcp_call(api_key, "tools/call", params)
    if "error" in result:
        return {"error": result["error"].get("message", str(result["error"]))}
    inner = result.get("result", result)
    return inner


def schedule_thread(api_key, account_id, tweets, scheduled_time=None, next_slot=False, image_urls=None):
    """Schedule a thread using Blotato's additionalPosts parameter.

    Args:
        api_key: Blotato API key
        account_id: X/Twitter account ID
        tweets: List of tweet texts
        scheduled_time: ISO 8601 time for the thread
        next_slot: Use next available slot
        image_urls: Optional image URLs for first tweet

    Returns:
        Result from blotato_create_post
    """
    print(f"Posting thread ({len(tweets)} tweets)...", end=" ", flush=True)

    # First tweet is the main text, rest go in additionalPosts
    first_tweet = tweets[0]
    additional_posts = [{"text": tweet} for tweet in tweets[1:]]

    result = schedule_post(
        api_key,
        account_id,
        "twitter",
        first_tweet,
        scheduled_time=scheduled_time,
        next_slot=next_slot,
        image_urls=image_urls,
        additional_posts=additional_posts,
    )

    info = extract_result(result)
    status = info.get("status", "unknown")
    url = info.get("url", "")
    print(f"{status}")
    if url:
        print(f"  URL: {url}")

    return info


def extract_result(result):
    if result.get("isError"):
        content = result.get("content", [])
        error_text = content[0].get("text", "Unknown error") if content else "Unknown error"
        return {"error": error_text}
    content = result.get("content", [])
    if content:
        inner = json.loads(content[0].get("text", "{}"))
        return {
            "submission_id": inner.get("postSubmissionId"),
            "status": inner.get("status"),
            "url": inner.get("publicUrl"),
        }
    return {}


def main():
    args = sys.argv[1:]
    auto_yes = "--yes" in args or "-y" in args
    show_list = "--list" in args
    use_all = "--all" in args
    next_slot = "--next-slot" in args
    check_only = "--check" in args
    force = "--force" in args
    platform_flag = None
    schedule_flag = None

    filtered = []
    i = 0
    while i < len(args):
        if args[i] in ("--yes", "-y", "--list", "--all", "--next-slot", "--check", "--force"):
            i += 1
        elif args[i] == "--platform" and i + 1 < len(args):
            platform_flag = args[i + 1]
            i += 2
        elif args[i] == "--schedule" and i + 1 < len(args):
            schedule_flag = args[i + 1]
            i += 2
        else:
            filtered.append(args[i])
            i += 1
    args = filtered

    if show_list:
        print("Available platforms:")
        for suffix, (account_id, platform) in PLATFORMS.items():
            print(f"  {suffix:8s} {platform:12s} (account {account_id})")
        sys.exit(0)

    if not args:
        print("Usage: python tools/schedule_post.py <draft-file> [options]")
        print("Options:")
        print("  --platform li,x,ig          Comma-separated platform suffixes")
        print("  --all                       Post to all platforms")
        print("  --schedule <time>           Schedule for specific time")
        print("  --next-slot                 Use Blotato's next available slot")
        print("  --check                     Check guardrails only (no scheduling)")
        print("  --force                     Skip guardrail checks")
        print("  --yes, -y                   Skip confirmation prompt")
        print("  --list                      Show available platforms")
        sys.exit(1)

    filepath = args[0]
    if not Path(filepath).exists():
        print(f"File not found: {filepath}")
        sys.exit(1)

    fm, issues = check_guardrails(filepath, force)

    if check_only:
        print(f"Guardrail check: {filepath}")
        if issues:
            print("BLOCKED:")
            for issue in issues:
                print(f"  - {issue}")
            sys.exit(1)
        else:
            print("PASSED: All guardrails OK")
            if fm:
                print(f"  Karen: {fm.get('karen_verdict', '(none)')}")
                print(f"  Status: {fm.get('status', '(none)')}")
            sys.exit(0)

    if issues:
        print("GUARDRAIL VIOLATIONS:")
        for issue in issues:
            print(f"  - {issue}")
        print("")
        print("Content must be in drafts/approved/ with karen_verdict: APPROVED")
        print("Use --force to bypass (not recommended)")
        sys.exit(1)

    api_key = load_api_key()
    if not api_key:
        print("ERROR: No BLOTATO_API_KEY found in .env or environment")
        sys.exit(1)

    filename_hints = detect_platform_from_filename(filepath)
    platforms = resolve_platforms(platform_flag, filename_hints, use_all)
    if not platforms:
        print(f"Cannot detect platform from filename: {filepath}")
        print("Use --platform li,x,ig or --all")
        print(f"Available: {', '.join(PLATFORMS.keys())}")
        sys.exit(1)

    scheduled_time = parse_schedule(schedule_flag) if schedule_flag else None

    text, image_prompt = parse_draft(filepath)

    # Check if this is a thread (X platform with ## Tweet N headers)
    is_thread = "x" in platforms and parse_thread(filepath) is not None
    tweets = parse_thread(filepath) if is_thread else None

    if is_thread:
        print(f"Thread detected: {len(tweets)} tweets")
        print(f"Platform: x (twitter)")
        print(f"Karen: {fm.get('karen_verdict', '(none)')}")
        if scheduled_time:
            print(f"Scheduled: {scheduled_time}")
        elif next_slot:
            print("Scheduled: next available slot")
        else:
            print("Scheduled: now")
        print("---")
        for i, tweet in enumerate(tweets):
            print(f"Tweet {i+1}: {tweet[:80]}...")
        print("---")
    else:
        print(f"Platforms: {', '.join(platforms)}")
        print(f"Text length: {len(text)} chars")
        print(f"Image prompt: {'yes' if image_prompt else 'no'}")
        print(f"Karen: {fm.get('karen_verdict', '(none)')}")
        if scheduled_time:
            print(f"Scheduled: {scheduled_time}")
        elif next_slot:
            print("Scheduled: next available slot")
        else:
            print("Scheduled: now")
        print("---")
        print(text[:300] + "..." if len(text) > 300 else text)
        print("---")

    if not auto_yes:
        try:
            count = len(tweets) if is_thread else len(platforms)
            label = "tweets in thread" if is_thread else f"platform(s)"
            confirm = input(f"Post to {count} {label}? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            sys.exit(0)
        if confirm != "y":
            print("Cancelled.")
            sys.exit(0)

    image_urls = []
    if image_prompt:
        print("\n[Image Generation]")
        image_urls = generate_visual(api_key, image_prompt, title="Road4AI Post Image")

    results = []
    for suffix in platforms:
        account_id, platform = PLATFORMS[suffix]
        if is_thread and platform == "twitter":
            print(f"\nPosting thread to {platform}...")
            try:
                thread_result = schedule_thread(
                    api_key,
                    account_id,
                    tweets,
                    scheduled_time=scheduled_time,
                    next_slot=next_slot,
                    image_urls=image_urls,
                )
                results.append({"platform": platform, "thread": True, "tweets": len(tweets), **thread_result})
            except Exception as e:
                results.append({"platform": platform, "error": str(e)})
                print(f"FAILED: {e}")
        else:
            print(f"\nPosting to {platform}...", end=" ", flush=True)
            try:
                result = schedule_post(api_key, account_id, platform, text, scheduled_time, next_slot, image_urls=image_urls)
                info = extract_result(result)
                results.append({"platform": platform, **info})
                status = info.get("status", "unknown")
                url = info.get("url", "")
                print(f"{status}")
                if url:
                    print(f"  URL: {url}")
            except Exception as e:
                results.append({"platform": platform, "error": str(e)})
                print(f"FAILED: {e}")

    print(f"\n{'='*50}")
    print("Results:")
    for r in results:
        platform = r["platform"]
        if "error" in r:
            print(f"  {platform:12s} FAILED  {r['error']}")
        elif r.get("thread"):
            sid = r.get("submission_id") or "?"
            status = r.get("status") or "scheduled"
            tweet_count = r.get("tweets", "?")
            url = r.get("url") or ""
            print(f"  {platform:12s} THREAD ({tweet_count} tweets) {status:12s} {sid}")
            if url:
                print(f"  {'':12s} {url}")
        else:
            sid = r.get("submission_id") or "?"
            status = r.get("status") or "scheduled"
            url = r.get("url") or ""
            print(f"  {platform:12s} {status:12s} {sid}")
            if url:
                print(f"  {'':12s} {url}")


if __name__ == "__main__":
    main()
