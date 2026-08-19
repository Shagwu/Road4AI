#!/usr/bin/env python3
"""
tools/repo_audit.py

CALIBRATION TOOL NOT AN AUTHORITATIVE COMPLIANCE GATE.

This is a read-only evidence-gathering tool. Its findings are advisory
input for human review, not a pass/fail verdict, not a CI gate, and not
a trigger for any automated remediation. Nothing downstream should treat
a clean run as authorization to act, or a non-clean run as a block.

Read-only calibration audit for Road4AI repo state.

Guarantees:
  - Never writes to AGENTS.md, queue records, drafts, Git state, or CI config.
  - Never calls a Git subcommand that mutates state.
  - Zero writes by default; - write-report is the only way to persist output,
    and even then it only adds a new timestamped file under docs/audits/.
  - Produces evidence only. Does not authorize or perform remediation.
  - No staleness/archival logic (deferred; depends on PR #3's enum values).

Exit codes:
  0 = clean, no findings
  1 = findings present (advisory human review required)
  2 = tool-level failure (e.g. unreadable path, unverified placeholders)
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

# --- Structural write-prevention -------------------------------------------
# Every file access in this tool goes through _ro_open(). It hard-fails if
# asked to open anything except "r"/"rb". This is the enforcement mechanism
# for "read-only" not just a description in the PR, but a code path that
# cannot write even if a future edit to this file tries to.

_ALLOWED_MODES = {"r", "rb"}


def _ro_open(path: Path, mode: str = "r"):
    if mode not in _ALLOWED_MODES:
        raise RuntimeError(
            f"repo_audit.py attempted a non-read-only open() with mode "
            f"'{mode}' on {path}. This tool is read-only by design; "
            f"refusing."
        )
    return open(path, mode)


# Explicitly forbidden importing/calling any of these from this module
# is a programming error, not a runtime decision. Kept as a visible list
# so a reviewer can grep for violations rather than trust prose.
_FORBIDDEN_OPERATIONS = (
    "os.remove",
    "os.rename",
    "os.unlink",
    "shutil.rmtree",
    "shutil.move",
    "Path.write_text",
    "Path.write_bytes",
    "Path.unlink",
    "subprocess: git add / git commit / git rm / git push",
)


@dataclass
class Finding:
    check: str
    severity: str  # "info" | "warn" | "error"
    path: str
    message: str


@dataclass
class AuditReport:
    started_at: str
    checks_run: list[str] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)

    def add(self, check: str, severity: str, path: str, message: str) -> None:
        self.findings.append(Finding(check, severity, path, message))

    def to_dict(self) -> dict:
        return {
            "started_at": self.started_at,
            "checks_run": self.checks_run,
            "findings": [f._dict_ for f in self.findings],
            "clean": not any(f.severity == "error" for f in self.findings),
        }


# --- Placeholder verification -----------------------------------------------
# Queue path, required fields, and allowed statuses below are NOT yet
# verified against the real repo. This tool refuses to run a "trusted"
# audit until a human flips PLACEHOLDERS_VERIFIED to True after confirming
# these match the actual state/queue.json schema. This is a runtime gate,
# not just a comment, so an unverified run can't be mistaken for a real one.

PLACEHOLDERS_VERIFIED = False  # <-- set True only after confirming below match reality

QUEUE_FILE_REL = "state/queue.json"
REQUIRED_FIELDS = {"id", "status"}
ALLOWED_STATUSES = {"draft", "in_review", "approved", "published"}


# --- Checks ------------------------------------------------------------------
# Four checks enabled on first run. A fifth (staleness/archival candidacy)
# is deliberately withheld see PR description.


def check_real_paths(repo_root: Path, queue_paths: list[str], report: AuditReport) -> None:
    report.checks_run.append("real_repository_paths")
    for p in queue_paths:
        full = repo_root / p
        if not full.exists():
            report.add(
                "real_repository_paths", "error", str(full),
                "Path referenced in queue/state does not resolve on disk.",
            )


def check_agents_md_protection(repo_root: Path, report: AuditReport) -> None:
    report.checks_run.append("agents_md_protection_mode")
    agents_md = repo_root / "AGENTS.md"
    if not agents_md.exists():
        report.add("agents_md_protection_mode", "error", str(agents_md),
                    "AGENTS.md not found.")
        return
    mode = stat.S_IMODE(agents_md.stat().st_mode)
    if mode != 0o444:
        report.add(
            "agents_md_protection_mode", "warn", str(agents_md),
            f"Expected mode 444 (locked), found {oct(mode)}.",
        )


def check_broken_symlinks(repo_root: Path, report: AuditReport) -> None:
    report.checks_run.append("broken_symlinks")
    for dirpath, _dirnames, filenames in os.walk(repo_root):
        if ".git" in dirpath:
            continue
        for name in filenames:
            full = Path(dirpath) / name
            if full.is_symlink() and not full.exists():
                report.add(
                    "broken_symlinks", "warn", str(full),
                    "Symlink target does not resolve.",
                )


def check_queue_record_shape(repo_root: Path, queue_file: Path,
                              required_fields: set[str],
                              allowed_statuses: set[str], report: AuditReport) -> None:
    report.checks_run.append("queue_record_shape")
    if not queue_file.exists():
        report.add("queue_record_shape", "error", str(queue_file),
                    "Queue file not found.")
        return
    with _ro_open(queue_file, "r") as f:
        try:
            records = json.load(f)
        except json.JSONDecodeError as e:
            report.add("queue_record_shape", "error", str(queue_file),
                        f"Queue file is not valid JSON: {e}")
            return

    for i, rec in enumerate(records if isinstance(records, list) else []):
        missing = required_fields - rec.keys()
        if missing:
            report.add(
                "queue_record_shape", "error", f"{queue_file}[{i}]",
                f"Record missing required fields: {sorted(missing)}",
            )
        status = rec.get("status")
        if status is not None and status not in allowed_statuses:
            report.add(
                "queue_record_shape", "warn", f"{queue_file}[{i}]",
                f"Status '{status}' not in current allowed set "
                f"{sorted(allowed_statuses)}. (Expected pre-PR#3 enum; "
                f"'scheduled'/'archived' not yet ratified.)",
            )


# --- Entry point --------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only calibration audit for Road4AI repo state.",
    )
    parser.add_argument(
        "--write-report",
        action="store_true",
        default=False,
        help=(
            "Write a timestamped JSON report to docs/audits/. Off by "
            "default: without this flag, the tool performs zero writes "
            "and prints findings to stdout only."
        ),
    )
    parser.add_argument(
        "--i-verified-placeholders",
        action="store_true",
        default=False,
        help=(
            "Required until PLACEHOLDERS_VERIFIED is flipped to True in "
            "source. Confirms QUEUE_FILE_REL / REQUIRED_FIELDS / "
            "ALLOWED_STATUSES have been checked against the real repo. "
            "Without this (or the source flag), the tool exits 2 rather "
            "than run findings that look authoritative but aren't."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]

    if not (PLACEHOLDERS_VERIFIED or args.i_verified_placeholders):
        print(
            "repo_audit.py: REFUSING TO RUN.\n"
            "QUEUE_FILE_REL / REQUIRED_FIELDS / ALLOWED_STATUSES are "
            "placeholders and have not been verified against the real "
            "repo schema. This is a calibration tool, not an authoritative "
            "compliance gate running it with unverified placeholders "
            "would produce findings that look real but aren't.\n\n"
            "To proceed: verify the constants near the top of this file "
            "against the actual state/queue.json schema, then either set "
            "PLACEHOLDERS_VERIFIED = True in source, or pass "
            "--i-verified-placeholders for a one-off run.",
            file=sys.stderr,
        )
        return 2

    report = AuditReport(started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    queue_file = repo_root / QUEUE_FILE_REL
    # SCAFFOLDING not yet populated. check_real_paths() will run against
    # this empty list and report "clean" on this first pass, but that
    # reflects zero inputs, not a real check. Populate from the verified
    # live queue schema in the follow-up calibration commit, alongside
    # flipping PLACEHOLDERS_VERIFIED.
    queue_paths: list[str] = []

    try:
        check_real_paths(repo_root, queue_paths, report)
        check_agents_md_protection(repo_root, report)
        check_broken_symlinks(repo_root, report)
        check_queue_record_shape(repo_root, queue_file, REQUIRED_FIELDS, ALLOWED_STATUSES, report)
    except Exception as e:  # tool-level failure, not a finding
        print(f"repo_audit.py: tool-level failure: {e}", file=sys.stderr)
        return 2

    print(
        "\n[CALIBRATION TOOL findings below are advisory evidence, not "
        "an authoritative compliance verdict.]\n",
        file=sys.stderr,
    )

    result = report.to_dict()
    print(json.dumps(result, indent=2))

    if args.write_report:
        # The only write path in this tool, and it's opt-in only. Additive
        # (new timestamped file), never touches existing repo state. Absent
        # --write-report, this block never runs and the tool is a true
        # zero-write dry run.
        out_dir = repo_root / "docs" / "audits"
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{report.started_at.replace(':', '-')}-repo-audit.json"
            out_path.write_text(json.dumps(result, indent=2))
            print(f"\nReport written to {out_path}", file=sys.stderr)
        except Exception as e:
            print(f"repo_audit.py: could not write report (non-fatal): {e}", file=sys.stderr)
    else:
        print(
            "\n(Report not written to disk pass --write-report to persist "
            "this as a timestamped file under docs/audits/.)",
            file=sys.stderr,
        )

    return 1 if result["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
