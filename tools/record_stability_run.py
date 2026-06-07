#!/usr/bin/env python3
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def gemini_version() -> str:
    try:
        result = subprocess.run(
            ["gemini", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() or result.stderr.strip() or "unknown"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def build_run_entry(args: argparse.Namespace, usage: dict) -> dict:
    return {
        "run_label": args.run_label,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "executor": args.executor,
        "git_commit": git_commit(),
        "command": args.command,
        "environment_notes": args.environment_notes,
        "gemini_cli_version": args.gemini_version or gemini_version(),
        "usage_report": str(args.usage_report),
        "mode": usage.get("mode"),
        "baseline_score": usage.get("baseline_score"),
        "baseline_score_stddev": usage.get("baseline_score_stddev"),
        "baseline_failed_case_ids": usage.get("baseline_failed_case_ids", []),
        "calls": usage.get("calls", {}),
        "case_count": usage.get("cases"),
    }


def append_run(stability_path: Path, run_entry: dict) -> dict:
    stability = read_json(stability_path)
    runs = stability.setdefault("runs", [])
    runs = [run for run in runs if run.get("run_label") != run_entry["run_label"]]
    runs.append(run_entry)
    stability["runs"] = runs
    stability["status"] = "in_progress"
    if len(runs) >= 2:
        stability["status"] = "ready_for_review"
    write_json(stability_path, stability)
    return stability


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a SkillOpt stability run usage report.")
    parser.add_argument("--usage-report", required=True, type=Path)
    parser.add_argument("--stability-runs", required=True, type=Path)
    parser.add_argument("--run-label", required=True, choices=["run_1", "run_2"])
    parser.add_argument("--executor", required=True, choices=["codex", "gemini"])
    parser.add_argument("--command", required=True)
    parser.add_argument("--environment-notes", default="")
    parser.add_argument("--gemini-version", default="")
    args = parser.parse_args()

    usage = read_json(args.usage_report)
    if usage.get("mode") != "baseline-only":
        raise SystemExit("Usage report must come from --baseline-only mode")

    run_entry = build_run_entry(args, usage)
    stability = append_run(args.stability_runs, run_entry)
    print(json.dumps({
        "status": stability["status"],
        "runs_recorded": len(stability.get("runs", [])),
        "recorded": run_entry["run_label"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
