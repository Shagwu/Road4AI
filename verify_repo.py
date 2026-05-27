import argparse
import json
import os
import sys

from magika import Magika


EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_SCAN_ERRORS = 2


def verify_directory(path):
    magika = Magika()

    results = {
        "path": os.path.abspath(path),
        "scanned_files": [],
        "mismatches": [],
        "binaries": [],
        "errors": [],
    }

    for root, dirs, files in os.walk(path):
        # Skip noisy directories
        dirs[:] = [d for d in dirs if d not in [".git", "__pycache__", ".venv", ".worktrees"]]

        for file in files:
            file_path = os.path.join(root, file)
            try:
                result = magika.identify_path(file_path)
                label = result.output.label
                ext = os.path.splitext(file)[1].lower().replace(".", "")

                results["scanned_files"].append(
                    {
                        "path": file_path,
                        "name": file,
                        "extension": ext,
                        "label": label,
                    }
                )

                text_types = ["python", "javascript", "markdown", "json", "yaml", "text", "txt"]
                if ext in ["txt", "md"] and label not in text_types and "text" not in label and "markdown" not in label:
                    results["mismatches"].append(
                        {
                            "path": file_path,
                            "extension": ext,
                            "detected_type": label,
                        }
                    )

                if "executable" in label or "binary" in label:
                    results["binaries"].append(
                        {
                            "path": file_path,
                            "detected_type": label,
                        }
                    )
            except Exception as e:
                results["errors"].append(
                    {
                        "path": file_path,
                        "error": str(e),
                    }
                )

    return results


def determine_exit_code(results):
    if results["errors"]:
        return EXIT_SCAN_ERRORS
    if results["mismatches"] or results["binaries"]:
        return EXIT_FINDINGS
    return EXIT_CLEAN


def print_text_report(results):
    print(f"--- Scanning: {results['path']} ---")

    for scanned_file in results["scanned_files"]:
        print(f"  - {scanned_file['name']}: {scanned_file['label']}")

    if results["mismatches"]:
        print("\n[!] SUSPICIOUS MISMATCHES (Content vs Extension):")
        for item in results["mismatches"]:
            print(
                f"  - {item['path']} "
                f"(Ext: {item['extension']} | Content: {item['detected_type']})"
            )

    if results["binaries"]:
        print("\n[*] BINARIES/EXECUTABLES FOUND:")
        for item in results["binaries"]:
            print(f"  - {item['path']} ({item['detected_type']})")

    if results["errors"]:
        print("\n[-] SCAN ERRORS:")
        for item in results["errors"]:
            print(f"  - {item['path']}: {item['error']}")

    if not results["mismatches"] and not results["binaries"] and not results["errors"]:
        print("\n[+] No suspicious files detected.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scan a repository for suspicious file type mismatches and binaries."
    )
    parser.add_argument("path", nargs="?", default=".", help="Directory to scan")
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Emit machine-readable JSON instead of text output",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    results = verify_directory(args.path)
    exit_code = determine_exit_code(results)

    if args.json_output:
        print(json.dumps(results, indent=2))
    else:
        print_text_report(results)

    sys.exit(exit_code)
