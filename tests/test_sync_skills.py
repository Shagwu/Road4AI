import importlib.util
import json
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "sync_skills.py"
SPEC = importlib.util.spec_from_file_location("sync_skills", MODULE_PATH)
sync_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync_skills)


def write_skill(path: Path, body: str = "# Skill\n") -> None:
    path.mkdir(parents=True)
    (path / "SKILL.md").write_text(body)


def manifest(tmp_path: Path) -> dict:
    return {
        "canonical_skills": {
            "content-pipeline": {
                "source": str(tmp_path / "skills" / "content-pipeline"),
                "runtime_targets": [str(tmp_path / ".agents" / "skills")],
            }
        },
        "vendor_tool_skills": {
            "vendor-skill": {
                "location": str(tmp_path / ".agents" / "skills" / "vendor-skill")
            }
        },
        "marketing_generic_pack": {},
        "runtime_road4ai": {},
    }


def test_check_reports_drift_when_target_missing(tmp_path):
    write_skill(tmp_path / "skills" / "content-pipeline")
    items = sync_skills.build_sync_items(manifest(tmp_path))

    _, drift = sync_skills.check_items(items)

    assert drift
    assert "content-pipeline" in drift[0]


def test_sync_copies_canonical_skill(tmp_path):
    write_skill(tmp_path / "skills" / "content-pipeline", "# Canonical\n")
    items = sync_skills.build_sync_items(manifest(tmp_path))

    sync_skills.sync_item(items[0])

    target = tmp_path / ".agents" / "skills" / "content-pipeline" / "SKILL.md"
    assert target.read_text() == "# Canonical\n"
    ok, drift = sync_skills.check_items(items)
    assert ok
    assert not drift


def test_refuses_to_overwrite_vendor_skill(tmp_path):
    write_skill(tmp_path / "skills" / "vendor-skill")
    data = {
        "canonical_skills": {
            "vendor-skill": {
                "source": str(tmp_path / "skills" / "vendor-skill"),
                "runtime_targets": [str(tmp_path / ".agents" / "skills")],
            }
        },
        "vendor_tool_skills": {
            "vendor-skill": {
                "location": str(tmp_path / ".agents" / "skills" / "vendor-skill")
            }
        },
    }

    with pytest.raises(ValueError, match="protected runtime skill"):
        sync_skills.build_sync_items(data)

