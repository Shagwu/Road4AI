import os
import re
import sys
from datetime import datetime
from tools.locker import file_lock

PLAN_FILE = "CONTENT_PLAN_APRIL.md"
CONTEXT_FILE = ".agents/product-marketing-context.md"
DRAFTS_DIR = "drafts"

def get_today_task():
    today = datetime.now().strftime("%B %-d") # e.g., "April 23"
    if not os.path.exists(PLAN_FILE):
        return None
    
    with open(PLAN_FILE, 'r') as f:
        content = f.read()
        
    # Match row: | Date | Topic | Platform | Status |
    pattern = rf"\| {today} \| (.*?) \| (.*?) \| (.*?) \|"
    match = re.search(pattern, content)
    if match:
        return {
            "topic": match.group(1).strip(),
            "platforms": match.group(2).strip(),
            "status": match.group(3).strip()
        }
    return None

def update_status(topic, new_status):
    with file_lock("content-plan"):
        with open(PLAN_FILE, 'r') as f:
            lines = f.readlines()
            
        with open(PLAN_FILE, 'w') as f:
            for line in lines:
                if topic in line:
                    # Replace the last column value
                    parts = line.split('|')
                    if len(parts) >= 5:
                        parts[4] = f" {new_status} "
                        line = '|'.join(parts)
                f.write(line)

def main():
    task = get_today_task()
    if not task:
        print("No task found for today.")
        return

    if task['status'] == "Drafted" or task['status'] == "Complete":
        print(f"Task '{task['topic']}' already {task['status']}.")
        return

    print(f"Processing task: {task['topic']}")
    
    # In a real scenario, this would call an LLM with the context.
    # For this automation setup, we generate the skeleton.
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = task['topic'].lower().replace(" ", "-").replace("/", "-")
    draft_path = os.path.join(DRAFTS_DIR, f"{date_str}-{slug}.md")
    
    context = ""
    if os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE, 'r') as f:
            context = f.read()

    draft_content = f"""# Daily Draft: {task['topic']}
Date: {date_str}

## Twitter/X Draft
[TODO: Generate high-signal thread based on {task['topic']}]
- Reference: {task['topic']}
- Tone: Technical, direct, "Liberated Research"

## LinkedIn Draft
[TODO: Generate long-form post based on {task['topic']}]

---
### Product Context Ref
{context[:500]}... (truncated)
"""
    
    with open(draft_path, 'w') as f:
        f.write(draft_content)
        
    update_status(task['topic'], "Drafted")
    print(f"Draft created at {draft_path}")

if __name__ == "__main__":
    main()
