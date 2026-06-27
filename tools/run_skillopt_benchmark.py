#!/usr/bin/env python3
# DEPRECATED: This Gemini CLI backend is unreliable and times out.
# Use run_skillopt_benchmark_openai.py instead for live benchmarking.
import argparse
import hashlib
import json
import logging
import os
import subprocess
import tempfile
import time
from statistics import pstdev
from dataclasses import dataclass
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path
from typing import Optional, Union


PROTECTED_FILES = {
    "AGENTS.md",
    "project.yaml",
    "docs/brand-voice.md",
    "docs/content-strategy.md",
    "state/*.json",
    "state/*.yaml",
    "rules/common/*.md",
    "rules/python/*.md",
}

ALLOWED_SKILL_PATTERNS = {
    "marketing-skills/skills/**/SKILL.md",
    "skills/**/SKILL.md",
    "rules/content/*.md",
}

TRANSIENT_STATUS_CODES = {408, 409, 429, 500, 502, 503, 504}


@dataclass
class UsageSnapshot:
    model_id: str
    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    reason: str = ""


class BenchmarkRunner:
    def __init__(
        self,
        skill_file: str,
        benchmark: str,
        output: str,
        dry_run: bool,
        pricing_config: Optional[str] = None,
        usage_output: Optional[str] = None,
        target_model: Optional[str] = None,
        evaluator_model: Optional[str] = None,
        optimizer_model: Optional[str] = None,
        failure_threshold: float = 0.7,
        openai_api_key: Optional[str] = None,
        baseline_only: bool = False,
    ):
        self.root = Path.cwd().resolve()
        self.skill_file = Path(skill_file)
        self.benchmark_file = Path(benchmark)
        self.output_file = Path(output)
        self.dry_run = dry_run
        self.baseline_only = baseline_only
        self.failure_threshold = failure_threshold
        self.pricing_config_path = Path(pricing_config) if pricing_config else None

        # Gemini CLI doesn't use these, but we keep them for CLI compatibility
        self.target_model = "gemini-cli"
        self.evaluator_model = "gemini-cli"
        self.optimizer_model = "gemini-cli"
        
        if not self.dry_run:
            if not usage_output:
                raise ValueError("Live mode requires --usage-output")
            self.usage_output_file = Path(usage_output)
        else:
            self.usage_output_file = Path(usage_output) if usage_output else None

        self._check_protected_file()
        self.cases = self._load_benchmark_cases()
        self.usage = {
            "target_model": UsageSnapshot(model_id=self.target_model),
            "evaluator_model": UsageSnapshot(model_id=self.evaluator_model),
            "optimizer_model": UsageSnapshot(model_id=self.optimizer_model),
        }

    def _repo_relative_path(self, path: Path) -> str:
        resolved = path.resolve()
        try:
            return resolved.relative_to(self.root).as_posix()
        except ValueError as exc:
            raise ValueError(f"Path is outside repository: {path}") from exc

    def _check_protected_file(self) -> None:
        skill_path = self._repo_relative_path(self.skill_file)
        
        # Check against protected patterns
        for pattern in PROTECTED_FILES:
            if fnmatch(skill_path, pattern):
                raise ValueError(f"Error: {skill_path} matches protected pattern: {pattern}")
        
        # Check against allowed patterns
        if not any(fnmatch(skill_path, pattern) for pattern in ALLOWED_SKILL_PATTERNS):
            raise ValueError(f"Error: {skill_path} does not match any allowed skill patterns: {sorted(ALLOWED_SKILL_PATTERNS)}")

    def _load_benchmark_cases(self) -> list[dict]:
        if not self.benchmark_file.exists():
            raise FileNotFoundError(f"Benchmark file not found: {self.benchmark_file}")
        cases = []
        for line_num, line in enumerate(self.benchmark_file.read_text().splitlines(), start=1):
            if not line.strip():
                continue
            try:
                case = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Line {line_num} is not valid JSON: {exc}") from exc
            self._validate_case(case, line_num)
            cases.append(case)
        if not cases:
            raise ValueError("Benchmark file is empty")
        return cases

    def _validate_case(self, case: dict, line_num: int) -> None:
        for field in ["id", "input", "expected_traits", "reject_traits", "reference"]:
            if field not in case:
                raise ValueError(f"Line {line_num}: missing required field '{field}'")
        if not isinstance(case["expected_traits"], list):
            raise ValueError(f"Line {line_num}: expected_traits must be a list")
        if not isinstance(case["reject_traits"], list):
            raise ValueError(f"Line {line_num}: reject_traits must be a list")
        if not isinstance(case["reference"], str):
            raise ValueError(f"Line {line_num}: reference must be a string")

    def run(self) -> dict:
        return self._dry_run() if self.dry_run else self._live_run()

    def _dry_run(self) -> dict:
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        result = {
            "status": "ready",
            "cases_loaded": len(self.cases),
            "governance_passed": True,
            "note": "Dry-run validation passed. Ready for live mode via Gemini CLI. No API calls were made.",
        }
        self.output_file.write_text(self._render_dry_run_report(result))
        return result

    def _render_dry_run_report(self, result: dict) -> str:
        return (
            "# Dry-Run Validation Report (Gemini CLI)\n\n"
            f"Status: {result['status']}\n\n"
            f"Benchmark: {result['cases_loaded']} cases\n"
            "Governance: passed\n"
            "Engine: gemini-cli\n\n"
            f"Note: {result['note']}\n"
        )

    def _live_run(self) -> dict:
        baseline_results = self._evaluate_skill(self.skill_file, optimized=False)
        baseline_mean = self._mean_score(baseline_results)
        failures = [result for result in baseline_results if result["eval"]["score"] < self.failure_threshold]

        edits = []
        optimized_results = baseline_results
        optimized_mean = baseline_mean
        if self.baseline_only:
            self.usage["optimizer_model"].reason = "Baseline-only mode"
        elif failures:
            edits = self._call_optimizer(self.skill_file, failures)
            optimized_skill = self._apply_edits_in_memory(self.skill_file, edits)
            optimized_results = self._evaluate_skill(optimized_skill, optimized=True)
            optimized_mean = self._mean_score(optimized_results)
        else:
            self.usage["optimizer_model"].reason = "No failures found in baseline"

        usage_json = self._finalize_usage(baseline_mean, optimized_mean, baseline_results, optimized_results)
        self._write_report(baseline_results, optimized_results, usage_json, edits)
        self._write_usage_json(usage_json)
        return {
            "baseline_score": baseline_mean,
            "optimized_score": optimized_mean,
            "improvement_pct": self._improvement_pct(baseline_mean, optimized_mean),
            "baseline_only": self.baseline_only,
            "report": str(self.output_file),
            "usage": str(self.usage_output_file),
        }

    def _evaluate_skill(self, skill_source: Union[Path, str], optimized: bool) -> list[dict]:
        results = []
        for case in self.cases:
            output = self._call_target(skill_source, case["input"], optimized)
            eval_result = self._call_evaluator(output, case["expected_traits"], case["reject_traits"], case["reference"])
            results.append({"case_id": case["id"], "input": case["input"], "output": output, "eval": eval_result})
        return results

    def _call_target(self, skill_source: Union[Path, str], input_text: str, is_optimized: bool) -> str:
        skill_text = skill_source if is_optimized else Path(skill_source).read_text()
        prompt = f"System Instruction:\n{skill_text}\n\nTask: {input_text}\n\nResponse:"
        response = self._call_gemini_cli(prompt)
        self.usage["target_model"].calls += 1
        return response

    def _call_evaluator(self, output: str, expected_traits: list, reject_traits: list, reference: str) -> dict:
        prompt = f"""
You are an evaluator for Road4AI social voice.

Output to evaluate:
{output}

Expected traits (should be present): {expected_traits}
Reject traits (should be absent): {reject_traits}
Reference exemplar (for alignment, not exact answer): {reference}

Return structured evaluation in JSON:
{{
  "expected_traits_met": ["list"],
  "expected_traits_missed": ["list"],
  "reject_traits_present": ["list"],
  "reject_traits_avoided": ["list"],
  "reference_alignment": 0.0,
  "reasoning": "Specific explanation."
}}

Be rigorous. Mark conceptual errors explicitly. Return ONLY the JSON object.
"""
        response = self._call_gemini_cli(prompt)
        self.usage["evaluator_model"].calls += 1
        eval_json = self._parse_json_from_gemini(response, "Evaluator")
        return self._score_eval(eval_json)

    def _score_eval(self, eval_json: dict) -> dict:
        expected_met = len(eval_json.get("expected_traits_met", []))
        expected_missed = len(eval_json.get("expected_traits_missed", []))
        expected_total = expected_met + expected_missed
        reject_present = len(eval_json.get("reject_traits_present", []))
        reference_alignment = float(eval_json.get("reference_alignment", 0.5))
        reference_alignment = min(max(reference_alignment, 0.0), 1.0)
        expected_score = expected_met / expected_total if expected_total else 1.0
        reject_score = 1.0 if reject_present == 0 else 0.3
        score = (expected_score * 0.5) + (reject_score * 0.3) + (reference_alignment * 0.2)
        return {
            "score": score,
            "expected_traits_met": eval_json.get("expected_traits_met", []),
            "expected_traits_missed": eval_json.get("expected_traits_missed", []),
            "reject_traits_present": eval_json.get("reject_traits_present", []),
            "reject_traits_avoided": eval_json.get("reject_traits_avoided", []),
            "reference_alignment": reference_alignment,
            "reasoning": eval_json.get("reasoning", ""),
        }

    def _call_optimizer(self, skill_file: Path, failures: list[dict]) -> list[dict]:
        skill_text = skill_file.read_text()
        failure_text = "\n".join(
            f"Case {failure['case_id']}: score {failure['eval']['score']:.2f}\n"
            f"Input: {failure['input']}\n"
            f"Output: {failure['output']}\n"
            f"Missed: {failure['eval']['expected_traits_missed']}\n"
            f"Rejected traits present: {failure['eval']['reject_traits_present']}\n"
            f"Reasoning: {failure['eval']['reasoning']}"
            for failure in failures[:5]
        )
        prompt = f"""
Current skill document:
```
{skill_text}
```

Recent benchmark failures:
{failure_text}

Propose 1-3 minimal edits to improve the skill.
Return JSON:
{{
  "edits": [
    {{"type": "add", "section": "...", "content": "..."}}
  ],
  "reasoning": "Why these edits help"
}}
Return ONLY the JSON object.
"""
        response = self._call_gemini_cli(prompt)
        self.usage["optimizer_model"].calls += 1
        result = self._parse_json_from_gemini(response, "Optimizer")
        edits = result.get("edits", [])
        if not isinstance(edits, list):
            raise RuntimeError("Optimizer JSON field 'edits' must be a list")
        return edits

    def _call_gemini_cli(self, prompt: str) -> str:
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as tf:
            tf.write(prompt)
            temp_path = tf.name
        
        try:
            cmd = ["gemini", "-p", f"file:{temp_path}"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as exc:
            logging.error("Gemini CLI failed: %s", exc.stderr)
            raise RuntimeError(f"Gemini CLI execution failed: {exc.stderr}") from exc
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def _parse_json_from_gemini(self, response: str, label: str) -> dict:
        # Strip markdown fences if present
        clean_response = response.strip()
        if clean_response.startswith("```"):
            lines = clean_response.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            clean_response = "\n".join(lines).strip()
            
        try:
            # Look for the JSON object in the string
            start_idx = clean_response.find("{")
            end_idx = clean_response.rfind("}")
            if start_idx != -1 and end_idx != -1:
                json_str = clean_response[start_idx:end_idx+1]
                return json.loads(json_str)
            return json.loads(clean_response)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"{label} returned invalid JSON: {exc}\nResponse: {response}") from exc

    def _apply_edits_in_memory(self, skill_file: Path, edits: list[dict]) -> str:
        skill_text = skill_file.read_text()
        for edit in edits:
            edit_type = edit.get("type")
            if edit_type != "add":
                raise ValueError(f"Unsupported optimizer edit type: {edit_type}. Only 'add' is supported in v2.1.")
            section = edit.get("section")
            content = edit.get("content")
            if not section or not content:
                raise ValueError("Add edits require section and content")
            skill_text += f"\n\n## {section}\n{content}\n"
        return skill_text

    def _score_stddev(self, results: list[dict]) -> float:
        scores = [result["eval"]["score"] for result in results]
        return pstdev(scores) if len(scores) > 1 else 0.0

    def _failed_case_ids(self, results: list[dict]) -> list[str]:
        return [
            result["case_id"]
            for result in results
            if result["eval"]["score"] < self.failure_threshold
        ]

    def _case_results(self, results: list[dict]) -> list[dict]:
        return [
            {
                "case_id": result["case_id"],
                "score": result["eval"]["score"],
                "expected_traits_missed": result["eval"]["expected_traits_missed"],
                "reject_traits_present": result["eval"]["reject_traits_present"],
                "reference_alignment": result["eval"]["reference_alignment"],
                "reasoning": result["eval"]["reasoning"],
            }
            for result in results
        ]

    def _finalize_usage(
        self,
        baseline_mean: float,
        optimized_mean: float,
        baseline_results: list[dict],
        optimized_results: list[dict],
    ) -> dict:
        usage = {
            "run_id": self._run_id(),
            "mode": "baseline-only" if self.baseline_only else "full",
            "benchmark": self.benchmark_file.parent.name,
            "cases": len(self.cases),
            "models": {role: snapshot.model_id for role, snapshot in self.usage.items()},
            "calls": {role: snapshot.calls for role, snapshot in self.usage.items()},
            "estimated_cost_usd": {
                "total": 0.0,
                "note": "Gemini CLI free tier"
            },
            "reasons": {role: snapshot.reason for role, snapshot in self.usage.items() if snapshot.reason},
            "baseline_score": baseline_mean,
            "optimized_score": optimized_mean,
            "baseline_score_stddev": self._score_stddev(baseline_results),
            "optimized_score_stddev": self._score_stddev(optimized_results),
            "baseline_failed_case_ids": self._failed_case_ids(baseline_results),
            "optimized_failed_case_ids": self._failed_case_ids(optimized_results),
            "improvement_pct": self._improvement_pct(baseline_mean, optimized_mean),
            "baseline_case_results": self._case_results(baseline_results),
            "optimized_case_results": self._case_results(optimized_results),
        }
        return usage

    def _run_id(self) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        return f"{timestamp}-{self.benchmark_file.parent.name}"

    def _mean_score(self, results: list[dict]) -> float:
        return sum(result["eval"]["score"] for result in results) / len(results)

    def _improvement_pct(self, baseline_mean: float, optimized_mean: float) -> float:
        return ((optimized_mean - baseline_mean) / baseline_mean * 100) if baseline_mean > 0 else 0.0

    def _write_report(self, baseline_results: list[dict], optimized_results: list[dict], usage_json: dict, edits: list[dict]) -> None:
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        baseline_mean = self._mean_score(baseline_results)
        optimized_mean = self._mean_score(optimized_results)
        lines = [
            "# SkillOpt Benchmark Report (Gemini CLI)",
            "",
            f"Benchmark: `{usage_json['benchmark']}`",
            f"Cases: {len(baseline_results)}",
            f"Baseline score: {baseline_mean:.3f}",
            f"Baseline std dev: {self._score_stddev(baseline_results):.3f}",
            f"Optimized score: {optimized_mean:.3f}",
            f"Optimized std dev: {self._score_stddev(optimized_results):.3f}",
            f"Improvement: {self._improvement_pct(baseline_mean, optimized_mean):.2f}%",
            "Total estimated cost: $0.0000 (Gemini CLI)",
            "",
            "## Proposed Edits",
            "",
        ]
        if edits:
            for index, edit in enumerate(edits, start=1):
                lines.extend([
                    f"### Edit {index}",
                    "",
                    f"Type: `{edit.get('type')}`",
                    f"Section: `{edit.get('section')}`",
                    "",
                    "```",
                    edit.get("content", ""),
                    "```",
                    "",
                ])
        else:
            lines.extend(["No edits proposed.", ""])
        lines.extend(["## Case Results", ""])
        for baseline, optimized in zip(baseline_results, optimized_results):
            lines.extend([
                f"### {baseline['case_id']}",
                "",
                f"Baseline score: {baseline['eval']['score']:.3f}",
                f"Optimized score: {optimized['eval']['score']:.3f}",
                f"Baseline reasoning: {baseline['eval']['reasoning']}",
                f"Optimized reasoning: {optimized['eval']['reasoning']}",
                "",
            ])
        self.output_file.write_text("\n".join(lines))

    def _write_usage_json(self, usage_json: dict) -> None:
        if self.usage_output_file:
            self.usage_output_file.parent.mkdir(parents=True, exist_ok=True)
            self.usage_output_file.write_text(json.dumps(usage_json, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Governed SkillOpt benchmark runner using Gemini CLI.")
    parser.add_argument("--skill-file", "--skill-path", required=True, help="Path to the skill markdown file")
    parser.add_argument("--benchmark", "--cases-path", required=True, help="Path to the benchmark JSONL file")
    parser.add_argument("--output", required=True, help="Path to write the markdown report")
    parser.add_argument("--dry-run", action="store_true", help="Perform validation without making API calls")
    parser.add_argument("--baseline-only", action="store_true", help="Run live baseline scoring only; skip optimization and after-score")
    parser.add_argument("--usage-output", help="Path to write the detailed JSON usage report")
    parser.add_argument("--failure-threshold", type=float, default=0.7)
    
    # Kept for backward compatibility with OpenAI version CLI
    parser.add_argument("--pricing-config", help="Ignored (using Gemini free tier)")
    parser.add_argument("--target-model", help="Ignored (using gemini-cli)")
    parser.add_argument("--evaluator-model", help="Ignored (using gemini-cli)")
    parser.add_argument("--optimizer-model", help="Ignored (using gemini-cli)")
    parser.add_argument("--openai-api-key", help="Ignored")
    
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        runner = BenchmarkRunner(
            skill_file=args.skill_file,
            benchmark=args.benchmark,
            output=args.output,
            dry_run=args.dry_run,
            usage_output=args.usage_output,
            failure_threshold=args.failure_threshold,
            baseline_only=args.baseline_only,
        )
        result = runner.run()
        print(json.dumps(result, indent=2))
        
        if not args.dry_run and not args.baseline_only:
            if result.get("baseline_score", 1.0) < args.failure_threshold:
                 return 1
            if result.get("optimized_score", 1.0) < args.failure_threshold:
                 return 1
                 
        return 0
    except Exception as exc:
        logging.error("%s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
