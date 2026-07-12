#!/usr/bin/env python3
"""Schedule a Road4AI post via Blotato MCP.

Usage:
  python tools/schedule_post.py drafts/approved/post-li.md
  python tools/schedule_post.py drafts/approved/post.md --platform li,x,ig
  python tools/schedule_post.py drafts/approved/post.md --all --yes
  python tools/schedule_post.py drafts/approved/post.md --schedule "2026-06-28T09:00:00Z"
  python tools/schedule_post.py drafts/approved/post.md --schedule "+2h"
  python tools/schedule_post.py drafts/approved/post.md --next-slot
  python tools/schedule_post.py drafts/approved/post.md --clone-media <submission_id> --platform ig
  python tools/schedule_post.py --check drafts/ready/post.md
  python tools/schedule_post.py --list

Guardrails:
  - Draft must be in drafts/approved/ (use --force to override)
  - Karen verdict must be APPROVED in frontmatter (use --force to override)
  - Draft must not already be scheduled (check published-log + queue blotato_id)
  - Draft must not have scheduled: true in frontmatter

Clone media:
  --clone-media <submission_id> pulls media URLs from an existing Blotato
  post and attaches them to the new post. Useful for cloning a LinkedIn post
  to Instagram when the original had auto-generated visuals.
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

VISUAL_TEMPLATES = {
    "carousel": "53cfec04-2500-41cf-8cc1-ba670d2c341a",  # Instagram Carousel Slideshow (short ID)
    "quote_card": "/base/v2/quote-card/f941e306-76f7-45da-b3d9-7463af630e91/v1",
    "image": "/base/v2/images-with-text/0ddb8655-c3da-43da-9f7d-be1915ca7818/v1",
    "tutorial": "/base/v2/tutorial-carousel/e095104b-e6c5-4a81-a89d-b0df3d7c5baf/v1",
    "video": "/base/v2/ai-story-video/5903fe43-514d-40ee-a060-0d6628c5f8fd/v1",
}


ROOT = Path(__file__).resolve().parent.parent

VISUAL_VARIETY_CYCLE = ["carousel", "quote_card", "image", "tutorial", "video"]
VISUAL_STATE_FILE = ROOT / "state" / "visual_variety.json"
MEDIA_CACHE_FILE = ROOT / "state" / "media_cache.json"
BRAND_STYLE_PREFIX = (
    "Black and emerald terminal aesthetic. Dark background, emerald green accents, "
    "bold white sans-serif text, no corporate stock photos, no emojis. "
)


def check_duplication(filepath, fm):
    """Check if this draft has already been scheduled. Returns list of issues."""
    issues = []
    filename = Path(filepath).stem

    # 1. Check if draft has scheduled: true in frontmatter
    if fm.get("scheduled", "").lower() == "true":
        issues.append(f"Draft already marked as scheduled (frontmatter: scheduled: true)")

    # 2. Check published-log.json
    pub_log = ROOT / "state" / "published-log.json"
    if pub_log.exists():
        try:
            pub_data = json.loads(pub_log.read_text())
            pub_entries = pub_data if isinstance(pub_data, list) else pub_data.get("entries", [])
            for entry in pub_entries:
                entry_title = entry.get("title", "")
                entry_id = entry.get("id", "")
                # Match by title similarity or filename substring
                if (filename in entry_id or filename in entry_title.replace(" ", "-").lower()
                        or entry_title.replace(" ", "-").lower() in filename):
                    issues.append(
                        f"Already in published-log: '{entry_title}' "
                        f"(published {entry.get('published_at', 'unknown')})"
                    )
                    break
        except (json.JSONDecodeError, KeyError):
            pass

    # 3. Check queue for existing blotato_id
    queue_path = ROOT / "state" / "current-queue.json"
    if queue_path.exists():
        try:
            qdata = json.loads(queue_path.read_text())
            queue = qdata.get("queue", qdata) if isinstance(qdata, dict) else qdata
            for entry in queue:
                entry_id = entry.get("id", "")
                if filename in entry_id or entry_id in filename:
                    if entry.get("blotato_id"):
                        issues.append(
                            f"Queue entry '{entry_id}' already has blotato_id: "
                            f"{entry['blotato_id']}"
                        )
                    if entry.get("status") == "published":
                        issues.append(
                            f"Queue entry '{entry_id}' is already status: published"
                        )
                    break
        except (json.JSONDecodeError, KeyError):
            pass

    return issues


def load_api_key():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("BLOTATO_API_KEY="):
                val = line.split("=", 1)[1].strip()
                if val and not val.startswith("#"):
                    return val
    return os.environ.get("BLOTATO_API_KEY", "")


def get_next_visual_type():
    """Read visual_variety.json and return the next visual type in the cycle."""
    last_type = "video"  # default: start with carousel (first in cycle)
    if VISUAL_STATE_FILE.exists():
        try:
            state = json.loads(VISUAL_STATE_FILE.read_text())
            last_type = state.get("last_type", "video")
        except (json.JSONDecodeError, KeyError):
            pass
    try:
        idx = VISUAL_VARIETY_CYCLE.index(last_type)
    except ValueError:
        idx = len(VISUAL_VARIETY_CYCLE) - 1
    next_idx = (idx + 1) % len(VISUAL_VARIETY_CYCLE)
    return VISUAL_VARIETY_CYCLE[next_idx]


def save_visual_type(visual_type):
    """Record the visual type just used for variety tracking."""
    VISUAL_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    VISUAL_STATE_FILE.write_text(json.dumps({"last_type": visual_type}, indent=2))


def save_media_cache(submission_id, media_urls):
    """Store media URLs keyed by Blotato submission ID for later cloning."""
    MEDIA_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    cache = {}
    if MEDIA_CACHE_FILE.exists():
        try:
            cache = json.loads(MEDIA_CACHE_FILE.read_text())
        except (json.JSONDecodeError, KeyError):
            pass
    cache[submission_id] = {
        "media_urls": media_urls,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    MEDIA_CACHE_FILE.write_text(json.dumps(cache, indent=2))


def load_media_cache(submission_id):
    """Load media URLs from cache by submission ID."""
    if not MEDIA_CACHE_FILE.exists():
        return []
    try:
        cache = json.loads(MEDIA_CACHE_FILE.read_text())
        entry = cache.get(submission_id, {})
        return entry.get("media_urls", [])
    except (json.JSONDecodeError, KeyError):
        return []


def auto_visual_prompt(post_text):
    """Generate a Blotato visual prompt from post content.

    Extracts the hook (first sentence or first line) and wraps it in
    brand style for the visual template.
    """
    # Take the first non-empty line as the hook
    lines = [l.strip() for l in post_text.split("\n") if l.strip()]
    hook = lines[0] if lines else post_text[:100]
    # Truncate to ~80 chars for visual readability
    if len(hook) > 80:
        hook = hook[:77] + "..."
    return (
        f"{BRAND_STYLE_PREFIX}"
        f"Bold white text: \"{hook}\". "
        f"Emerald accent bar at bottom. Clean, minimal, text-forward."
    )


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

    # Extract ALL Blotato image prompt blocks (for carousels with multiple slides)
    all_image_prompts = re.findall(
        r"\*\*Blotato image prompt:\*\*\s*\n(.+?)(?=\n\*\*Blotato|\n---|\n#|\Z)",
        content,
        re.DOTALL,
    )
    all_image_prompts = [p.strip() for p in all_image_prompts if p.strip()]

    # Single prompt (backward compatible)
    image_prompt = all_image_prompts[0] if all_image_prompts else ""

    # Match heading format: ## Image Prompt ...
    if not image_prompt:
        heading_match = re.search(
            r"^##\s+Image Prompt.*\n(.+?)(?=\n---|\n\n##|\n\n#|\Z)",
            content,
            re.MULTILINE | re.DOTALL,
        )
        if heading_match:
            image_prompt = heading_match.group(1).strip()
            all_image_prompts = [image_prompt]

    lines = content.split("\n")
    start = 0
    # Skip frontmatter: if line 0 is ---, find the closing ---
    if lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    else:
        for i, line in enumerate(lines):
            if line.strip() == "---" and i > 3:
                start = i + 1
                break
    after_frontmatter = "\n".join(lines[start:]).strip()

    # Split by --- separator (between image prompts and post text)
    sections = re.split(r"\n---\n", after_frontmatter)
    # Take the FIRST section that doesn't contain Blotato image prompts
    # (the post body is always the first section; later sections are
    # Links, Publication Instructions, etc. — those must not be posted)
    post_text = ""
    for section in sections:
        if "**Blotato image prompt:**" not in section:
            post_text = section.strip()
            break
    # Fallback: if all sections have prompts, strip prompts from full text
    if not post_text:
        post_text = re.sub(r"\*\*Blotato image prompt:\*\*\s*\n(.+?)(?=\n\*\*Blotato|\Z)", "", after_frontmatter, flags=re.DOTALL).strip()

    # Strip leading markdown title (# Title) — Blotato doesn't need it
    post_text = re.sub(r"^#\s+.+\n\n?", "", post_text).strip()

    return post_text, image_prompt, all_image_prompts


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


def fetch_post_media(api_key, submission_id):
    """Fetch media URLs for a Blotato submission.

    Strategy:
    1. Check local media cache (stored at generation time)
    2. Fall back to blotato_list_posts and match by recent LinkedIn posts

    Returns list of media URL strings, or empty list on failure.
    """
    print(f"  Fetching media for submission {submission_id}...", end=" ", flush=True)

    # 1. Check local cache first
    cached = load_media_cache(submission_id)
    if cached:
        print(f"found {len(cached)} URL(s) (cached)")
        return cached

    # 2. Fall back to list_posts — match by finding the LinkedIn post
    #    scheduled closest to now with the same submission time window
    try:
        result = mcp_call(api_key, "tools/call", {
            "name": "blotato_list_posts",
            "arguments": {"limit": 20},
        })
        if "error" in result:
            print("FAILED: list_posts error")
            return []
        inner = result.get("result", result)
        content = inner.get("content", [])
        if not content:
            print("FAILED: no response")
            return []
        data = json.loads(content[0].get("text", "{}"))
        posts = data.get("items", [])

        # Find LinkedIn posts with media — the most recent one is likely ours
        for post in posts:
            if post.get("platform") == "linkedin" and post.get("mediaUrls"):
                print(f"found {len(post['mediaUrls'])} URL(s) (from list_posts)")
                return post["mediaUrls"]

        print("no media found")
        return []
    except Exception as e:
        print(f"FAILED: {e}")
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


def generate_visual(api_key, prompt, title="Road4AI Visual", visual_type="image"):
    """Generate a visual via Blotato and return image URLs or video URL."""
    template_id = VISUAL_TEMPLATES.get(visual_type, VISUAL_TEMPLATES["image"])
    print(f"  Generating {visual_type}: {title}...", end=" ", flush=True)
    result = mcp_call(api_key, "tools/call", {
        "name": "blotato_create_visual",
        "arguments": {
            "templateId": template_id,
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

    # Poll until done (300s timeout for videos)
    import time
    max_attempts = 60 if visual_type == "video" else 30
    poll_interval = 5
    for attempt in range(max_attempts):
        time.sleep(poll_interval)
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
        item = status_data.get("item", {})
        status = item.get("status", "")
        if status == "done":
            # Videos return mediaUrl, images/carousels return imageUrls
            media_url = item.get("mediaUrl")
            image_urls = item.get("imageUrls", [])
            if media_url and visual_type == "video":
                print(f"done (video)")
                return [media_url]
            elif image_urls:
                print(f"done ({len(image_urls)} image(s))")
                return image_urls
            else:
                print("FAILED: no media in response")
                return []
        elif status in ("failed", "error"):
            print(f"FAILED: {status}")
            return []
    print("TIMEOUT")
    return []


def schedule_post(api_key, account_id, platform, text, scheduled_time=None, next_slot=False, image_urls=None, additional_posts=None, media_type=None):
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
    # Instagram/Facebook need mediaType for video posts
    if media_type:
        arguments["mediaType"] = media_type

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


def mark_as_scheduled(filepath):
    """Add scheduled: true to frontmatter after successful Blotato submission."""
    path = Path(filepath)
    content = path.read_text()
    fm_match = re.match(r"^(---\s*\n)(.*?\n)(---\s*\n)", content, re.DOTALL)
    if not fm_match:
        return
    fm_block = fm_match.group(2)
    if "scheduled:" in fm_block.lower():
        return  # already marked
    # Add scheduled: true at end of frontmatter
    new_fm = fm_block.rstrip() + "\nscheduled: true\n"
    new_content = fm_match.group(1) + new_fm + fm_match.group(3) + content[fm_match.end():]
    path.write_text(new_content)


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
    clone_media_id = None

    filtered = []
    i = 0
    while i < len(args):
        if args[i] in ("--yes", "-y", "--list", "--all", "--next-slot", "--check", "--force"):
            i += 1
        elif args[i] == "--clone-media" and i + 1 < len(args):
            clone_media_id = args[i + 1]
            i += 2
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
        print("  --clone-media <sub_id>      Pull media from existing Blotato submission")
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

    # Duplication check (unless --force)
    if not force:
        dup_issues = check_duplication(filepath, fm)
        if dup_issues:
            print("DUPLICATION BLOCKED:")
            for issue in dup_issues:
                print(f"  - {issue}")
            print("")
            print("This content appears to already be scheduled or published.")
            print("Use --force to bypass (not recommended)")
            sys.exit(1)

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

    text, image_prompt, all_image_prompts = parse_draft(filepath)
    visual_type = fm.get("visual_type", "image")

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

    # --clone-media: pull media from an existing Blotato submission
    if clone_media_id:
        image_urls = fetch_post_media(api_key, clone_media_id)
        if not image_urls:
            print("\nWARNING: Could not fetch media from submission", clone_media_id)
            print("Post will go out without media attached.")
            if not auto_yes:
                try:
                    confirm = input("Continue anyway? [y/N] ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    confirm = "n"
                if confirm != "y":
                    print("Cancelled.")
                    sys.exit(0)
    else:
        # Auto-generate visual for LinkedIn posts that lack one
        if "li" in platforms and not image_prompt and not all_image_prompts:
            visual_type = get_next_visual_type()
            image_prompt = auto_visual_prompt(text)
            print(f"\n[Auto-visual: {visual_type}]")
            print(f"  Prompt: {image_prompt[:100]}...")
        if image_prompt or all_image_prompts:
            print(f"\n[Visual Generation: {visual_type}]")
            if visual_type == "carousel" and len(all_image_prompts) > 1:
                combined = "Create a carousel with these slides:\n"
                for i, p in enumerate(all_image_prompts, 1):
                    combined += f"\nSlide {i}/{len(all_image_prompts)}: {p}\n"
                image_urls = generate_visual(api_key, combined, title="Road4AI Carousel", visual_type=visual_type)
            else:
                image_urls = generate_visual(api_key, image_prompt, title="Road4AI Post Image", visual_type=visual_type)
            if image_urls:
                save_visual_type(visual_type)

    # Warn if image generation failed and posts include Instagram
    ig_needs_media = "ig" in platforms and not clone_media_id
    if not image_urls and ig_needs_media:
        print("\n" + "=" * 50)
        print("WARNING: No media URLs generated. Instagram posts require")
        print("media (image or video) to display correctly.")
        print("Posts will go out as text-only.")
        print("=" * 50)
        if not auto_yes:
            try:
                confirm = input("Continue without media? [y/N] ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                confirm = "n"
            if confirm != "y":
                print("Cancelled.")
                sys.exit(0)

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
                # Detect video URLs for Instagram/Facebook mediaType
                media_type = None
                if platform in ("instagram", "facebook") and image_urls:
                    has_video = any(url.endswith((".mp4", ".mov", ".webm")) for url in image_urls)
                    if has_video:
                        media_type = "reel"
                result = schedule_post(api_key, account_id, platform, text, scheduled_time, next_slot, image_urls=image_urls, media_type=media_type)
                info = extract_result(result)
                results.append({"platform": platform, **info})
                status = info.get("status", "unknown")
                url = info.get("url", "")
                sid = info.get("submission_id")
                # Cache media URLs for later cloning
                if sid and image_urls:
                    save_media_cache(sid, image_urls)
                print(f"{status}")
                if url:
                    print(f"  URL: {url}")
            except Exception as e:
                results.append({"platform": platform, "error": str(e)})
                print(f"FAILED: {e}")

    print(f"\n{'='*50}")
    print("Results:")
    any_success = False
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
            any_success = True
        else:
            sid = r.get("submission_id") or "?"
            status = r.get("status") or "scheduled"
            url = r.get("url") or ""
            print(f"  {platform:12s} {status:12s} {sid}")
            if url:
                print(f"  {'':12s} {url}")
            any_success = True

    # Mark draft as scheduled to prevent duplicates
    if any_success:
        try:
            mark_as_scheduled(filepath)
            print(f"\n  Draft marked as scheduled: {filepath}")
        except Exception as e:
            print(f"\n  WARNING: Could not mark draft as scheduled: {e}")
            print(f"  Manual action required: add 'scheduled: true' to frontmatter")


if __name__ == "__main__":
    main()
