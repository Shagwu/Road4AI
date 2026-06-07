import importlib.util
import json
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "run_skillopt_benchmark.py"
SPEC = importlib.util.spec_from_file_location("run_skillopt_benchmark", MODULE_PATH)
runner_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner_module)


BenchmarkRunner = runner_module.BenchmarkRunner


def write_jsonl(path: Path, cases: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(case) for case in cases) + "\n")


def write_pricing(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "source": "https://openai.com/api/pricing/",
        "models": {
            "gpt-4.1-2025-04-14": {
                "input_per_1m_tokens": 2.0,
                "output_per_1m_tokens": 8.0,
            }
        },
    }))


def valid_case() -> dict:
    return {
        "id": "sv-001",
        "input": "Draft a hook.",
        "expected_traits": ["technical", "direct"],
        "reject_traits": ["vague"],
        "reference": "If your agent remembers everything, it will eventually understand nothing.",
    }


def make_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.chdir(tmp_path)
    skill = tmp_path / "marketing-skills" / "skills" / "social-voice" / "SKILL.md"
    skill.parent.mkdir(parents=True, exist_ok=True)
    skill.write_text("# Social Voice\n\nBe direct.")
    write_jsonl(tmp_path / "benchmarks" / "social_voice" / "social_voice_cases.jsonl", [valid_case()])
    write_pricing(tmp_path / "config" / "openai-pricing-2026-05.json")
    return tmp_path


def test_dry_run_writes_validation_report(tmp_path, monkeypatch):
    repo = make_repo(tmp_path, monkeypatch)

    runner = BenchmarkRunner(
        skill_file="marketing-skills/skills/social-voice/SKILL.md",
        benchmark="benchmarks/social_voice/social_voice_cases.jsonl",
        output="reports/skillopt/social_voice/dry-run.md",
        dry_run=True,
        pricing_config="config/openai-pricing-2026-05.json",
    )

    result = runner.run()

    report = repo / "reports" / "skillopt" / "social_voice" / "dry-run.md"
    assert result["status"] == "ready"
    assert result["cases_loaded"] == 1
    assert report.exists()
    assert "No API calls were made" in report.read_text()


def test_protected_file_is_rejected(tmp_path, monkeypatch):
    make_repo(tmp_path, monkeypatch)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "brand-voice.md").write_text("# Brand")

    with pytest.raises(ValueError, match="protected files list"):
        BenchmarkRunner(
            skill_file="docs/brand-voice.md",
            benchmark="benchmarks/social_voice/social_voice_cases.jsonl",
            output="reports/out.md",
            dry_run=True,
        )


def test_non_skill_markdown_is_rejected(tmp_path, monkeypatch):
    make_repo(tmp_path, monkeypatch)
    bad = tmp_path / "marketing-skills" / "skills" / "social-voice" / "README.md"
    bad.write_text("# Readme")

    with pytest.raises(ValueError, match="does not match allowed patterns"):
        BenchmarkRunner(
            skill_file="marketing-skills/skills/social-voice/README.md",
            benchmark="benchmarks/social_voice/social_voice_cases.jsonl",
            output="reports/out.md",
            dry_run=True,
        )


def test_live_mode_requires_usage_output(tmp_path, monkeypatch):
    make_repo(tmp_path, monkeypatch)

    with pytest.raises(ValueError, match="Live mode requires --usage-output"):
        BenchmarkRunner(
            skill_file="marketing-skills/skills/social-voice/SKILL.md",
            benchmark="benchmarks/social_voice/social_voice_cases.jsonl",
            output="reports/out.md",
            dry_run=False,
        )


def test_baseline_only_skips_optimizer_and_writes_case_scores(tmp_path, monkeypatch):
    make_repo(tmp_path, monkeypatch)
    runner = BenchmarkRunner(
        skill_file="marketing-skills/skills/social-voice/SKILL.md",
        benchmark="benchmarks/social_voice/social_voice_cases.jsonl",
        output="reports/out.md",
        dry_run=False,
        usage_output="reports/usage.json",
        baseline_only=True,
    )
    runner._call_target = lambda skill_source, input_text, is_optimized: "A direct technical hook."
    runner._call_evaluator = lambda output, expected_traits, reject_traits, reference: {
        "score": 0.65,
        "expected_traits_met": ["technical"],
        "expected_traits_missed": ["direct"],
        "reject_traits_present": [],
        "reject_traits_avoided": ["vague"],
        "reference_alignment": 0.5,
        "reasoning": "Mixed.",
    }
    runner._call_optimizer = lambda skill_file, failures: pytest.fail("optimizer should not run")

    result = runner.run()
    usage = json.loads((tmp_path / "reports" / "usage.json").read_text())

    assert result["baseline_only"] is True
    assert usage["mode"] == "baseline-only"
    assert usage["baseline_score"] == pytest.approx(0.65)
    assert usage["optimized_score"] == pytest.approx(0.65)
    assert usage["baseline_failed_case_ids"] == ["sv-001"]
    assert usage["baseline_case_results"][0]["case_id"] == "sv-001"


def test_score_eval_weights_traits_and_reference(tmp_path, monkeypatch):
    make_repo(tmp_path, monkeypatch)
    runner = BenchmarkRunner(
        skill_file="marketing-skills/skills/social-voice/SKILL.md",
        benchmark="benchmarks/social_voice/social_voice_cases.jsonl",
        output="reports/out.md",
        dry_run=True,
    )

    scored = runner._score_eval({
        "expected_traits_met": ["technical"],
        "expected_traits_missed": ["direct"],
        "reject_traits_present": [],
        "reject_traits_avoided": ["vague"],
        "reference_alignment": 0.5,
        "reasoning": "Mixed.",
    })

    assert scored["score"] == pytest.approx(0.65)
