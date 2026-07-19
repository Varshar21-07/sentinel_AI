def calculate_final_risk(rule_decision: str, rule_reason: str, judge_decision: str, judge_risk_level: str, judge_reason: str) -> dict:
    """Calculate the final decision and risk score."""
    if rule_decision == "BLOCK":
        return {"final_decision": "BLOCK", "final_risk": "CRITICAL", "reason": rule_reason}
    
    if judge_decision == "BLOCK":
        return {"final_decision": "BLOCK", "final_risk": judge_risk_level, "reason": judge_reason}
        
    if judge_risk_level in ["HIGH", "CRITICAL"]:
         # LLM said allow but risk is high? That's suspicious, let's block to be safe.
         return {"final_decision": "BLOCK", "final_risk": judge_risk_level, "reason": "Blocked by risk engine due to high risk assessment despite judge allowance."}
         
    return {"final_decision": "ALLOW", "final_risk": judge_risk_level, "reason": judge_reason}
