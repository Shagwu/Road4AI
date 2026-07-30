"""
mimo_provider.py

Wrapper for talking to a raw llama-server instance serving MiMo-7B-RL-Q4_K_M
(no embedded chat template in the GGUF, so we handle ChatML formatting,
stop sequences, and <think> stripping here instead of via --chat-template).

Drop this into your Road4AI provider layer and call `mimo_chat()` wherever
you currently call MiMo directly (harvester_pipeline.py, Karen, MiMo Auto, etc).
"""

import json
import re
import requests
from dataclasses import dataclass
from typing import Optional


# --- Config -----------------------------------------------------------------

MIMO_ENDPOINT = "http://localhost:8000/completion"  # adjust port to your llama-server launch
MAX_TOKENS_DEFAULT = 1024
TEMPERATURE_DEFAULT = 0.2

# ChatML turn delimiters
IM_START = "<|im_start|>"
IM_END = "<|im_end|>"

# Stop sequences: turn-end token + safety nets against runaway generation
STOP_SEQUENCES = [
    IM_END,
    f"{IM_START}user",       # in case model starts hallucinating the next turn
    f"{IM_START}system",
]

THINK_BLOCK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
# In case a think block is opened but never closed (runaway generation cut off by max_tokens)
UNCLOSED_THINK_RE = re.compile(r"<think>.*$", re.DOTALL | re.IGNORECASE)

# Matches ```json ... ``` or plain ``` ... ``` fences (MiMo wraps structured
# output in markdown fences even when asked for raw JSON)
JSON_FENCE_RE = re.compile(r"^```(?:json)?\s*\n(.*?)\n?```$", re.DOTALL | re.IGNORECASE)


@dataclass
class MimoResponse:
    text: str            # cleaned, final answer text
    raw: str              # raw completion exactly as returned by llama-server
    had_think_block: bool
    truncated: bool       # True if we suspect max_tokens cut off before natural stop


# --- Prompt formatting --------------------------------------------------------

def format_chatml(system: Optional[str], user_prompt: str) -> str:
    """Build a ChatML-formatted prompt for /completion."""
    parts = []
    if system:
        parts.append(f"{IM_START}system\n{system}{IM_END}\n")
    parts.append(f"{IM_START}user\n{user_prompt}{IM_END}\n")
    parts.append(f"{IM_START}assistant\n")
    return "".join(parts)


# --- Response cleaning --------------------------------------------------------

def strip_think(raw_text: str) -> tuple[str, bool]:
    """Remove <think>...</think> reasoning blocks. Returns (cleaned_text, had_think_block)."""
    had_think = bool(THINK_BLOCK_RE.search(raw_text)) or bool(UNCLOSED_THINK_RE.search(raw_text))

    cleaned = THINK_BLOCK_RE.sub("", raw_text)
    cleaned = UNCLOSED_THINK_RE.sub("", cleaned)  # catch truncated/unclosed think blocks

    # Strip any leftover ChatML delimiters that leaked into the output
    cleaned = cleaned.replace(IM_START, "").replace(IM_END, "")
    cleaned = cleaned.strip()

    return cleaned, had_think


def strip_json_fence(text: str) -> str:
    """Strip a leading/trailing markdown code fence (```json ... ``` or ``` ... ```)
    if present. MiMo tends to wrap structured output in fences even when the
    prompt asks for raw JSON with no formatting. Safe no-op if no fence found."""
    text = text.strip()
    match = JSON_FENCE_RE.match(text)
    if match:
        return match.group(1).strip()
    return text


def looks_truncated(raw_text: str, tokens_used: Optional[int], max_tokens: int) -> bool:
    """Heuristic: if we hit the token ceiling AND there's an unclosed think block
    or no natural stop sequence in sight, flag it as likely truncated garbage
    rather than a clean completion."""
    hit_ceiling = tokens_used is not None and tokens_used >= max_tokens
    unclosed = bool(UNCLOSED_THINK_RE.search(raw_text)) and not THINK_BLOCK_RE.search(raw_text)
    return hit_ceiling or unclosed


# --- Main entrypoint -----------------------------------------------------------

def mimo_chat(
    user_prompt: str,
    system: Optional[str] = None,
    max_tokens: int = MAX_TOKENS_DEFAULT,
    temperature: float = TEMPERATURE_DEFAULT,
    endpoint: str = MIMO_ENDPOINT,
    timeout_s: int = 120,
) -> MimoResponse:
    """
    Send a ChatML-formatted request to MiMo via llama-server /completion,
    strip reasoning blocks, and return a clean result.

    Raises requests.RequestException on network/timeout failure -- catch this
    at the call site (e.g. Karen review, harvester pipeline) and treat it as
    a hard failure, not a silent pass.
    """
    prompt = format_chatml(system, user_prompt)

    payload = {
        "prompt": prompt,
        "n_predict": max_tokens,
        "temperature": temperature,
        "stop": STOP_SEQUENCES,
    }

    resp = requests.post(endpoint, json=payload, timeout=timeout_s)
    resp.raise_for_status()
    data = resp.json()

    raw_text = data.get("content", "")
    tokens_used = data.get("tokens_predicted")

    cleaned, had_think = strip_think(raw_text)
    truncated = looks_truncated(raw_text, tokens_used, max_tokens)

    return MimoResponse(
        text=cleaned,
        raw=raw_text,
        had_think_block=had_think,
        truncated=truncated,
    )


def mimo_json_chat(
    user_prompt: str,
    system: Optional[str] = None,
    max_tokens: int = MAX_TOKENS_DEFAULT,
    temperature: float = TEMPERATURE_DEFAULT,
    endpoint: str = MIMO_ENDPOINT,
    timeout_s: int = 120,
) -> dict:
    """
    Same as mimo_chat(), but strips markdown JSON fences and parses the result.

    Raises json.JSONDecodeError if MiMo didn't return valid JSON -- callers
    (e.g. Karen, harvester_pipeline.py) should catch this explicitly and
    treat it as a hard failure / retry, not swallow it. Don't silently fall
    back to an empty dict here; that would hide real formatting regressions.
    """
    result = mimo_chat(
        user_prompt,
        system=system,
        max_tokens=max_tokens,
        temperature=temperature,
        endpoint=endpoint,
        timeout_s=timeout_s,
    )
    fenced_stripped = strip_json_fence(result.text)
    return json.loads(fenced_stripped)  # raises JSONDecodeError on malformed output


# --- Quick manual test ----------------------------------------------------------

if __name__ == "__main__":
    result = mimo_chat("Say only the word 'test'. Nothing else.")
    print("=== CLEANED ===")
    print(result.text)
    print("\n=== HAD THINK BLOCK ===", result.had_think_block)
    print("=== TRUNCATED ===", result.truncated)
    if result.truncated or len(result.text) > 200:
        print("\n=== RAW (for debugging) ===")
        print(result.raw)

    print("\n\n=== JSON TEST ===")
    json_result = mimo_chat("Return valid JSON with keys title and summary.")

    print("raw output:")
    print(json_result.raw)

    fenced_stripped = strip_json_fence(json_result.text)

    print("cleaned after fence strip:")
    print(fenced_stripped)

try:
    parsed = json.loads(fenced_stripped)
    print("parsed json:")
    print(parsed)
    print("type:", type(parsed))
except json.JSONDecodeError as e:
    print("JSON PARSE FAILED")
    print("error:", e)  