#!/usr/bin/env python3
"""Generate daily-plan.md from repo state — runs Mon-Fri at 6am via launchd."""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

CRON_LOG_PATH = ROOT / "state" / "daily-brief.log"


def _cron_log(msg: str):
    """Append a plain-text message to the cron log file."""
    try:
        CRON_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CRON_LOG_PATH, "a") as f:
            f.write(msg + "\n")
    except Exception as e:
        print(f"[daily-brief] Failed to write cron log: {e}", file=sys.stderr)


def _read_file(path: Path) -> str:
    """Read a file, return empty string if missing."""
    try:
        return path.read_text()
    except FileNotFoundError:
        return ""


def _git_log() -> str:
    """Get last 3 Hermes checkpoints."""
    try:
        result = subprocess.run(
            ["git", "log", "--grep=CHECKPOINT:", "--format=%B", "-3"],
            capture_output=True, text=True, cwd=str(ROOT), timeout=10,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def _queue_stats() -> dict:
    """Parse queue and return status counts + struggle ratio."""
    queue_path = ROOT / "state" / "current-queue.json"
    raw = _read_file(queue_path)
    if not raw:
        return {"total": 0, "statuses": {}, "struggle_count": 0, "top_10_total": 0}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"total": 0, "statuses": {}, "struggle_count": 0, "top_10_total": 0}

    entries = data.get("queue", data) if isinstance(data, dict) else data
    if not isinstance(entries, list):
        return {"total": 0, "statuses": {}, "struggle_count": 0, "top_10_total": 0}

    statuses = {}
    for e in entries:
        s = e.get("status", "unknown")
        statuses[s] = statuses.get(s, 0) + 1

    top_10 = entries[:10]
    struggle_count = sum(1 for e in top_10 if e.get("type") == "Struggle")

    return {
        "total": len(entries),
        "statuses": statuses,
        "struggle_count": struggle_count,
        "top_10_total": len(top_10),
    }


def _drafts_check() -> dict:
    """Check drafts/ lifecycle folders."""
    result = {}
    for folder in ["approved", "ready", "ideas", "archived"]:
        d = ROOT / "drafts" / folder
        if d.exists():
            files = [f.name for f in d.iterdir() if f.is_file()]
            result[folder] = files
        else:
            result[folder] = []
    return result


def _task_status() -> list:
    """Parse state.yaml for task statuses."""
    state_path = ROOT / "state.yaml"
    raw = _read_file(state_path)
    if not raw:
        return []

    tasks = []
    current_id = None
    for line in raw.splitlines():
        stripped = line.strip()
        # Match task ID lines like "T-001:"
        if stripped.startswith("T-") and stripped.endswith(":") and len(stripped) <= 8:
            current_id = stripped.rstrip(":")
        # Match status lines indented under a task
        elif current_id and stripped.startswith("status:"):
            status = stripped.split(":", 1)[1].strip()
            tasks.append({"id": current_id, "status": status})
            current_id = None
    return tasks


def _upcoming_milestones() -> list:
    """Extract date-based milestones from WORKING-CONTEXT.md."""
    wc = _read_file(ROOT / "WORKING-CONTEXT.md")
    if not wc:
        return []

    milestones = []
    today = datetime.now().date()
    for line in wc.splitlines():
        line = line.strip()
        # Look for date patterns like "July 15" or "2026-07-15"
        for fmt in ["%B %d", "%Y-%m-%d"]:
            try:
                # Try parsing with current year
                dt = datetime.strptime(line.split("|")[0].strip().split("-")[-1].strip(), fmt)
                if fmt == "%B %d":
                    dt = dt.replace(year=today.year)
                delta = (dt.date() - today).days
                if -3 <= delta <= 30:
                    desc = line.split("|")[-1].strip() if "|" in line else line
                    milestones.append({
                        "date": dt.strftime("%Y-%m-%d"),
                        "days_away": delta,
                        "description": desc[:80],
                    })
                break
            except (ValueError, IndexError):
                continue
    return sorted(milestones, key=lambda m: m["days_away"])


def _git_diff_summary() -> str:
    """Check for uncommitted changes."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=str(ROOT), timeout=10,
        )
        lines = [l for l in result.stdout.strip().splitlines() if l]
        if not lines:
            return "Clean working tree."
        return f"{len(lines)} uncommitted file(s): {', '.join(l.split()[-1] for l in lines[:5])}"
    except Exception:
        return "Could not check git status."


def generate_daily_plan() -> str:
    """Build the daily-plan.md content from repo state."""
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Gather data
    checkpoints = _git_log()
    qstats = _queue_stats()
    drafts = _drafts_check()
    tasks = _task_status()
    milestones = _upcoming_milestones()
    git_status = _git_diff_summary()

    # Parse checkpoints for decisions and remaining
    decisions = []
    remaining = []
    confidence = "unknown"
    for line in checkpoints.splitlines():
        line = line.strip()
        if line.startswith("Decisions:"):
            decisions.append(line.split(":", 1)[1].strip())
        elif line.startswith("Remaining:"):
            remaining.append(line.split(":", 1)[1].strip())
        elif line.startswith("Confidence:"):
            confidence = line.split(":", 1)[1].strip()

    # Build output
    lines = []
    lines.append(f"# Daily Plan - {today}")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append("")

    # Executive summary
    lines.append("## Executive summary")
    lines.append("")
    active_tasks = [t for t in tasks if t["status"] in ("in_progress", "verify", "ready")]
    blocked_tasks = [t for t in tasks if t["status"] == "blocked"]
    scheduled_count = qstats["statuses"].get("scheduled", 0)
    published_count = qstats["statuses"].get("published", 0)
    approved_count = len(drafts.get("approved", []))

    summary_parts = []
    if milestones:
        nearest = milestones[0]
        summary_parts.append(f"Nearest milestone: {nearest['description']} ({nearest['date']}, {nearest['days_away']}d)")
    if active_tasks:
        summary_parts.append(f"{len(active_tasks)} task(s) in progress")
    if blocked_tasks:
        summary_parts.append(f"{len(blocked_tasks)} task(s) blocked")
    if scheduled_count:
        summary_parts.append(f"{scheduled_count} content item(s) scheduled")
    if approved_count:
        summary_parts.append(f"{approved_count} draft(s) awaiting manual scheduling")
    if not summary_parts:
        summary_parts.append("No active milestones or tasks detected")
    lines.append("; ".join(summary_parts) + ".")
    lines.append("")

    # P1 - Highest priority
    lines.append("## P1 - Highest priority")
    lines.append("")
    p1_items = []
    for t in active_tasks:
        if t["status"] in ("in_progress", "verify"):
            p1_items.append(f"- **{t['id']}** — status: `{t['status']}`")
    if approved_count:
        p1_items.append(f"- {approved_count} draft(s) in `drafts/approved/` — manual scheduling only, do not auto-schedule")
    if not p1_items:
        p1_items.append("- No P1 items detected. Check queue for new ideas.")
    lines.extend(p1_items)
    lines.append("")

    # P2 - Important next work
    lines.append("## P2 - Important next work")
    lines.append("")
    p2_items = []
    for t in blocked_tasks:
        p2_items.append(f"- **{t['id']}** — blocked (waiting on upstream)")
    ready_count = qstats["statuses"].get("ready_for_drafting", 0)
    if ready_count:
        p2_items.append(f"- **{ready_count} queue item(s) ready for drafting**")
    if remaining:
        for r in remaining[:3]:
            p2_items.append(f"- {r}")
    if not p2_items:
        p2_items.append("- No P2 items detected.")
    lines.extend(p2_items)
    lines.append("")

    # P3 - Lower priority / support
    lines.append("## P3 - Lower priority / support work")
    lines.append("")
    p3_items = []
    if qstats["statuses"].get("idea", 0):
        p3_items.append(f"- **{qstats['statuses']['idea']} idea(s)** in queue need promotion to drafting")
    if decisions:
        for d in decisions[:2]:
            p3_items.append(f"- {d}")
    p3_items.append("- Drift monitoring check (automated)")
    if not p3_items:
        p3_items.append("- No P3 items detected.")
    lines.extend(p3_items)
    lines.append("")

    # Risks / blockers
    lines.append("## Risks / blockers")
    lines.append("")
    risk_items = []
    if blocked_tasks:
        risk_items.append(f"- {len(blocked_tasks)} task(s) blocked: {', '.join(t['id'] for t in blocked_tasks)}")
    if confidence in ("low", "unknown"):
        risk_items.append(f"- Last checkpoint confidence: {confidence}")
    if milestones:
        overdue = [m for m in milestones if m["days_away"] < 0]
        if overdue:
            risk_items.append(f"- OVERDUE: {', '.join(m['description'] for m in overdue)}")
    if not risk_items:
        risk_items.append("- No blockers detected.")
    lines.extend(risk_items)
    lines.append("")

    # Queue audit
    lines.append("## Queue audit")
    lines.append("")
    lines.append("```")
    lines.append(f"Total entries : {qstats['total']}")
    for status, count in sorted(qstats["statuses"].items()):
        label = status.replace("_", " ").title()
        lines.append(f"{label:14}: {count}")
    struggle_pct = (qstats["struggle_count"] / qstats["top_10_total"] * 100) if qstats["top_10_total"] else 0
    lines.append(f"Struggle (T10): {qstats['struggle_count']}/{qstats['top_10_total']} ({struggle_pct:.0f}%)")
    lines.append(f"Git status    : {git_status}")
    lines.append("```")
    lines.append("")

    # Upcoming milestones
    if milestones:
        lines.append("## Upcoming milestones")
        lines.append("")
        for m in milestones[:5]:
            sign = "+" if m["days_away"] >= 0 else ""
            lines.append(f"- {m['date']} ({sign}{m['days_away']}d): {m['description']}")
        lines.append("")

    # Drafts status
    any_drafts = any(drafts.get(k) for k in ["approved", "ready", "ideas"])
    if any_drafts:
        lines.append("## Drafts")
        lines.append("")
        for folder in ["approved", "ready", "ideas"]:
            files = drafts.get(folder, [])
            if files:
                lines.append(f"- `{folder}/`: {', '.join(files[:5])}")
        lines.append("")

    # Last checkpoint
    if checkpoints:
        lines.append("## Last Hermes checkpoint")
        lines.append("")
        lines.append("```")
        lines.append(checkpoints[:500])
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    msg = f"[daily-brief] Starting daily brief generation at {timestamp}"
    print(msg)
    _cron_log(msg)

    try:
        content = generate_daily_plan()
        output_path = ROOT / "daily-plan.md"
        output_path.write_text(content)
        done_msg = f"[daily-brief] daily-plan.md written ({len(content)} bytes)"
        print(done_msg)
        _cron_log(done_msg)
    except Exception as e:
        err_msg = f"[daily-brief] Error: {e}"
        print(err_msg, file=sys.stderr)
        _cron_log(err_msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
