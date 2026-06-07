import importlib.util
import json
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "record_stability_run.py"
SPEC = importlib.util.spec_from_file_location("record_stability_run", MODULE_PATH)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data) + "\n")


def stability_seed() -> dict:
    return {
        "status": "pending",
        "purpose": "test",
        "skill_path": ".agents/skills/voice-match/SKILL.md",
        "benchmark_path": "benchmarks/social_voice/social_voice_cases.jsonl",
        "case_count": 12,
        "runner": "tools/run_skillopt_benchmark.py",
        "runner_engine": "gemini-cli",
        "executor_allowed": ["codex", "gemini"],
        "pass_criteria": {
            "mean_score_variance_pct_max": 5,
            "failed_case_overlap_pct_min": 80,
            "standard_deviation_must_be_stable": True,
        },
        "runs": [],
    }


def usage_report() -> dict:
    return {
        "mode": "baseline-only",
        "cases": 12,
        "calls": {"target_model": 12, "evaluator_model": 12, "optimizer_model": 0},
        "baseline_score": 0.72,
        "baseline_score_stddev": 0.08,
        "baseline_failed_case_ids": ["V-001", "V-003"],
    }


def test_append_run_records_baseline_usage(tmp_path, monkeypatch):
    stability = tmp_path / "stability-runs.json"
    usage = tmp_path / "usage.json"
    write_json(stability, stability_seed())
    write_json(usage, usage_report())
    monkeypatch.setattr(module, "git_commit", lambda: "abc1234")
    monkeypatch.setattr(module, "gemini_version", lambda: "gemini-test")

    args = type("Args", (), {
        "run_label": "run_1",
        "executor": "codex",
        "command": "python3 tools/run_skillopt_benchmark.py --baseline-only",
        "environment_notes": "test env",
        "gemini_version": "",
        "usage_report": usage,
    })()

    entry = module.build_run_entry(args, module.read_json(usage))
    result = module.append_run(stability, entry)

    assert result["status"] == "in_progress"
    assert result["runs"][0]["run_label"] == "run_1"
    assert result["runs"][0]["git_commit"] == "abc1234"
    assert result["runs"][0]["baseline_failed_case_ids"] == ["V-001", "V-003"]


def test_second_run_marks_ready_for_review(tmp_path, monkeypatch):
    stability = tmp_path / "stability-runs.json"
    usage = tmp_path / "usage.json"
    write_json(stability, stability_seed())
    write_json(usage, usage_report())
    monkeypatch.setattr(module, "git_commit", lambda: "abc1234")
    monkeypatch.setattr(module, "gemini_version", lambda: "gemini-test")

    for label in ["run_1", "run_2"]:
        args = type("Args", (), {
            "run_label": label,
            "executor": "gemini",
            "command": "same command",
            "environment_notes": "",
            "gemini_version": "gemini-test",
            "usage_report": usage,
        })()
        module.append_run(stability, module.build_run_entry(args, module.read_json(usage)))

    result = module.read_json(stability)
    assert result["status"] == "ready_for_review"
    assert [run["run_label"] for run in result["runs"]] == ["run_1", "run_2"]
