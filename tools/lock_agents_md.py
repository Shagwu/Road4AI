#!/usr/bin/env python3
"""Toggle filesystem protection on AGENTS.md.

Usage:
  python tools/lock_agents_md.py --status    # Show current lock state
  python tools/lock_agents_md.py --lock      # Make read-only (chmod 444)
  python tools/lock_agents_md.py --unlock    # Make writable (chmod 644)
  python tools/lock_agents_md.py --guard     # Lock if currently writable (no-op if already locked)

The --guard mode is designed for pre-commit hooks and hermes checkpoints.
It only locks; it never unlocks. Safe to run repeatedly.
"""

import argparse
import os
import stat
import sys
from pathlib import Path

AGENTS_MD = Path(__file__).resolve().parent.parent / "AGENTS.md"


def get_mode():
    return oct(AGENTS_MD.stat().st_mode)[-3:]


def is_writable():
    return os.access(AGENTS_MD, os.W_OK)


def lock():
    os.chmod(AGENTS_MD, 0o444)
    print(f"Locked AGENTS.md ({get_mode()})")


def unlock():
    os.chmod(AGENTS_MD, 0o644)
    print(f"Unlocked AGENTS.md ({get_mode()})")


def status():
    mode = get_mode()
    writable = is_writable()
    state = "UNLOCKED (writable)" if writable else "LOCKED (read-only)"
    print(f"AGENTS.md: {state} [{mode}]")
    print(f"Path: {AGENTS_MD}")


def guard():
    if is_writable():
        lock()
    else:
        print(f"AGENTS.md already locked [{get_mode()}]")


def main():
    parser = argparse.ArgumentParser(description="Toggle filesystem protection on AGENTS.md")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--status", action="store_true", help="Show current lock state")
    group.add_argument("--lock", action="store_true", help="Make read-only (chmod 444)")
    group.add_argument("--unlock", action="store_true", help="Make writable (chmod 644)")
    group.add_argument("--guard", action="store_true", help="Lock if writable (safe for hooks)")
    args = parser.parse_args()

    if not AGENTS_MD.exists():
        print(f"Error: {AGENTS_MD} not found", file=sys.stderr)
        sys.exit(1)

    if args.status:
        status()
    elif args.lock:
        lock()
    elif args.unlock:
        unlock()
    elif args.guard:
        guard()


if __name__ == "__main__":
    main()
