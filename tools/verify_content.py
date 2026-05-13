import json
import os
import sys
import re

def check_json_integrity(directory):
    print("Checking JSON integrity...")
    success = True
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            path = os.path.join(directory, filename)
            try:
                with open(path, 'r') as f:
                    json.load(f)
                # print(f"  [OK] {filename}")
            except Exception as e:
                print(f"  [FAIL] {filename}: {e}")
                success = False
    return success

def check_x_draft_length(queue_path):
    print("Checking X draft lengths (max 280 chars)...")
    success = True
    try:
        with open(queue_path, 'r') as f:
            data = json.load(f)
            for item in data.get("queue", []):
                platform = item.get("platform", "")
                if "X" in platform:
                    hook = item.get("hook", "")
                    if len(hook) > 280:
                        print(f"  [FAIL] {item.get('id')}: Hook too long ({len(hook)} chars)")
                        success = False
    except Exception as e:
        print(f"  Error reading queue for X check: {e}")
        success = False
    return success

def check_queue_consistency(queue_path):
    print("Checking queue consistency (missing scheduled_time)...")
    success = True
    try:
        with open(queue_path, 'r') as f:
            data = json.load(f)
            for item in data.get("queue", []):
                if item.get("status") == "scheduled":
                    if not item.get("scheduled_time"):
                        print(f"  [FAIL] {item.get('id')}: Marked as scheduled but missing scheduled_time")
                        success = False
    except Exception as e:
        print(f"  Error reading queue for consistency check: {e}")
        success = False
    return success

def main():
    state_dir = "state"
    queue_file = os.path.join(state_dir, "current-queue.json")
    
    ok = True
    if not check_json_integrity(state_dir): ok = False
    if not check_x_draft_length(queue_file): ok = False
    if not check_queue_consistency(queue_file): ok = False
    
    if not ok:
        sys.exit(1)
    print("All health checks passed.")

if __name__ == "__main__":
    main()
