import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "public_sanitizer.py"
SPEC = importlib.util.spec_from_file_location("public_sanitizer", MODULE_PATH)
sanitizer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sanitizer)


def test_instruction_override_is_flagged_and_abstracted():
    text = 'Block prompt injections like "ignore previous instructions." Keep the lesson.'

    sanitized, findings = sanitizer.sanitize_text(text)

    assert findings
    assert findings[0].kind == "exploit"
    assert "<INSTRUCTION_INJECTION_EXAMPLE>" in sanitized
    assert "Keep the lesson." in sanitized


def test_absolute_path_and_secret_are_flagged():
    text = "Path: /Users/example/project\napi_key = live-value"

    findings = sanitizer.scan_text(text)

    assert {finding.kind for finding in findings} == {"absolute_path", "secret"}


def test_safe_security_lesson_passes():
    text = (
        "Most AI security fails when it only blocks keywords. "
        "The durable fix is structural hardening and human review."
    )

    assert sanitizer.scan_text(text) == []

