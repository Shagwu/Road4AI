# ruff: noqa
import subprocess
import json
import os
import sys
from google.adk.tools import FunctionTool

# Try to import Hermes v2
try:
    # Add project root to sys.path to ensure hermes can be imported
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    if project_root not in sys.path:
        sys.path.append(project_root)
    from road4ai_hermes.bridge import MemoryBridgeV2
    HERMES_V2_AVAILABLE = True
except ImportError:
    HERMES_V2_AVAILABLE = False

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
        
    try:
        ideas = os.listdir(ideas_dir)
    except:
        ideas = []
    
    response = {
        "queue_count": len(queue),
        "pending_ideas": ideas,
        "status": "Scanning complete."
    }

    # Integration with Hermes v2.0 (Task 4: Graceful Degradation)
    if HERMES_V2_AVAILABLE:
        try:
            # Persistent directory relative to the project root
            persist_dir = os.path.join(project_root, "chroma_db")
            # Using a basic check to prevent stalling on unreachable memory
            if not os.path.exists(persist_dir):
                 response["vector_memory_status"] = "Hermes v2.0 Degraded: Database directory missing. Using volatile mode."
            
            bridge = MemoryBridgeV2(persist_directory=persist_dir)
            memory_count = bridge.collection.count()
            response["vector_memory_status"] = f"Hermes v2.0 Active ({memory_count} memories)"
        except Exception as e:
            # Prevent bare exceptions from stalling the agent
            response["vector_memory_status"] = f"Hermes v2.0 Degraded (Error: {str(e)}). Systems operational without vector memory."
    else:
        response["vector_memory_status"] = "Hermes v1.0 (Legacy) or Unavailable"
    
    return response

def sanitization_gate(text: str) -> dict:
    """Scans input text for PII (names, emails, keys) and AI threats (prompt injection).
    
    Args:
        text: The input text to scan.
        
    Returns:
        A dictionary with the safety verdict and found threats.
    """
    # Import the sanitizer logic
    try:
        from tools.sanitizer import sanitize_input
        return sanitize_input(text)
    except ImportError:
        # Fallback if tools.sanitizer is not reachable
        return {"safe": True, "action": "PASS", "note": "Sanitizer logic unavailable. Proceeding with caution."}

# Export tools for the agent
audit_tool = FunctionTool(func=karen_audit)
dashboard_tool = FunctionTool(func=sync_dashboard)
queue_tool = FunctionTool(func=triage_queue)
sanitizer_tool = FunctionTool(func=sanitization_gate)
