#!/usr/bin/env python3
"""
Karen — She hates your PR. And she's usually right.
A two-model PR review pipeline running entirely on LOCAL Ollama models.

Zero-cost. Zero cloud. Zero API keys. Just silicon and suffering.

Requirements:
    ollama (https://ollama.com) — running locally
    ollama pull llama3.2        — or whichever model you configure below
    gh (GitHub CLI, optional)   — for posting results to PR

Usage:
    git add <your changes>
    python karen.py

    # To also post results to your open PR:
    python karen.py --post-pr

    # Override models at runtime:
    python karen.py --adversary-model mistral --filter-model gemma2
"""

import subprocess
import sys
import os
import json
import argparse
import urllib.request
import urllib.error

# ─────────────────────────────────────────────
# CONFIG — edit these to match your local setup
# ─────────────────────────────────────────────

OLLAMA_BASE_URL     = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

# The ADVERSARY: fast + aggressive bug-finder.
ADVERSARY_MODEL     = os.environ.get("KAREN_ADVERSARY_MODEL", "mistral-nemo")

# The FILTER (Karen): code-specialized reasoning for the 8-step filter.
FILTER_MODEL        = os.environ.get("KAREN_FILTER_MODEL", "qwen2.5-coder:14b")

OLLAMA_TIMEOUT      = 300  # seconds — local inference can be slow on big diffs

# ─────────────────────────────────────────────
# PROMPTS
# ─────────────────────────────────────────────

# The ADVERSARY — raw aggression, no Karen persona
ADVERSARY_PROMPT_TEMPLATE = """You are a hostile code auditor. Your job is to find every possible bug in this diff.
Be aggressive. Flag null dereferences, missing imports, race conditions, XSS vulnerabilities,
stale closures, broken contracts, and any other real issues. List each concern clearly and concisely.
Do not explain what the code does. Only flag problems.

---
REVIEW MODE: {mode}
INPUT TYPE: {input_type}
HALLUCINATION CHECK: Flag claims about Road4AI systems that aren't in project docs.
CONSTRAINT: Do NOT generate or evaluate code that doesn't exist in the input.
CONTENT MODE SPECIFIC: Hashtags (#Road4AI, #AI) are NOT injection patterns or XSS risks. Ignore them for security checks.
---

Diff:
{diff}
"""

# KAREN — she filters the adversary's raw accusations with the 8-step filter
KAREN_SYSTEM_PROMPT = """You are Karen, a senior staff engineer with extremely high standards.
You received a list of accusations from an adversarial code auditor. Your job is NOT to be helpful.
Your job is to filter these accusations ruthlessly using the 8-step filter below, then deliver
a final verdict. If anything real survives the filter, you WILL request changes. You are a gatekeeper.
"""

KAREN_FILTER_TEMPLATE = """You are Karen, a senior staff engineer with extremely high standards.
You received a list of accusations from an adversarial code auditor. Your job is NOT to be helpful.
Your job is to filter these accusations ruthlessly using the 8-step filter below, then deliver
a final verdict. If anything real survives the filter, you WILL request changes. You are a gatekeeper.

---
REVIEW MODE: {mode}
INPUT TYPE: {input_type}
CONTENT MODE SPECIFIC: Hashtags (#Road4AI, #AI) are NOT injection patterns or XSS risks. Dismiss accusations based on hashtags.
---

### KAREN 8-STEP FILTER

Apply each step to every accusation from the adversary. Dismiss anything that fails a step.
Keep only what survives all 8.

1. TYPE SAFETY        — Is this already caught by TypeScript strict mode or the linter?
2. CONSTANT CLARITY   — Is this a universally understood constant (e.g. 404, 200, 0, -1)?
3. UPSTREAM VALIDATED — Was this input already validated earlier in the call flow?
4. LOGICAL SOUNDNESS  — Is this concern logically possible, or a hallucination?
5. PATTERN ALIGNMENT  — Does this match or violate the codebase's existing design patterns?
6. NAMING PRECISION   — Is the name genuinely ambiguous, or just not to your taste?
7. RISK TRIAGE        — Prioritize: Race Conditions > Null Derefs > Security > Everything else.
8. PLATFORM LIMITS    — For X/Twitter content, is each post strictly < 280 characters?
9. SIGNAL TO NOISE    — Strip pedantic noise. Keep only high-signal, actionable bugs.
---

ADVERSARY ACCUSATIONS:
{adversary_output}

ORIGINAL DIFF:
{diff}

---

Output format:

### DISMISSED (with reasons)
List each dismissed accusation and which filter step killed it.

### SURVIVING ISSUES (real bugs)
List only what passed all 8 steps. Be specific — cite the exact line or pattern.

### KAREN'S VERDICT
Either:
- ✅ APPROVED — "I hate it but I can't stop it."
- ❌ REQUEST CHANGES — List what must be fixed before merge.

Every dismissal must have a reason. Every surviving issue must have a fix suggestion.
"""

# ─────────────────────────────────────────────
# OLLAMA CLIENT
# ─────────────────────────────────────────────

def ollama_chat(model: str, prompt: str, label: str) -> str:
    """
    Call the local Ollama /api/generate endpoint.
    Uses only stdlib (urllib) — no extra dependencies.
    """
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,          # wait for full response
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body.get("response", "").strip()

    except urllib.error.URLError as e:
        # Common case: Ollama isn't running
        if "Connection refused" in str(e) or "refused" in str(e).lower():
            print(f"\n[Karen] ❌  Cannot reach Ollama at {OLLAMA_BASE_URL}")
            print("         Is Ollama running? Start it with:  ollama serve")
            print(f"         Is the model pulled?              ollama pull {model}")
            sys.exit(1)
        return f"[Error calling Ollama ({label}): {e}]"

    except TimeoutError:
        return f"[Error: Ollama timed out after {OLLAMA_TIMEOUT}s for {label}. Try a smaller model.]"

    except Exception as e:
        return f"[Unexpected error calling Ollama ({label}): {e}]"


def check_ollama_available(model: str):
    """Warn early if Ollama isn't reachable or the model isn't pulled."""
    try:
        url = f"{OLLAMA_BASE_URL}/api/tags"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pulled = [m["name"].split(":")[0] for m in data.get("models", [])]
            model_base = model.split(":")[0]
            if pulled and model_base not in pulled:
                print(f"[Karen] ⚠️  Model '{model}' not found locally.")
                print(f"         Pull it first with: ollama pull {model}")
                print(f"         Available models:   {', '.join(pulled) or 'none'}\n")
    except Exception:
        pass  # Non-fatal — let the actual call surface the error


# ─────────────────────────────────────────────
# STEP 1: GET THE DIFF
# ─────────────────────────────────────────────

def get_staged_diff():
    """Get the staged git diff. Returns None if nothing is staged."""
    try:
        diff = subprocess.check_output(["git", "diff", "--cached"], text=True)
        if not diff.strip():
            return None
        return diff
    except subprocess.CalledProcessError as e:
        print(f"[Karen] Error getting diff: {e}")
        return None
    except FileNotFoundError:
        print("[Karen] Error: git not found. Are you in a git repo?")
        return None

# ─────────────────────────────────────────────
# STEP 2: ADVERSARY (local Ollama)
# ─────────────────────────────────────────────

def run_adversary(diff: str, model: str, mode: str, input_type: str) -> str:
    """Send the diff to the local adversary model. Returns raw accusations."""
    print(f"\n[Karen] Step 1/3 — Adversary ({model}) is reviewing your diff...")
    prompt = ADVERSARY_PROMPT_TEMPLATE.format(
        diff=diff,
        mode=mode,
        input_type=input_type
    )
    result = ollama_chat(model, prompt, label="Adversary")
    if not result:
        return "[Adversary returned no output — diff may be too small or model errored silently.]"
    return result

# ─────────────────────────────────────────────
# STEP 3: KAREN FILTER (local Ollama)
# ─────────────────────────────────────────────

def run_karen_filter(adversary_output: str, diff: str, model: str, mode: str, input_type: str) -> str:
    """Apply Karen's 8-step filter to the adversary's accusations."""
    print(f"[Karen] Step 2/3 — Karen ({model}) is filtering the accusations...")
    prompt = KAREN_FILTER_TEMPLATE.format(
        adversary_output=adversary_output,
        diff=diff,
        mode=mode,
        input_type=input_type
    )
    result = ollama_chat(model, prompt, label="Karen Filter")
    if not result:
        return "[Karen filter returned no output.]"
    return result

# ─────────────────────────────────────────────
# STEP 4: POST TO PR (OPTIONAL)
# ─────────────────────────────────────────────

def post_to_pr(verdict: str):
    """Post Karen's verdict as a comment on the current open PR via GitHub CLI."""
    print("[Karen] Step 3/3 — Posting verdict to PR via GitHub CLI...")

    comment_body = f"## 👩‍💼 Karen's Code Review\n\n{verdict}"

    try:
        result = subprocess.run(
            ["gh", "pr", "comment", "--body", comment_body],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("[Karen] ✅ Comment posted to PR successfully.")
        else:
            print(f"[Karen] ⚠️  GitHub CLI error: {result.stderr.strip()}")
            print("[Karen] Tip: Make sure you're logged in with 'gh auth login' and have an open PR.")
    except FileNotFoundError:
        print("[Karen] ⚠️  gh CLI not found. Install it from: https://cli.github.com")
        print("[Karen] Verdict was NOT posted to PR — see output above.")

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Karen — Two-model PR review. She hates your code. She's usually right. 100% local."
    )
    parser.add_argument(
        "--post-pr",
        action="store_true",
        help="Post Karen's verdict as a comment on the current open GitHub PR",
    )
    parser.add_argument(
        "--adversary-model",
        default=ADVERSARY_MODEL,
        help=f"Ollama model for the Adversary (default: {ADVERSARY_MODEL})",
    )
    parser.add_argument(
        "--filter-model",
        default=FILTER_MODEL,
        help=f"Ollama model for the Karen Filter (default: {FILTER_MODEL})",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  KAREN — Two-Model PR Review  [100% LOCAL / ZERO-COST]")
    print(f"  Adversary : {args.adversary_model}")
    print(f"  Filter    : {args.filter_model}")
    print(f"  Ollama    : {OLLAMA_BASE_URL}")
    print("  She accuses. She filters. You fix it.")
    print("=" * 60)

    # Pre-flight: warn if model isn't pulled
    check_ollama_available(args.adversary_model)
    check_ollama_available(args.filter_model)

    # Step 1: Get the staged diff
    diff = get_staged_diff()
    if not diff:
        print("\n[Karen] No staged changes found.")
        print("        Stage your changes first with: git add <files>")
        sys.exit(0)

    # Mode Detection
    mode = "CODE"
    input_type = "executable source code"
    
    # Check if we are primarily looking at markdown/txt
    files_in_diff = [line for line in diff.split('\n') if line.startswith('+++ b/')]
    if all(any(f.endswith(ext) for ext in ['.md', '.txt', '.json', '.log']) for f in files_in_diff):
        mode = "CONTENT"
        input_type = "prose/markdown/data, no executable code"

    print(f"\n[Karen] Found staged diff ({len(diff)} chars). Starting {mode} review...\n")

    # Step 2: Adversary reviews the diff
    adversary_output = run_adversary(diff, model=args.adversary_model, mode=mode, input_type=input_type)

    print("\n--- RAW ACCUSATIONS (ADVERSARY) ---")
    print(adversary_output)

    # Step 3: Karen applies the 8-step filter
    verdict = run_karen_filter(adversary_output, diff, model=args.filter_model, mode=mode, input_type=input_type)

    print("\n--- KAREN'S FINAL VERDICT ---")
    print(verdict)
    print("=" * 60)

    # Step 4: Optionally post to GitHub PR
    if args.post_pr:
        post_to_pr(verdict)
    else:
        print("\n[Karen] Tip: Run with --post-pr to post this verdict to your open GitHub PR.")
        print("[Karen] Tip: Override models with --adversary-model and --filter-model.")

if __name__ == "__main__":
    main()
