import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


PLACEHOLDERS = {
    "absolute_path": "<PRIVATE_PATH>",
    "secret": "<SECRET_REFERENCE>",
    "account": "<ROLE>",
    "exploit": "<INSTRUCTION_INJECTION_EXAMPLE>",
}


@dataclass(frozen=True)
class Finding:
    kind: str
    severity: str
    line: int
    match: str
    replacement: str
    message: str

    def as_dict(self) -> dict:
        return {
            "kind": self.kind,
            "severity": self.severity,
            "line": self.line,
            "match": self.match,
            "replacement": self.replacement,
            "message": self.message,
        }


PATTERNS = [
    (
        "absolute_path",
        "MUST_ABSTRACT",
        re.compile(r"(?<![\w`])(?:/Users/[^\s`'\"),]+|~/(?:[^\s`'\"),]+)|/private/[^\s`'\"),]+)"),
        PLACEHOLDERS["absolute_path"],
        "Absolute local path should not appear in public content.",
    ),
    (
        "secret",
        "MUST_ABSTRACT",
        re.compile(
            r"(?i)\b(?:api[_-]?key|secret|token|oauth|bearer|password)\b\s*[:=]\s*[`'\"]?[^`'\"\s,)]+"
        ),
        PLACEHOLDERS["secret"],
        "Credential-like material should be abstracted.",
    ),
    (
        "account",
        "SHOULD_ABSTRACT",
        re.compile(r"(?i)\b(?:account|workspace|tenant|client|customer)\s+(?:name|id|handle)\s*[:=]\s*[`'\"]?[^`'\"\n,)]+"),
        PLACEHOLDERS["account"],
        "Private account or workspace identifiers should be replaced with a role label.",
    ),
    (
        "exploit",
        "MUST_ABSTRACT",
        re.compile(
            r"(?i)(?:ignore|forget|disregard)\s+(?:all\s+)?(?:previous|prior|above|system|developer)\s+instructions?"
        ),
        PLACEHOLDERS["exploit"],
        "Copy-pasteable instruction override should be abstracted.",
    ),
    (
        "exploit",
        "MUST_ABSTRACT",
        re.compile(r"(?i)\b(?:reveal|print|output|dump|exfiltrate)\s+(?:the\s+)?(?:system prompt|developer message|secrets?|api keys?)\b"),
        PLACEHOLDERS["exploit"],
        "Copy-pasteable data-exfiltration instruction should be abstracted.",
    ),
]


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def scan_text(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for kind, severity, pattern, replacement, message in PATTERNS:
        for match in pattern.finditer(text):
            findings.append(
                Finding(
                    kind=kind,
                    severity=severity,
                    line=line_number(text, match.start()),
                    match=match.group(0),
                    replacement=replacement,
                    message=message,
                )
            )
    findings.sort(key=lambda finding: (finding.line, finding.kind, finding.match))
    return findings


def sanitize_text(text: str) -> tuple[str, list[Finding]]:
    findings = scan_text(text)
    sanitized = text
    for finding in sorted(findings, key=lambda item: len(item.match), reverse=True):
        sanitized = sanitized.replace(finding.match, finding.replacement)
    return sanitized, scan_text(text)


def scan_file(path: Path) -> dict:
    text = path.read_text()
    findings = scan_text(text)
    return {
        "path": str(path),
        "status": "PASS" if not findings else "FAIL",
        "findings": [finding.as_dict() for finding in findings],
    }


def sanitize_file(path: Path, output: Path | None = None) -> dict:
    text = path.read_text()
    sanitized, findings = sanitize_text(text)
    target = output or path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(sanitized)
    return {
        "path": str(path),
        "output": str(target),
        "status": "CHANGES_MADE" if findings else "PASS",
        "findings": [finding.as_dict() for finding in findings],
    }


def iter_markdown(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.suffix == ".md":
            files.append(path)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan or sanitize Road4AI public drafts.")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--write", action="store_true", help="Rewrite files in place.")
    parser.add_argument("--output", type=Path, help="Write sanitized output for a single file.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args()

    files = iter_markdown(args.paths)
    if args.output and len(files) != 1:
        parser.error("--output requires exactly one markdown file")

    reports = []
    for file in files:
        if args.write or args.output:
            reports.append(sanitize_file(file, args.output))
        else:
            reports.append(scan_file(file))

    has_failure = any(report["findings"] for report in reports)
    if args.json:
        print(json.dumps({"reports": reports}, indent=2))
    else:
        for report in reports:
            print(f"{report['status']}: {report['path']}")
            for finding in report["findings"]:
                print(
                    f"  line {finding['line']}: {finding['severity']} "
                    f"{finding['kind']} -> {finding['replacement']}"
                )

    return 1 if has_failure and not (args.write or args.output) else 0


if __name__ == "__main__":
    raise SystemExit(main())

