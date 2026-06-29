#!/usr/bin/env python3
"""
Harvester → Drift Monitor hook.
Receives signals from Agent-Reach harvester, routes through drift monitoring.

Usage:
    # Process a harvester signal
    python tools/harvester_drift_hook.py --signal '{"source":"twitter","topic":"SkillOpt","confidence":0.85}'

    # Check if harvester is allowed to run (pause/resume gate)
    python tools/harvester_drift_hook.py --gate-check

    # Pause harvesting (blue halt)
    python tools/harvester_drift_hook.py --pause "drift halt on social_voice"

    # Resume harvesting (after investigation)
    python tools/harvester_drift_hook.py --resume "root cause resolved"
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drift_monitor import DriftMonitor, DRIFT_LOG, DRIFT_HALT

HARVESTER_STATE = Path("state/harvester_gate.json")


def load_gate() -> dict:
    """Load harvester gate state."""
    if HARVESTER_STATE.exists():
        return json.loads(HARVESTER_STATE.read_text())
    return {
        "status": "open",
        "paused_at": None,
        "pause_reason": None,
        "resumed_at": None,
        "resume_reason": None,
        "signals_processed": 0,
        "signals_blocked": 0
    }


def save_gate(state: dict) -> None:
    """Save harvester gate state."""
    HARVESTER_STATE.parent.mkdir(parents=True, exist_ok=True)
    HARVESTER_STATE.write_text(json.dumps(state, indent=2) + "\n")


def gate_check() -> dict:
    """Check if harvester is allowed to run."""
    state = load_gate()

    # Check if there are recent blue halts NOT overridden by a resume
    recent_blue = False
    if DRIFT_HALT.exists():
        lines = DRIFT_HALT.read_text().splitlines()
        if lines:
            last_halt = json.loads(lines[-1])
            if last_halt.get("approved_to_continue") is False:
                # Check if gate was resumed after this halt
                halted_at = last_halt.get("timestamp", "")
                resumed_at = state.get("resumed_at", "")
                if resumed_at and resumed_at > halted_at:
                    recent_blue = False  # Resume overrides old halt
                else:
                    recent_blue = True

    allowed = state["status"] == "open" and not recent_blue

    result = {
        "allowed": allowed,
        "gate_status": state["status"],
        "recent_blue_halt": recent_blue,
        "signals_processed": state["signals_processed"],
        "signals_blocked": state["signals_blocked"]
    }

    if not allowed:
        result["reason"] = state.get("pause_reason", "Recent blue halt not resolved")

    return result


def process_signal(signal_data: dict) -> dict:
    """Process a harvester signal through confidence tiering."""
    gate = gate_check()

    if not gate["allowed"]:
        # Block signal
        state = load_gate()
        state["signals_blocked"] += 1
        save_gate(state)

        return {
            "action": "blocked",
            "reason": gate["reason"],
            "signal": signal_data
        }

    # Signal allowed — route by confidence tier
    domain = signal_data.get("domain", "social_voice")
    confidence = signal_data.get("confidence", 0.5)

    # Determine confidence tier
    if confidence >= 0.8:
        tier = "green"
        action = "auto-store"
    elif confidence >= 0.5:
        tier = "yellow"
        action = "queue-for-review"
    else:
        tier = "blue"
        action = "discard"

    # Update gate state
    state = load_gate()
    state["signals_processed"] += 1
    save_gate(state)

    return {
        "action": action,
        "domain": domain,
        "confidence": confidence,
        "tier": tier,
        "signal": signal_data
    }


def pause_harvesting(reason: str) -> dict:
    """Pause harvesting due to drift halt."""
    state = load_gate()
    state["status"] = "paused"
    state["paused_at"] = datetime.now(timezone.utc).isoformat()
    state["pause_reason"] = reason
    save_gate(state)

    return {"status": "paused", "reason": reason}


def resume_harvesting(reason: str) -> dict:
    """Resume harvesting after investigation."""
    state = load_gate()
    state["status"] = "open"
    state["resumed_at"] = datetime.now(timezone.utc).isoformat()
    state["resume_reason"] = reason
    save_gate(state)

    return {"status": "open", "reason": reason}


def main() -> int:
    parser = argparse.ArgumentParser(description="Harvester → Drift Monitor hook")
    parser.add_argument("--signal", help="JSON signal data to process")
    parser.add_argument("--gate-check", action="store_true", help="Check if harvesting is allowed")
    parser.add_argument("--pause", help="Pause harvesting with reason")
    parser.add_argument("--resume", help="Resume harvesting with reason")
    args = parser.parse_args()

    if args.gate_check:
        result = gate_check()
        print(json.dumps(result, indent=2))
        return 0 if result["allowed"] else 1

    if args.pause:
        result = pause_harvesting(args.pause)
        print(json.dumps(result, indent=2))
        return 0

    if args.resume:
        result = resume_harvesting(args.resume)
        print(json.dumps(result, indent=2))
        return 0

    if args.signal:
        signal_data = json.loads(args.signal)
        result = process_signal(signal_data)
        print(json.dumps(result, indent=2))
        return 0 if result["action"] != "blocked" else 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
