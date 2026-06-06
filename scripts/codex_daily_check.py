#!/usr/bin/env python3
"""Print the Road4AI daily startup audit for Codex sessions."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
QUEUE_PATH = REPO / "state" / "current-queue.json"
TASKS_DIR = REPO / "plan" / "tasks"
REQUIRED_FILES = [
    "AGENTS.md",
    "state/current-queue.json",
    "docs/brand-voice.md",
    "docs/content-strategy.md",
    "WORKING-CONTEXT.md",
]


def load_queue() -> list[dict]:
    data = json.loads(QUEUE_PATH.read_text())
    if isinstance(data, dict) and isinstance(data.get("queue"), list):
        return data["queue"]
    if isinstance(data, list):
        return data
    raise ValueError("state/current-queue.json must contain a queue array")


def read_task(path: Path) -> dict[str, str]:
    text = path.read_text()
    fields = {}
    for key in ("id", "title", "status", "phase", "wave", "assigned_to"):
        match = re.search(rf"^{key}:\s*(.+)$", text, flags=re.MULTILINE)
        if match:
            fields[key] = match.group(1).strip().strip('"')
    depends = re.search(r"^depends_on:\s*\[(.*?)\]$", text, flags=re.MULTILINE)
    if depends:
        fields["depends_on"] = depends.group(1).strip()
    return fields


def main() -> int:
    print("ROAD4AI DAILY STARTUP")
    print("Repo          : /Users/shagwu/Downloads/Road4AI-main")
    print(f"Checked at    : {datetime.now(timezone.utc).isoformat(timespec='seconds')}")

    missing = [name for name in REQUIRED_FILES if not (REPO / name).exists()]
    print(f"Core files    : {'OK' if not missing else 'MISSING ' + ', '.join(missing)}")

    queue = load_queue()
    statuses = Counter(item.get("status", "unknown") for item in queue)
    ids = [item.get("id") for item in queue if item.get("id")]
    duplicate_ids = sorted(item_id for item_id, count in Counter(ids).items() if count > 1)

    print()
    print("QUEUE AUDIT")
    print("───────────────────────────────")
    print(f"Total entries : {len(queue)}")
    print(f"Published     : {statuses.get('published', 0)}")
    print(f"Scheduled     : {statuses.get('scheduled', 0)}")
    print(f"Ready         : {statuses.get('ready', 0) + statuses.get('ready_for_publishing', 0)}")
    print(f"Drafting      : {statuses.get('draft_in_progress', 0)}")
    print(f"Duplicate IDs : {'none' if not duplicate_ids else ', '.join(duplicate_ids)}")
    print("───────────────────────────────")

    upcoming = sorted(
        (
            item
            for item in queue
            if item.get("status") in {"scheduled", "ready", "ready_for_publishing", "ready_for_drafting"}
        ),
        key=lambda item: item.get("scheduled_time") or item.get("created_at") or "",
    )

    print()
    print("NEXT CONTENT ITEMS")
    for item in upcoming[:5]:
        when = item.get("scheduled_time") or item.get("created_at") or "unscheduled"
        print(f"- {when} | {item.get('status', 'unknown')} | {item.get('title', item.get('id', 'untitled'))}")

    tasks = [read_task(path) for path in sorted(TASKS_DIR.glob("T-*.yaml"))]
    ready_tasks = [task for task in tasks if task.get("status") == "ready"]
    blocked_tasks = [task for task in tasks if task.get("status") == "blocked"]

    print()
    print("PLAN TASKS")
    print(f"Ready         : {len(ready_tasks)}")
    for task in ready_tasks:
        print(f"- {task.get('id', '?')} | {task.get('title', 'untitled')} | assigned: {task.get('assigned_to', 'unknown')}")
    print(f"Blocked       : {len(blocked_tasks)}")

    return 1 if missing or duplicate_ids else 0


if __name__ == "__main__":
    raise SystemExit(main())
