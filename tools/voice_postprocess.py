#!/usr/bin/env python3
"""Post-processing filter for voice-match outputs.

Strips em dashes and replaces known reject phrases with Road4AI-appropriate alternatives.
Deterministic, auditable, zero model variance.
"""
import re
import sys
from typing import Optional

# Reject phrase -> replacement mapping (case-insensitive matching)
REJECT_PHRASES = {
    "game-changer": "effective shift",
    "revolutionizing": "rethinking",
    "excited to share": "here's what happened",
    "excited to announce": "here's what happened",
    "thrilled to share": "here's what happened",
    "perfectly aligned": "mostly aligned",
    "never makes mistakes": "rarely stumbles",
    "never make mistakes": "rarely stumble",
    "never making mistakes": "rarely making errors",
    "never making errors": "rarely making mistakes",
    "amazing for productivity": "useful for throughput",
    "in today's fast-paced world": "right now",
    "in today's hyper-speed world": "right now",
    "unprecedented": "notable",
    "game changing": "effective",
    "life-changing": "useful",
    "you won't believe": "here's what happened",
    "how easy it is": "what it actually takes",
    "changing everything": "shifting the approach",
    "the same thing": "similar in purpose",
}

# Em dash patterns to replace
EM_DASH_PATTERNS = [
    (r"\u2014", " -- "),   # em dash
    (r"\u2013", " - "),    # en dash
    (r"(?<!\w)--(?!\w)", " - "),  # double hyphen (not in words)
]

# Cleanup: collapse multiple spaces/punctuation artifacts
CLEANUP_PATTERNS = [
    (r"  +", " "),           # double spaces
    (r"\s+([.,;:!?])", r"\1"),  # space before punctuation
    (r"([.,;:!?])\s*--\s*", r"\1 "),  # orphaned dash after punctuation
]


def postprocess(text: str, extra_replacements: Optional[dict] = None) -> dict:
    """Apply post-processing to voice-match output.

    Returns dict with:
        - text: cleaned output
        - em_dashes_removed: count of em dashes stripped
        - phrases_replaced: list of (original, replacement) tuples applied
    """
    replacements = dict(REJECT_PHRASES)
    if extra_replacements:
        replacements.update(extra_replacements)

    original = text
    phrases_replaced = []

    # Step 1: Replace reject phrases
    for phrase, replacement in sorted(replacements.items(), key=lambda x: -len(x[0])):
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        if pattern.search(text):
            text = pattern.sub(replacement, text)
            phrases_replaced.append((phrase, replacement))

    # Step 2: Strip em dashes
    em_dash_count = 0
    for pattern_str, replacement in EM_DASH_PATTERNS:
        count = len(re.findall(pattern_str, text))
        em_dash_count += count
        text = re.sub(pattern_str, replacement, text)

    # Step 3: Cleanup artifacts
    for pattern_str, replacement in CLEANUP_PATTERNS:
        text = re.sub(pattern_str, replacement, text)

    # Step 4: Verify em dashes are gone
    remaining = text.count("\u2014") + text.count("\u2013")
    if remaining > 0:
        em_dash_count += remaining
        text = text.replace("\u2014", " ").replace("\u2013", " ")
        text = re.sub(r"  +", " ", text)

    return {
        "text": text.strip(),
        "em_dashes_removed": em_dash_count,
        "phrases_replaced": phrases_replaced,
    }


def main():
    """CLI mode: read from stdin or file, write to stdout."""
    import argparse
    parser = argparse.ArgumentParser(description="Post-process voice-match output")
    parser.add_argument("input", nargs="?", help="Input file (default: stdin)")
    parser.add_argument("--verify", action="store_true", help="Verify no em dashes remain")
    args = parser.parse_args()

    if args.input:
        with open(args.input) as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    result = postprocess(text)

    print(result["text"])
    if result["em_dashes_removed"] > 0:
        print(f"\n[postprocess] Em dashes removed: {result['em_dashes_removed']}", file=sys.stderr)
    if result["phrases_replaced"]:
        for orig, repl in result["phrases_replaced"]:
            print(f"[postprocess] '{orig}' -> '{repl}'", file=sys.stderr)

    if args.verify:
        remaining = result["text"].count("\u2014") + result["text"].count("\u2013")
        if remaining > 0:
            print(f"[postprocess] WARNING: {remaining} em dashes still present!", file=sys.stderr)
            sys.exit(1)
        else:
            print("[postprocess] Verified: zero em dashes", file=sys.stderr)


if __name__ == "__main__":
    main()
