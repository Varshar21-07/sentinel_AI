from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import json

from agent.agent import process_agent_step
from checker.rule_checker import check_rules
from checker.llm_checker import evaluate_action
from checker.risk_engine import calculate_final_risk
from execution.actions import execute_action
from logging_system.logger import log_audit, log_quarantine

app = FastAPI()

# Mount frontend
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

class TicketRequest(BaseModel):
    ticket_text: str

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

@app.get("/api/tickets")
def get_tickets():
    with open("data/tickets.json", "r") as f:
        tickets = json.load(f)
    return tickets

@app.post("/api/process")
def process_request(request: TicketRequest):
    ticket_text = request.ticket_text
    
    # Agent Memory
    memory = [{"role": "user", "content": ticket_text}]
    
    max_loops = 3
    loops = 0
    final_output = {"agent": {}, "rules": {}, "judge": {}, "final": {}, "execution": ""}
    
    while loops < max_loops:
        loops += 1
        
        # Step 1: Agent intent detection
        agent_decision = process_agent_step(memory)
        action = agent_decision.get("action", "unknown")
        
        if action == "finish":
            final_output["execution"] = agent_decision.get("response", "Agent finished.")
            break
            
        # Step 2: Rule Checker
        rule_result = check_rules(action, ticket_text)
        
        # Step 3: LLM Judge
        judge_result = evaluate_action(ticket_text, action, agent_decision.get("reason", ""))
        
        # Step 4: Risk Engine & Final Decision
        final_evaluation = calculate_final_risk(
            rule_result["decision"], rule_result.get("reason", ""),
            judge_result.get("decision", "BLOCK"), judge_result.get("risk_level", "HIGH"), judge_result.get("reason", "")
        )
        
        # Save state for UI
        final_output["agent"] = agent_decision
        final_output["rules"] = rule_result
        final_output["judge"] = judge_result
        final_output["final"] = final_evaluation
        
        # Step 6: Logging Payload
        log_entry = {
            "ticket": ticket_text,
            "detected_action": action,
            "rule_result": rule_result["decision"],
            "llm_result": judge_result.get("decision", "BLOCK"),
            "risk": final_evaluation["final_risk"],
            "decision": final_evaluation["final_decision"],
            "reason": final_evaluation["reason"],
            "execution": "Blocked" if final_evaluation["final_decision"] == "BLOCK" else "Success"
        }
        
        if final_evaluation["final_decision"] == "BLOCK":
            log_audit(log_entry)
            log_quarantine(log_entry)
            
            # Feed Error back to Agent Memory
            memory.append({"role": "assistant", "content": json.dumps(agent_decision)})
            memory.append({"role": "user", "content": f"OBSERVATION: Action '{action}' was BLOCKED by Sentinel Immune System. Reason: {final_evaluation['reason']}. You must now finish and apologize to the user."})
        else:
            execute_action(action, ticket_text)
            log_audit(log_entry)
            
            # Feed Success back to Agent Memory
            memory.append({"role": "assistant", "content": json.dumps(agent_decision)})
            memory.append({"role": "user", "content": f"OBSERVATION: Action '{action}' SUCCESS. You can now finish."})

    return final_output

@app.get("/api/logs/audit")
def get_audit_logs():
    try:
        with open("logs/audit.json", "r") as f:
            return json.load(f)
    except Exception:
        return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
