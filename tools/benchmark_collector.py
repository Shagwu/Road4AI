#!/usr/bin/env python3
"""
Benchmark Collector for SkillOpt

Collects benchmark cases from various sources for SkillOpt training.
Supports manual labeling, auto-generation from existing content,
and import from external sources.

Usage:
    # Collect from manual input
    python tools/benchmark_collector.py --mode manual --domain social_voice

    # Auto-generate from existing drafts
    python tools/benchmark_collector.py --mode auto --source drafts/

    # Import from external file
    python tools/benchmark_collector.py --mode import --input external_cases.jsonl

    # List collected cases
    python tools/benchmark_collector.py --mode list --domain social_voice
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


BENCHMARK_DIR = Path("benchmarks")
DOMAINS = ["social_voice", "memory_ops", "qa", "content_planning"]


def collect_manual(domain: str) -> dict:
    """Interactive manual collection of benchmark cases."""
    print(f"\n=== Manual Benchmark Collection: {domain} ===\n")
    print("Enter benchmark cases. Type 'done' to finish.\n")

    cases = []
    case_num = 1

    while True:
        print(f"--- Case {case_num} ---")
        case_id = input(f"ID (e.g., {domain[:2]}-{case_num:03d}): ").strip()
        if case_id.lower() == "done":
            break
        if not case_id:
            case_id = f"{domain[:2]}-{case_num:03d}"

        input_text = input("Input (what the agent should respond to): ").strip()
        if input_text.lower() == "done":
            break

        reference = input("Reference exemplar (good output): ").strip()
        if reference.lower() == "done":
            break

        expected_traits = input("Expected traits (comma-separated): ").strip()
        if expected_traits.lower() == "done":
            break
        expected_traits = [t.strip() for t in expected_traits.split(",") if t.strip()]

        reject_traits = input("Reject traits (comma-separated): ").strip()
        if reject_traits.lower() == "done":
            break
        reject_traits = [t.strip() for t in reject_traits.split(",") if t.strip()]

        case = {
            "id": case_id,
            "input": input_text,
            "expected_traits": expected_traits,
            "reject_traits": reject_traits,
            "reference": reference,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "source": "manual",
        }
        cases.append(case)
        case_num += 1
        print()

    return {"domain": domain, "cases": cases, "collected_at": datetime.now(timezone.utc).isoformat()}


def collect_auto(source_dir: str, domain: str) -> dict:
    """Auto-generate benchmark cases from existing content."""
    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"Error: Source directory not found: {source_path}")
        sys.exit(1)

    cases = []
    case_num = 1

    for md_file in source_path.rglob("*.md"):
        content = md_file.read_text()
        if len(content) < 100:
            continue

        # Extract first heading as potential input
        lines = content.split("\n")
        heading = ""
        for line in lines:
            if line.startswith("#"):
                heading = line.lstrip("#").strip()
                break

        if not heading:
            heading = md_file.stem.replace("-", " ").title()

        # Use first paragraph as reference
        reference = ""
        in_paragraph = False
        for line in lines:
            if line.strip() and not line.startswith("#"):
                reference = line.strip()
                break

        if not reference:
            reference = f"Content from {md_file.name}"

        case = {
            "id": f"{domain[:2]}-{case_num:03d}",
            "input": f"Draft content about: {heading}",
            "expected_traits": ["technical", "direct", "specific"],
            "reject_traits": ["vague", "buzzword-heavy"],
            "reference": reference[:200],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "source": str(md_file),
        }
        cases.append(case)
        case_num += 1

        if case_num > 20:
            break

    return {"domain": domain, "cases": cases, "collected_at": datetime.now(timezone.utc).isoformat()}


def collect_import(input_file: str, domain: str) -> dict:
    """Import benchmark cases from external file."""
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    cases = []
    for line_num, line in enumerate(input_path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            case = json.loads(line)
            # Validate required fields
            for field in ["id", "input", "expected_traits", "reject_traits", "reference"]:
                if field not in case:
                    print(f"Warning: Line {line_num} missing field '{field}', skipping")
                    continue
            case["created_at"] = datetime.now(timezone.utc).isoformat()
            case["source"] = str(input_path)
            cases.append(case)
        except json.JSONDecodeError:
            print(f"Warning: Line {line_num} is not valid JSON, skipping")

    return {"domain": domain, "cases": cases, "collected_at": datetime.now(timezone.utc).isoformat()}


def list_cases(domain: Optional[str] = None) -> None:
    """List collected benchmark cases."""
    if domain:
        domains = [domain]
    else:
        domains = DOMAINS

    for d in domains:
        benchmark_file = BENCHMARK_DIR / d / f"{d}_cases.jsonl"
        if benchmark_file.exists():
            cases = []
            for line in benchmark_file.read_text().splitlines():
                if line.strip():
                    cases.append(json.loads(line))
            print(f"\n=== {d}: {len(cases)} cases ===")
            for case in cases[:5]:
                print(f"  {case['id']}: {case['input'][:60]}...")
            if len(cases) > 5:
                print(f"  ... and {len(cases) - 5} more")
        else:
            print(f"\n=== {d}: No cases found ===")


def save_cases(collected: dict) -> None:
    """Save collected cases to benchmark file."""
    domain = collected["domain"]
    cases = collected["cases"]

    if not cases:
        print("No cases to save.")
        return

    benchmark_dir = BENCHMARK_DIR / domain
    benchmark_dir.mkdir(parents=True, exist_ok=True)

    benchmark_file = benchmark_dir / f"{domain}_cases.jsonl"

    # Append to existing cases
    existing_ids = set()
    if benchmark_file.exists():
        for line in benchmark_file.read_text().splitlines():
            if line.strip():
                case = json.loads(line)
                existing_ids.add(case["id"])

    new_cases = [c for c in cases if c["id"] not in existing_ids]

    if not new_cases:
        print(f"All {len(cases)} cases already exist in {benchmark_file}")
        return

    with open(benchmark_file, "a") as f:
        for case in new_cases:
            f.write(json.dumps(case) + "\n")

    print(f"Saved {len(new_cases)} new cases to {benchmark_file}")
    print(f"Total cases: {len(existing_ids) + len(new_cases)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark Collector for SkillOpt")
    parser.add_argument("--mode", choices=["manual", "auto", "import", "list"], required=True,
                        help="Collection mode")
    parser.add_argument("--domain", default="social_voice", choices=DOMAINS,
                        help="Benchmark domain")
    parser.add_argument("--source", help="Source directory for auto mode")
    parser.add_argument("--input", help="Input file for import mode")

    args = parser.parse_args()

    if args.mode == "list":
        list_cases(args.domain)
        return 0

    if args.mode == "manual":
        collected = collect_manual(args.domain)
    elif args.mode == "auto":
        if not args.source:
            print("Error: --source required for auto mode")
            return 1
        collected = collect_auto(args.source, args.domain)
    elif args.mode == "import":
        if not args.input:
            print("Error: --input required for import mode")
            return 1
        collected = collect_import(args.input, args.domain)

    print(f"\nCollected {len(collected['cases'])} cases for {collected['domain']}")
    save_cases(collected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
