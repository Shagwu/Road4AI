#!/usr/bin/env python3
"""
Multi-Domain Benchmark Runner for SkillOpt

Runs orchestration suite tests using local Ollama backend.
Tests cross-domain interactions between social_voice and memory_ops.

Usage:
    # Dry-run validation
    python tools/run_multi_domain_benchmark.py --dry-run

    # Live run with local models
    python tools/run_multi_domain_benchmark.py

    # Run specific cases
    python tools/run_multi_domain_benchmark.py --case orch-001,orch-002
"""

import argparse
import json
import time
import requests
from pathlib import Path
from typing import Optional


OLLAMA_ENDPOINT = "http://localhost:11434"
REASONING_MODEL = "qwen2.5-coder:14b"
ADVERSARIAL_MODEL = "mistral-nemo:latest"

BENCHMARK_FILE = Path("benchmarks/orchestration/orchestration_cases.jsonl")
OUTPUT_DIR = Path("reports/skillopt/orchestration")


class MultiDomainRunner:
    def __init__(self, dry_run: bool = False, cases: Optional[list] = None):
        self.dry_run = dry_run
        self.cases = self._load_cases(cases)
        self.results = []

    def _load_cases(self, filter_cases: Optional[list] = None) -> list:
        if not BENCHMARK_FILE.exists():
            raise FileNotFoundError(f"Benchmark file not found: {BENCHMARK_FILE}")

        cases = []
        for line in BENCHMARK_FILE.read_text().splitlines():
            if not line.strip():
                continue
            case = json.loads(line)
            if filter_cases and case["id"] not in filter_cases:
                continue
            cases.append(case)
        return cases

    def run(self) -> dict:
        if self.dry_run:
            return self._dry_run()
        return self._live_run()

    def _dry_run(self) -> dict:
        print("=== Dry-Run Validation ===")
        print(f"Cases loaded: {len(self.cases)}")
        print(f"Reasoning model: {REASONING_MODEL}")
        print(f"Adversarial model: {ADVERSARIAL_MODEL}")
        print(f"Endpoint: {OLLAMA_ENDPOINT}")

        # Validate case structure
        for case in self.cases:
            required = ["id", "input", "expected_traits", "reject_traits", "reference"]
            for field in required:
                if field not in case:
                    raise ValueError(f"Case {case.get('id', 'unknown')} missing field: {field}")

        print("\nAll cases valid. Ready for live mode.")
        return {"status": "ready", "cases": len(self.cases)}

    def _live_run(self) -> dict:
        print("=== Live Multi-Domain Run ===")
        start_time = time.time()

        for case in self.cases:
            print(f"\n--- {case['id']} ---")
            result = self._evaluate_case(case)
            self.results.append(result)
            print(f"  Score: {result['score']:.3f}")
            print(f"  Drift: {result['drift']:.3f}")

        elapsed = time.time() - start_time
        summary = self._summarize_results()

        # Save results
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_file = OUTPUT_DIR / f"{int(time.time())}-multi-domain-run.json"
        output_file.write_text(json.dumps(summary, indent=2))

        print(f"\n=== Summary ===")
        print(f"Total cases: {summary['total_cases']}")
        print(f"Average score: {summary['avg_score']:.3f}")
        print(f"Max drift: {summary['max_drift']:.3f}")
        print(f"Drift threshold breaches: {summary['drift_breaches']}")
        print(f"Elapsed: {elapsed:.1f}s")
        print(f"Results saved to: {output_file}")

        return summary

    def _evaluate_case(self, case: dict) -> dict:
        # Use reasoning model to evaluate
        prompt = f"""Evaluate this orchestration case. Return JSON with score (0-1) and drift (0-1).

Case: {case['input']}

Expected traits: {case['expected_traits']}
Reject traits: {case['reject_traits']}
Reference: {case['reference']}

Return JSON:
{{"score": 0.0, "drift": 0.0, "reasoning": "..."}}
"""

        if self.dry_run:
            return {"id": case["id"], "score": 0.0, "drift": 0.0, "reasoning": "dry-run"}

        try:
            response = requests.post(
                f"{OLLAMA_ENDPOINT}/api/generate",
                json={
                    "model": REASONING_MODEL,
                    "prompt": prompt,
                    "format": "json",
                    "stream": False
                },
                timeout=60
            )
            result = response.json()
            response_text = result.get("response", "{}")

            # Parse JSON response
            try:
                parsed = json.loads(response_text)
                return {
                    "id": case["id"],
                    "score": parsed.get("score", 0.0),
                    "drift": parsed.get("drift", 0.0),
                    "reasoning": parsed.get("reasoning", "")
                }
            except json.JSONDecodeError:
                return {
                    "id": case["id"],
                    "score": 0.0,
                    "drift": 1.0,
                    "reasoning": f"Failed to parse response: {response_text[:200]}"
                }
        except Exception as e:
            return {
                "id": case["id"],
                "score": 0.0,
                "drift": 1.0,
                "reasoning": f"Error: {str(e)}"
            }

    def _summarize_results(self) -> dict:
        scores = [r["score"] for r in self.results]
        drifts = [r["drift"] for r in self.results]

        return {
            "total_cases": len(self.results),
            "avg_score": sum(scores) / len(scores) if scores else 0,
            "max_drift": max(drifts) if drifts else 0,
            "drift_breaches": sum(1 for d in drifts if d > 0.05),
            "results": self.results
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-Domain Benchmark Runner")
    parser.add_argument("--dry-run", action="store_true", help="Validate without API calls")
    parser.add_argument("--case", help="Comma-separated case IDs to run")
    args = parser.parse_args()

    cases = args.case.split(",") if args.case else None
    runner = MultiDomainRunner(dry_run=args.dry_run, cases=cases)
    result = runner.run()

    if not args.dry_run and result.get("drift_breaches", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
