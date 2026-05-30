#!/usr/bin/env python3
import argparse
import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path
from typing import Optional, Union


PROTECTED_FILES = {
    "AGENTS.md",
    "state/current-queue.json",
    "state/published-log.json",
    "docs/brand-voice.md",
    "docs/content-strategy.md",
}

ALLOWED_SKILL_PATTERNS = {
    "marketing-skills/skills/**/SKILL.md",
    ".agents/skills/**/SKILL.md",
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
    ):
        self.root = Path.cwd().resolve()
        self.skill_file = Path(skill_file)
        self.benchmark_file = Path(benchmark)
        self.output_file = Path(output)
        self.dry_run = dry_run
        self.failure_threshold = failure_threshold
        self.pricing_config_path = Path(pricing_config) if pricing_config else None

        if not self.dry_run:
            self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("Live mode requires OPENAI_API_KEY or --openai-api-key")
            if not usage_output:
                raise ValueError("Live mode requires --usage-output")
            if not pricing_config:
                raise ValueError("Live mode requires --pricing-config")
            if not target_model or not evaluator_model or not optimizer_model:
                raise ValueError("Live mode requires exact --target-model, --evaluator-model, and --optimizer-model")
            self.usage_output_file = Path(usage_output)
            self.pricing = self._load_pricing(pricing_config)
            self.target_model = target_model
            self.evaluator_model = evaluator_model
            self.optimizer_model = optimizer_model
            self._validate_pricing_models([self.target_model, self.evaluator_model, self.optimizer_model])
        else:
            self.api_key = None
            self.usage_output_file = Path(usage_output) if usage_output else None
            self.pricing = self._load_pricing(pricing_config) if pricing_config else None
            self.target_model = target_model or "gpt-4.1-2025-04-14"
            self.evaluator_model = evaluator_model or "gpt-4.1-2025-04-14"
            self.optimizer_model = optimizer_model or "gpt-4.1-2025-04-14"

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
        if skill_path in PROTECTED_FILES:
            raise ValueError(f"Error: {skill_path} is in protected files list")
        if not any(fnmatch(skill_path, pattern) for pattern in ALLOWED_SKILL_PATTERNS):
            raise ValueError(f"Error: {skill_path} does not match allowed patterns: {sorted(ALLOWED_SKILL_PATTERNS)}")

    def _load_pricing(self, config_path: str) -> dict:
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Pricing config not found: {path}")
        try:
            pricing = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            raise ValueError(f"Pricing config is not valid JSON: {exc}") from exc
        if not isinstance(pricing.get("models"), dict):
            raise ValueError("Pricing config must contain a models object")
        return pricing

    def _validate_pricing_models(self, models: list[str]) -> None:
        for model in models:
            model_config = self.pricing["models"].get(model)
            if not model_config:
                raise ValueError(f"Pricing config missing model: {model}")
            if "input_per_1m_tokens" not in model_config or "output_per_1m_tokens" not in model_config:
                raise ValueError(f"Pricing config for {model} must include input_per_1m_tokens and output_per_1m_tokens")

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
            "pricing_valid": self.pricing is not None,
            "would_call_estimate": {
                "target_model": f"{len(self.cases)} baseline + {len(self.cases)} optimized (if failures > 0)",
                "evaluator_model": f"{len(self.cases)} baseline + {len(self.cases)} optimized (if failures > 0)",
                "optimizer_model": "1 (if failures > 0, else 0)",
            },
            "note": "Dry-run validation passed. Ready for live mode. No API calls were made.",
        }
        self.output_file.write_text(self._render_dry_run_report(result))
        return result

    def _render_dry_run_report(self, result: dict) -> str:
        planned = "\n".join(f"- {role}: {estimate}" for role, estimate in result["would_call_estimate"].items())
        return (
            "# Dry-Run Validation Report\n\n"
            f"Status: {result['status']}\n\n"
            f"Benchmark: {result['cases_loaded']} cases\n"
            "Governance: passed\n"
            f"Pricing: {'configured' if result['pricing_valid'] else 'not provided'}\n\n"
            "## Planned API Calls If Live\n\n"
            f"{planned}\n\n"
            f"Note: {result['note']}\n"
        )

    def _live_run(self) -> dict:
        baseline_results = self._evaluate_skill(self.skill_file, optimized=False)
        baseline_mean = self._mean_score(baseline_results)
        failures = [result for result in baseline_results if result["eval"]["score"] < self.failure_threshold]

        edits = []
        optimized_results = baseline_results
        optimized_mean = baseline_mean
        if failures:
            edits = self._call_optimizer_with_retry(self.skill_file, failures)
            optimized_skill = self._apply_edits_in_memory(self.skill_file, edits)
            optimized_results = self._evaluate_skill(optimized_skill, optimized=True)
            optimized_mean = self._mean_score(optimized_results)
        else:
            self.usage["optimizer_model"].reason = "No failures found in baseline"

        usage_json = self._finalize_usage(baseline_mean, optimized_mean)
        self._write_report(baseline_results, optimized_results, usage_json, edits)
        self._write_usage_json(usage_json)
        return {
            "baseline_score": baseline_mean,
            "optimized_score": optimized_mean,
            "improvement_pct": self._improvement_pct(baseline_mean, optimized_mean),
            "report": str(self.output_file),
            "usage": str(self.usage_output_file),
        }

    def _evaluate_skill(self, skill_source: Union[Path, str], optimized: bool) -> list[dict]:
        results = []
        for case in self.cases:
            output = self._call_target_with_retry(skill_source, case["input"], optimized)
            eval_result = self._call_evaluator_with_retry(output, case["expected_traits"], case["reject_traits"], case["reference"])
            results.append({"case_id": case["id"], "input": case["input"], "output": output, "eval": eval_result})
        return results

    def _call_target_with_retry(self, skill_source: Union[Path, str], input_text: str, is_optimized: bool) -> str:
        skill_text = skill_source if is_optimized else Path(skill_source).read_text()
        response = self._call_openai_with_retry(
            model=self.target_model,
            messages=[{"role": "system", "content": skill_text}, {"role": "user", "content": input_text}],
            temperature=0.7,
            max_tokens=500,
        )
        self._record_usage("target_model", response)
        return response.choices[0].message.content or ""

    def _call_evaluator_with_retry(self, output: str, expected_traits: list, reject_traits: list, reference: str) -> dict:
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

Be rigorous. Mark conceptual errors explicitly.
"""
        response = self._call_openai_with_retry(
            model=self.evaluator_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=500,
            json_response=True,
        )
        self._record_usage("evaluator_model", response)
        eval_json = self._parse_json_response(response, "Evaluator")
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

    def _call_optimizer_with_retry(self, skill_file: Path, failures: list[dict]) -> list[dict]:
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
"""
        response = self._call_openai_with_retry(
            model=self.optimizer_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1200,
            json_response=True,
        )
        self._record_usage("optimizer_model", response)
        result = self._parse_json_response(response, "Optimizer")
        edits = result.get("edits", [])
        if not isinstance(edits, list):
            raise RuntimeError("Optimizer JSON field 'edits' must be a list")
        return edits

    def _call_openai_with_retry(self, model: str, messages: list, temperature: float, max_tokens: int, json_response: bool = False):
        from openai import APIConnectionError, APIError, APITimeoutError, AuthenticationError, BadRequestError, NotFoundError, OpenAI, PermissionDeniedError, RateLimitError

        client = OpenAI(api_key=self.api_key)
        kwargs = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if json_response:
            kwargs["response_format"] = {"type": "json_object"}

        for attempt in range(3):
            try:
                return client.chat.completions.create(**kwargs)
            except (AuthenticationError, BadRequestError, PermissionDeniedError, NotFoundError):
                raise
            except (RateLimitError, APITimeoutError, APIConnectionError) as exc:
                self._retry_or_raise(exc, attempt)
            except APIError as exc:
                if getattr(exc, "status_code", None) in TRANSIENT_STATUS_CODES:
                    self._retry_or_raise(exc, attempt)
                raise
        raise RuntimeError("Unexpected retry loop exit")

    def _retry_or_raise(self, exc: Exception, attempt: int) -> None:
        if attempt >= 2:
            raise exc
        wait_time = 2 ** attempt
        logging.warning("Transient OpenAI error; retrying in %ss: %s", wait_time, exc)
        time.sleep(wait_time)

    def _record_usage(self, role: str, response) -> None:
        usage = getattr(response, "usage", None)
        if usage is None:
            raise RuntimeError(f"{role} response did not include usage data")
        snapshot = self.usage[role]
        snapshot.calls += 1
        snapshot.prompt_tokens += int(getattr(usage, "prompt_tokens", 0) or 0)
        snapshot.completion_tokens += int(getattr(usage, "completion_tokens", 0) or 0)
        snapshot.total_tokens += int(getattr(usage, "total_tokens", 0) or 0)
        if snapshot.total_tokens <= 0:
            raise RuntimeError(f"{role} response usage had zero total tokens")

    def _parse_json_response(self, response, label: str) -> dict:
        content = response.choices[0].message.content or ""
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"{label} returned invalid JSON: {exc}") from exc
        if not isinstance(parsed, dict):
            raise RuntimeError(f"{label} JSON response must be an object")
        return parsed

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

    def _finalize_usage(self, baseline_mean: float, optimized_mean: float) -> dict:
        for role in ["target_model", "evaluator_model"]:
            if self.usage[role].total_tokens <= 0:
                raise RuntimeError(f"{role} has no token data")
        for snapshot in self.usage.values():
            if snapshot.total_tokens > 0:
                model_config = self.pricing["models"][snapshot.model_id]
                snapshot.cost_usd = (
                    snapshot.prompt_tokens * model_config["input_per_1m_tokens"] / 1_000_000
                    + snapshot.completion_tokens * model_config["output_per_1m_tokens"] / 1_000_000
                )
        pricing_config = {
            "path": self.pricing_config_path.as_posix(),
            "sha256": hashlib.sha256(self.pricing_config_path.read_bytes()).hexdigest(),
            "source": self.pricing.get("source", ""),
        }
        total_cost = sum(snapshot.cost_usd for snapshot in self.usage.values())
        usage = {
            "run_id": self._run_id(),
            "benchmark": self.benchmark_file.parent.name,
            "cases": len(self.cases),
            "pricing_config": pricing_config,
            "models": {role: snapshot.model_id for role, snapshot in self.usage.items()},
            "calls": {role: snapshot.calls for role, snapshot in self.usage.items()},
            "tokens": {
                role: {
                    "prompt": snapshot.prompt_tokens,
                    "completion": snapshot.completion_tokens,
                    "total": snapshot.total_tokens,
                }
                for role, snapshot in self.usage.items()
            },
            "estimated_cost_usd": {
                "target_model": self.usage["target_model"].cost_usd,
                "evaluator_model": self.usage["evaluator_model"].cost_usd,
                "optimizer_model": self.usage["optimizer_model"].cost_usd,
                "total": total_cost,
            },
            "reasons": {role: snapshot.reason for role, snapshot in self.usage.items() if snapshot.reason},
            "baseline_score": baseline_mean,
            "optimized_score": optimized_mean,
            "improvement_pct": self._improvement_pct(baseline_mean, optimized_mean),
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
            "# SkillOpt Benchmark Report",
            "",
            f"Benchmark: `{usage_json['benchmark']}`",
            f"Cases: {len(baseline_results)}",
            f"Baseline score: {baseline_mean:.3f}",
            f"Optimized score: {optimized_mean:.3f}",
            f"Improvement: {self._improvement_pct(baseline_mean, optimized_mean):.2f}%",
            f"Total estimated cost: ${usage_json['estimated_cost_usd']['total']:.4f}",
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
        self.usage_output_file.parent.mkdir(parents=True, exist_ok=True)
        self.usage_output_file.write_text(json.dumps(usage_json, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Governed SkillOpt benchmark runner with three-model evaluation.")
    parser.add_argument("--skill-file", "--skill-path", required=True, help="Path to the skill markdown file")
    parser.add_argument("--benchmark", "--cases-path", required=True, help="Path to the benchmark JSONL file")
    parser.add_argument("--output", required=True, help="Path to write the markdown report")
    parser.add_argument("--dry-run", action="store_true", help="Perform validation without making API calls")
    parser.add_argument("--usage-output", help="Path to write the detailed JSON usage report")
    parser.add_argument("--pricing-config")
    parser.add_argument("--target-model")
    parser.add_argument("--evaluator-model")
    parser.add_argument("--optimizer-model")
    parser.add_argument("--failure-threshold", type=float, default=0.7)
    parser.add_argument("--openai-api-key")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        runner = BenchmarkRunner(
            skill_file=args.skill_file,
            benchmark=args.benchmark,
            output=args.output,
            dry_run=args.dry_run,
            pricing_config=args.pricing_config,
            usage_output=args.usage_output,
            target_model=args.target_model,
            evaluator_model=args.evaluator_model,
            optimizer_model=args.optimizer_model,
            failure_threshold=args.failure_threshold,
            openai_api_key=args.openai_api_key,
        )
        result = runner.run()
        print(json.dumps(result, indent=2))
        
        # If live and score below threshold, could exit 1 if desired by project.yaml
        # But acceptance_criteria says "exits 0 on all-pass, exits 1 on any failure"
        if not args.dry_run:
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
