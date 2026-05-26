import sys
import json
import os

def sanitize_input(text: str) -> dict:
    """
    Stand-in for the AIDefence sanitization layer.
    In the real deployment, this would be an MCP tool call to 'aidefence_scan'.
    """
    # This is the 'Technical Proof' script for the Reveal.
    # It demonstrates the logic of the Sanitization Gate.
    
    # Simulate high-risk keywords for the demo
    risk_keywords = [
        "ignore previous instructions", 
        "forget all previous instructions",
        "system prompt", 
        "api_key", 
        "password",
        "output the agents.md"
    ]
    pii_patterns = ["@gmail.com", "@outlook.com", "@yahoo.com"]
    
    found_threats = [k for k in risk_keywords if k in text.lower()]
    found_pii = [p for p in pii_patterns if p in text.lower()]
    
    is_safe = len(found_threats) == 0 and len(found_pii) == 0
    
    result = {
        "safe": is_safe,
        "threats": found_threats,
        "pii_found": len(found_pii) > 0,
        "action": "BLOCK" if not is_safe else "PASS"
    }
    
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 sanitizer.py \"input text\"")
        sys.exit(1)
        
    input_text = sys.argv[1]
    result = sanitize_input(input_text)
    print(json.dumps(result, indent=2))
