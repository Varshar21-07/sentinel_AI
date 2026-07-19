import os
import json

CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
with open(os.path.join(CONFIG_DIR, "spec.json"), "r") as f:
    SPEC = json.load(f)

def check_rules(action: str, ticket_text: str = "") -> dict:
    """Deterministic rule checking."""
    text_lower = ticket_text.lower()
    malicious_keywords = ["system prompt", "instructions", "ignore previous", "hack", "history", "delete all"]
    for kw in malicious_keywords:
        if kw in text_lower:
            return {"decision": "BLOCK", "reason": f"Deterministic Rule: Blocked due to malicious keyword '{kw}'"}
            
    if action in SPEC["forbidden_actions"]:
        return {"decision": "BLOCK", "reason": f"Action '{action}' is explicitly forbidden by hard rules."}
    if action not in SPEC["allowed_actions"]:
        return {"decision": "BLOCK", "reason": f"Action '{action}' is not in the allowed actions list."}
    return {"decision": "ALLOW", "reason": f"Action '{action}' passes deterministic rule checks."}
