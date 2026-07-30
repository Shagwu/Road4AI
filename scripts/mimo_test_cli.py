#!/usr/bin/env python3
"""
Small CLI to exercise MiMo via mimo_provider.mimo_chat().

Usage:
    python scripts/mimo_test_cli.py "Say only the word 'test'."
"""

import sys

from mimo_provider import mimo_chat


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print("Usage: python scripts/mimo_test_cli.py <prompt>")
        return 1

    prompt = " ".join(argv)

    result = mimo_chat(prompt, system=None)

    print("=== CLEANED TEXT ===")
    print(result.text)
    print("\n=== FLAGS ===")
    print("had_think_block:", result.had_think_block)
    print("truncated:", result.truncated)

    if result.truncated or len(result.text) > 400:
        print("\n=== RAW OUTPUT (debug) ===")
        print(result.raw)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())