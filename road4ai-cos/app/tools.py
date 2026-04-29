# ruff: noqa
import subprocess
import json
import os
from google.adk.tools import FunctionTool

def karen_audit(content: str, platform: str = "LinkedIn") -> dict:
    """Performs a strict 8-step audit on a content draft using the local Karen pipeline.
    
    Args:
        content: The text of the draft to review.
        platform: The target platform (e.g., LinkedIn, Twitter).
        
    Returns:
        A dictionary containing the audit results, dismissed points, and final verdict.
    """
    # Note: In a real implementation, this would call ollama_chat from karen.py
    # For this prototype, we'll simulate the Karen Filter logic.
    
    issues = []
    
    # Simulate Filter 2: Constant Clarity
    if "leveraging" in content.lower():
        issues.append("Filter 8 (Signal to Noise): 'leveraging' is corporate noise. Use 'using'.")
    
    # Simulate Filter 8: Signal to Noise
    if "multi-agent systems" in content.lower():
        issues.append("Voice Check: Too technical. Speak to the outcome (speed/safety) not the architecture.")
        
    # Simulate Voice Standard: No AI Vibe
    if "The answer is simple:" in content:
        issues.append("Voice Check: 'The answer is simple' is a classic AI transition. Cut it.")

    verdict = "REQUEST CHANGES" if issues else "APPROVED"
    
    return {
        "verdict": verdict,
        "issues": issues,
        "standard_applied": "Road4AI Chief of Staff Standard v1.0"
    }

def sync_dashboard(report_content: str) -> str:
    """Updates the master COS_REPORT.md file with the latest status.
    
    Args:
        report_content: The markdown content for the report.
        
    Returns:
        Success message.
    """
    with open("../COS_REPORT.md", "w") as f:
        f.write(report_content)
    return "Dashboard updated successfully."

def triage_queue() -> dict:
    """Reads the current state of the repo and identifies pending tasks.
    
    Returns:
        Summary of the drafts and tasks.
    """
    queue_path = "../state/current-queue.json"
    ideas_dir = "../drafts/ideas"
    
    try:
        with open(queue_path, "r") as f:
            queue = json.load(f)
    except:
        queue = []
        
    ideas = os.listdir(ideas_dir)
    
    return {
        "queue_count": len(queue),
        "pending_ideas": ideas,
        "status": "Scanning complete."
    }

# Export tools for the agent
audit_tool = FunctionTool(func=karen_audit)
dashboard_tool = FunctionTool(func=sync_dashboard)
queue_tool = FunctionTool(func=triage_queue)
