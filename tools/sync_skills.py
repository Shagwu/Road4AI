#!/usr/bin/env python3
import argparse
import filecmp
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


MANIFEST_PATH = Path("skills/manifest.json")


@dataclass(frozen=True)
class SyncItem:
    name: str
    source: Path
    target: Path


def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    with path.open() as handle:
        return json.load(handle)


def protected_runtime_locations(manifest: dict) -> set[Path]:
    protected: set[Path] = set()
    for section in ("vendor_tool_skills", "marketing_generic_pack", "runtime_road4ai"):
        for item in manifest.get(section, {}).values():
            location = item.get("location")
            if location:
                protected.add(Path(location))
    return protected


def build_sync_items(manifest: dict) -> list[SyncItem]:
    protected = protected_runtime_locations(manifest)
    items: list[SyncItem] = []

    for name, item in manifest.get("canonical_skills", {}).items():
        source = Path(item["source"])
        targets = item.get("runtime_targets", [])
        if not targets:
            continue
        if not source.exists():
            raise FileNotFoundError(f"{name}: source does not exist: {source}")
        if not (source / "SKILL.md").exists():
            raise FileNotFoundError(f"{name}: missing SKILL.md in {source}")

        for target_root in targets:
            target = Path(target_root) / name
            if target in protected and target != source:
                raise ValueError(f"{name}: target would overwrite protected runtime skill: {target}")
            items.append(SyncItem(name=name, source=source, target=target))

    return items


def dirs_equal(left: Path, right: Path) -> bool:
    if not right.exists():
        return False
    comparison = filecmp.dircmp(left, right)
    if comparison.left_only or comparison.right_only or comparison.diff_files or comparison.funny_files:
        return False
    return all(dirs_equal(Path(comparison.left) / subdir, Path(comparison.right) / subdir) for subdir in comparison.common_dirs)


def sync_item(item: SyncItem) -> str:
    if item.target.exists():
        shutil.rmtree(item.target)
    item.target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(item.source, item.target)
    return f"SYNCED {item.name}: {item.source} -> {item.target}"


def check_items(items: list[SyncItem]) -> tuple[list[str], list[str]]:
    ok: list[str] = []
    drift: list[str] = []
    for item in items:
        if dirs_equal(item.source, item.target):
            ok.append(f"OK {item.name}: {item.target}")
        else:
            drift.append(f"DRIFT {item.name}: {item.source} -> {item.target}")
    return ok, drift


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync canonical Road4AI skills into runtime skill locations.")
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--check", action="store_true", help="Report drift without changing files.")
    parser.add_argument("--sync", action="store_true", help="Install canonical skills into runtime targets.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable output.")
    args = parser.parse_args()

    if args.check == args.sync:
        parser.error("choose exactly one of --check or --sync")

    manifest = load_manifest(args.manifest)
    items = build_sync_items(manifest)

    if args.check:
        ok, drift = check_items(items)
        result = {"status": "PASS" if not drift else "DRIFT", "ok": ok, "drift": drift}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            for line in ok + drift:
                print(line)
        return 1 if drift else 0

    synced = [sync_item(item) for item in items]
    ok, drift = check_items(items)
    result = {"status": "SYNCED" if not drift else "DRIFT_AFTER_SYNC", "synced": synced, "ok": ok, "drift": drift}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for line in synced:
            print(line)
        for line in drift:
            print(line)
    return 1 if drift else 0


if __name__ == "__main__":
    raise SystemExit(main())

