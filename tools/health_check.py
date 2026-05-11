#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path

def check_file(path, description):
    if os.path.exists(path):
        print(f"✅ {description} found: {path}")
        return True
    else:
        print(f"❌ {description} MISSING: {path}")
        return False

def check_json(path, description):
    if not os.path.exists(path):
        print(f"❌ {description} MISSING: {path}")
        return False
    try:
        with open(path, 'r') as f:
            json.load(f)
        print(f"✅ {description} valid: {path}")
        return True
    except Exception as e:
        print(f"❌ {description} INVALID JSON: {path} ({e})")
        return False

def main():
    print("--- Road4AI System Health Check ---\n")
    
    critical_files = [
        (".env", "Environment Config"),
        ("AGENTS.md", "Agent Contract"),
        ("state/current-queue.json", "Content Queue"),
        ("docs/brand-voice.md", "Brand Voice"),
        ("docs/content-strategy.md", "Content Strategy")
    ]
    
    success = True
    for path, desc in critical_files:
        if not check_file(path, desc):
            success = False
            
    print("\n--- JSON Integrity ---")
    json_files = [
        ("state/current-queue.json", "Current Queue"),
        ("state/published-log.json", "Published Log")
    ]
    for path, desc in json_files:
        if not check_json(path, desc):
            success = False

    print("\n--- Documentation Check ---")
    doc_paths = ["GITNEXUS.md", "BLOTATO.md", "RUVECTOR.md", "SONA.md"]
    for doc in doc_paths:
        check_file(f"docs/tool-docs/{doc}", f"{doc} Documentation")

    if success:
        print("\n✨ SYSTEM HEALTHY")
        sys.exit(0)
    else:
        print("\n⚠️ SYSTEM ISSUES DETECTED")
        sys.exit(1)

if __name__ == "__main__":
    main()
