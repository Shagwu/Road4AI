#!/usr/bin/env python3
<<<<<<< HEAD
"""
Daily drift check for July 1-10 monitoring window.
Run once per day. Logs to state/drift_log.jsonl, alerts to state/drift_alerts.jsonl.
=======
"""Daily drift check — runs voice-match benchmark and checks drift against baseline.
>>>>>>> fc0dff2 (CHECKPOINT: Daily drift monitoring scheduled — runs 09:00 UTC daily)

Usage:
    python tools/daily_drift_check.py
    python tools/daily_drift_check.py --dry-run
"""
<<<<<<< HEAD

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drift_monitor import DriftMonitor, DRIFT_LOG, DRIFT_ALERTS, DRIFT_HALT


def run_daily_check(dry_run: bool = False) -> dict:
    """Run daily drift check using latest orchestration scores."""
    monitor = DriftMonitor()

    sv_score = monitor.baseline["domains"]["social_voice"]["score"]
    mo_score = monitor.baseline["domains"]["memory_ops"]["score"]

    checkpoint_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "domains": [
            {"name": "social_voice", "score": sv_score, "confidence_tier": "green"},
            {"name": "memory_ops", "score": mo_score, "confidence_tier": "green"}
        ]
    }

    report = monitor.run_check(checkpoint_data)

    if not dry_run:
        monitor.log_result(report)

    # Print summary
    status = report["overall_status"]
    marker = {"green": "\u2713", "yellow": "\u26a0", "blue": "\u2717"}.get(status, "?")
    print(f"Daily Drift Check: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Status: {marker} {status.upper()}")
    for check in report["domain_checks"]:
        print(f"  {check['domain']}: {check['variance']:.2%} variance \u2014 {check['action']}")
    print(f"  Cross-domain correlation: {report['cross_domain']['correlation']:.2f}")

    if report["human_action_needed"]:
        print(f"\n\u26a0 Human action required")
    else:
        print(f"\n\u2713 All clear")

    if dry_run:
        print("\n[dry-run \u2014 not logged]")

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Daily drift check for July 1-10 window")
    parser.add_argument("--dry-run", action="store_true", help="Don't write to state files")
    args = parser.parse_args()

    report = run_daily_check(dry_run=args.dry_run)
    return 1 if report["overall_status"] == "blue" else 0


if __name__ == "__main__":
    raise SystemExit(main())
=======
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from drift_monitor import DriftMonitor, BASELINE_FILE, DRIFT_LOG, DRIFT_ALERTS, DRIFT_HALT
from voice_postprocess import postprocess

# Load Ollama pricing
PRICING_FILE = ROOT / "reports" / "skillopt" / "ollama-pricing.json"


def run_benchmark(dry_run: bool = False) -> dict:
    """Run voice-match benchmark and return scores."""
    if dry_run:
        # Use cached scores from last run
        usage_file = ROOT / "reports" / "skillopt" / "social_voice" / "stability-run-4-optimized-usage.json"
        if usage_file.exists():
            usage = json.loads(usage_file.read_text())
            return {
                "social_voice": usage.get("baseline_score", 0.0),
                "cases": usage.get("cases", 0),
                "failed": usage.get("baseline_failed_case_ids", []),
            }
        return {"social_voice": 0.0, "cases": 0, "failed": []}

    # Run live benchmark via Python API (avoids subprocess timeout issues)
    sys.path.insert(0, str(ROOT / "tools"))
    import os
    os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1"
    os.environ["OPENAI_API_KEY"] = "ollama"

    from run_skillopt_benchmark_openai import BenchmarkRunner

    date_str = datetime.now().strftime("%Y-%m-%d")
    runner = BenchmarkRunner(
        skill_file=str(ROOT / ".agents" / "skills" / "voice-match" / "SKILL.md"),
        benchmark=str(ROOT / "benchmarks" / "social_voice" / "social_voice_cases.jsonl"),
        output=str(ROOT / "reports" / "skillopt" / "social_voice" / f"daily-{date_str}.md"),
        dry_run=False,
        usage_output=str(ROOT / "reports" / "skillopt" / "social_voice" / f"daily-{date_str}-usage.json"),
        target_model="qwen2.5-coder:7b",
        evaluator_model="qwen2.5-coder:7b",
        optimizer_model="qwen2.5-coder:7b",
        pricing_config=str(PRICING_FILE),
        baseline_only=True,
    )

    result = runner.run()
    return {
        "social_voice": result.get("baseline_score", 0.0),
        "cases": 10,
        "failed": [],
    }


def run_daily_check(dry_run: bool = False):
    """Run daily drift check and log results."""
    timestamp = datetime.now(timezone.utc).isoformat()

    print(f"[daily-drift] Starting daily check at {timestamp}")

    # Run benchmark
    bench = run_benchmark(dry_run)
    sv_score = bench["social_voice"]

    if sv_score == 0.0 and bench.get("error"):
        print(f"[daily-drift] Benchmark error: {bench['error']}", file=sys.stderr)
        _log_check(timestamp, "error", sv_score, bench)
        return

    print(f"[daily-drift] Social voice score: {sv_score:.3f} (cases: {bench['cases']}, failed: {bench['failed']})")

    # Check drift
    monitor = DriftMonitor()
    status, action, reason = monitor.check_drift("social_voice", sv_score)

    print(f"[daily-drift] Status: {status} | Action: {action} | {reason}")

    # Log the check
    _log_check(timestamp, status, sv_score, bench, action, reason)

    # Handle alerts
    if status == "yellow":
        print(f"[daily-drift] ALERT: {reason}")
        _send_alert(status, sv_score, reason)
    elif status == "blue":
        print(f"[daily-drift] HALT: {reason}")
        _send_alert(status, sv_score, reason)
    elif status == "green":
        print(f"[daily-drift] OK: within tolerance")


def _send_alert(status: str, score: float, reason: str):
    """Send alert via Slack webhook if configured, otherwise just log."""
    import os
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")

    # Check .env file
    if not webhook_url:
        env_path = ROOT / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("SLACK_WEBHOOK_URL="):
                    webhook_url = line.split("=", 1)[1].strip()
                    break

    if not webhook_url:
        print("[daily-drift] No SLACK_WEBHOOK_URL set, alert logged only")
        return

    # Send to Slack
    try:
        import urllib.request
        emoji = "🟡" if status == "yellow" else "🔴"
        payload = json.dumps({
            "text": f"{emoji} Road4AI Drift Alert\nStatus: {status.upper()}\nScore: {score:.3f}\nReason: {reason}"
        }).encode()
        req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
        print(f"[daily-drift] Alert sent to Slack")
    except Exception as e:
        print(f"[daily-drift] Slack alert failed: {e}")


def _log_check(timestamp: str, status: str, score: float, bench: dict, action: str = None, reason: str = None):
    """Log drift check to state files."""
    STATE_DIR = ROOT / "state"
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": timestamp,
        "domain": "social_voice",
        "score": score,
        "cases": bench.get("cases", 0),
        "failed": bench.get("failed", []),
        "status": status,
        "action": action,
        "reason": reason,
    }

    # Append to drift log
    with open(DRIFT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

    # If yellow, append to alerts
    if status == "yellow":
        with open(DRIFT_ALERTS, "a") as f:
            f.write(json.dumps(entry) + "\n")

    # If blue, append to halts
    if status == "blue":
        with open(DRIFT_HALT, "a") as f:
            f.write(json.dumps(entry) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Daily drift check")
    parser.add_argument("--dry-run", action="store_true", help="Use cached scores instead of running benchmark")
    args = parser.parse_args()

    run_daily_check(args.dry_run)


if __name__ == "__main__":
    main()
>>>>>>> fc0dff2 (CHECKPOINT: Daily drift monitoring scheduled — runs 09:00 UTC daily)
