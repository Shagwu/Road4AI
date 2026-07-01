#!/usr/bin/env python3
"""Deterministic evaluator for voice-match benchmark.

Rule-based scoring with zero LLM variance. Checks:
1. Em dash count (must be 0)
2. Reject traits present (must be 0)
3. Expected traits detected (pattern matching)
4. Sentence punchiness (short sentences score higher)

Returns consistent scores across runs.
"""
import json
import re
import sys
from pathlib import Path
from typing import Optional


# Reject phrases to check for (case-insensitive)
REJECT_PHRASES = [
    "game-changer", "revolutionizing", "excited to share", "excited to announce",
    "thrilled to share", "perfectly aligned", "never makes mistakes",
    "never make mistakes", "amazing for productivity", "in today's fast-paced world",
    "unprecedented", "game changing", "life-changing", "you won't believe",
    "how easy it is", "changing everything", "the same thing", "trick",
    "simple guide", "make your agents smarter", "with you all today",
    "journey", "thrilled", "revolutionary",
]

# Em dash patterns
EM_DASH_PATTERNS = [
    r"\u2014",  # em dash
    r"\u2013",  # en dash
    r"(?<!\w)--(?!\w)",  # double hyphen
]

# Expected trait patterns (simplified matching)
TRAIT_PATTERNS = {
    "No em dashes": lambda text: not any(re.search(p, text) for p in EM_DASH_PATTERNS),
    "Punchy": lambda text: _check_punchy(text),
    "Conspiratorial": lambda text: _check_conspiratorial(text),
    "Opinionated": lambda text: _check_opinionated(text),
    "Senior Persona": lambda text: _check_senior_persona(text),
    "Technical focus": lambda text: _check_technical_focus(text),
    "High signal-to-noise": lambda text: _check_signal_noise(text),
    "Zero-cost engineering": lambda text: _check_zero_cost(text),
    "Transparent": lambda text: _check_transparent(text),
    "Technical integrity": lambda text: _check_technical_integrity(text),
    "No hype": lambda text: _check_no_hype(text),
    "Transparency": lambda text: _check_transparent(text),
    "Humble": lambda text: _check_humble(text),
    "Manual friction focus": lambda text: _check_manual_friction(text),
    "Direct": lambda text: _check_direct(text),
    "No pleasantries": lambda text: _check_no_pleasantries(text),
    "No marketing fluff": lambda text: _check_no_marketing_fluff(text),
    "Tutorial format": lambda text: _check_tutorial_format(text),
    "Practical": lambda text: _check_practical(text),
    "Specific claim": lambda text: _check_specific_claim(text),
}


def _count_em_dashes(text: str) -> int:
    count = 0
    for pattern in EM_DASH_PATTERNS:
        count += len(re.findall(pattern, text))
    return count


def _find_reject_traits(text: str) -> list:
    found = []
    text_lower = text.lower()
    for phrase in REJECT_PHRASES:
        if phrase.lower() in text_lower:
            found.append(phrase)
    return found


def _avg_sentence_length(text: str) -> float:
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 0
    lengths = [len(s.split()) for s in sentences]
    return sum(lengths) / len(lengths)


def _check_punchy(text: str) -> bool:
    avg_len = _avg_sentence_length(text)
    return avg_len < 20


def _check_conspiratorial(text: str) -> bool:
    conspiratorial_phrases = [
        "here is what", "here's what", "nobody tells", "wish i knew",
        "the trap is", "to be honest", "did you know", "can you believe",
        "let me tell you", "the secret", "insider", "between us",
    ]
    text_lower = text.lower()
    return any(p in text_lower for p in conspiratorial_phrases)


def _check_opinionated(text: str) -> bool:
    opinion_markers = ["i think", "i believe", "in my experience", "what i've found",
                       "the reality is", "the truth is", "here's the thing"]
    text_lower = text.lower()
    return any(p in text_lower for p in opinion_markers)


def _check_senior_persona(text: str) -> bool:
    senior_markers = ["years of", "been doing", "learned the hard way",
                      "what nobody tells", "principal engineer", "tech lead",
                      "in the trenches", "seen this before"]
    text_lower = text.lower()
    return any(p in text_lower for p in senior_markers)


def _check_technical_focus(text: str) -> bool:
    technical_terms = ["hnsw", "rag", "prompt injection", "cold/warm",
                       "latency", "tokens", "embeddings", "vector",
                       "agent", "swarm", "orchestration"]
    text_lower = text.lower()
    return any(t in text_lower for t in technical_terms)


def _check_signal_noise(text: str) -> bool:
    signal_markers = ["signal", "noise", "focused", "essential", "core"]
    text_lower = text.lower()
    return any(m in text_lower for m in signal_markers)


def _check_zero_cost(text: str) -> bool:
    zero_cost_markers = ["zero-cost", "free", "local", "no api", "without paying",
                         "no cost", "zero cost", "ollama"]
    text_lower = text.lower()
    return any(m in text_lower for m in zero_cost_markers)


def _check_transparent(text: str) -> bool:
    transparent_markers = ["honestly", "transparent", "admit", "limitation",
                           "trade-off", "tradeoff", "caveat", "warning"]
    text_lower = text.lower()
    return any(m in text_lower for m in transparent_markers)


def _check_technical_integrity(text: str) -> bool:
    integrity_markers = ["accuracy", "correct", "precise", "factual",
                         "technical", "specific", "measured"]
    text_lower = text.lower()
    return any(m in text_lower for m in integrity_markers)


def _check_no_hype(text: str) -> bool:
    hype_words = ["amazing", "incredible", "revolutionary", "game-changing",
                  "best", "perfect", "flawless", "exceptional"]
    text_lower = text.lower()
    return not any(h in text_lower for h in hype_words)


def _check_humble(text: str) -> bool:
    humble_markers = ["limitation", "challenge", "struggle", "difficult",
                      "not easy", "hard part", "what i learned"]
    text_lower = text.lower()
    return any(m in text_lower for m in humble_markers)


def _check_manual_friction(text: str) -> bool:
    friction_markers = ["manual", "friction", "human review", "human in the loop",
                        "human oversight", "double-check", "verify"]
    text_lower = text.lower()
    return any(m in text_lower for m in friction_markers)


def _check_direct(text: str) -> bool:
    avg_len = _avg_sentence_length(text)
    return avg_len < 25


def _check_no_pleasantries(text: str) -> bool:
    pleasantries = ["hello", "welcome", "thank you for reading", "i hope",
                    "dear", "greetings"]
    text_lower = text.lower()
    return not any(p in text_lower for p in pleasantries)


def _check_no_marketing_fluff(text: str) -> bool:
    fluff = ["leverage", "utilize", "synergy", "paradigm", "ecosystem",
              "holistic", "seamless", "cutting-edge"]
    text_lower = text.lower()
    return not any(f in text_lower for f in fluff)


def _check_tutorial_format(text: str) -> bool:
    tutorial_markers = ["step", "how to", "guide", "protocol", "here's how",
                        "first", "second", "third", "1.", "2.", "3."]
    text_lower = text.lower()
    return any(m in text_lower for m in tutorial_markers)


def _check_practical(text: str) -> bool:
    practical_markers = ["use", "apply", "implement", "try", "example",
                         "in practice", "actually"]
    text_lower = text.lower()
    return any(m in text_lower for m in practical_markers)


def _check_specific_claim(text: str) -> bool:
    specific_markers = ["saved", "reduced", "improved", "increased",
                        "from x to y", "in my case", "what worked"]
    text_lower = text.lower()
    return any(m in text_lower for m in specific_markers)


def evaluate_output(output: str, expected_traits: list, reject_traits: list) -> dict:
    """Deterministic evaluation of voice-match output.

    Returns dict with:
        - score: 0.0 to 1.0
        - em_dash_count: number of em dashes found
        - reject_traits_present: list of reject traits found
        - traits_detected: list of expected traits detected
        - traits_missed: list of expected traits not detected
        - reasoning: human-readable explanation
    """
    em_dash_count = _count_em_dashes(output)
    reject_found = _find_reject_traits(output)

    # Score components
    em_dash_score = 1.0 if em_dash_count == 0 else max(0, 1.0 - (em_dash_count * 0.2))
    reject_score = 1.0 if len(reject_found) == 0 else max(0, 1.0 - (len(reject_found) * 0.15))

    # Trait detection
    traits_detected = []
    traits_missed = []
    for trait in expected_traits:
        if trait in TRAIT_PATTERNS:
            if TRAIT_PATTERNS[trait](output):
                traits_detected.append(trait)
            else:
                traits_missed.append(trait)
        else:
            traits_detected.append(trait)

    trait_score = len(traits_detected) / len(expected_traits) if expected_traits else 1.0

    # Combined score
    score = (em_dash_score * 0.3) + (reject_score * 0.3) + (trait_score * 0.4)

    reasoning_parts = []
    if em_dash_count > 0:
        reasoning_parts.append(f"Found {em_dash_count} em dashes")
    if reject_found:
        reasoning_parts.append(f"Reject traits present: {', '.join(reject_found)}")
    if traits_missed:
        reasoning_parts.append(f"Missing traits: {', '.join(traits_missed)}")
    if not reasoning_parts:
        reasoning_parts.append("All checks passed")

    return {
        "score": round(score, 3),
        "em_dash_count": em_dash_count,
        "reject_traits_present": reject_found,
        "traits_detected": traits_detected,
        "traits_missed": traits_missed,
        "reasoning": "; ".join(reasoning_parts),
    }


def main():
    """CLI mode: evaluate output against expected traits."""
    import argparse
    parser = argparse.ArgumentParser(description="Deterministic voice-match evaluator")
    parser.add_argument("output", help="Output text to evaluate")
    parser.add_argument("--expected-traits", required=True, help="JSON list of expected traits")
    parser.add_argument("--reject-traits", required=True, help="JSON list of reject traits")
    args = parser.parse_args()

    output = Path(args.output).read_text() if Path(args.output).exists() else args.output
    expected_traits = json.loads(args.expected_traits)
    reject_traits = json.loads(args.reject_traits)

    result = evaluate_output(output, expected_traits, reject_traits)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
