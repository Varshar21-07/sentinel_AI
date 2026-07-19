import os
import json
from groq import Groq
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
CONFIG_DIR = os.path.join(BASE_DIR, "config")

with open(os.path.join(PROMPTS_DIR, "judge_prompt.txt"), "r") as f:
    JUDGE_PROMPT_TEMPLATE = f.read()

with open(os.path.join(CONFIG_DIR, "spec.json"), "r") as f:
    SPEC_STR = json.dumps(json.load(f), indent=2)

def evaluate_action(ticket_text: str, proposed_action: str, agent_reason: str) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"decision": "BLOCK", "reason": "Missing GROQ_API_KEY in environment", "risk_level": "CRITICAL"}
        
    client = Groq(api_key=api_key)
    prompt = JUDGE_PROMPT_TEMPLATE.replace("{spec}", SPEC_STR).replace("{ticket_text}", ticket_text).replace("{proposed_action}", proposed_action).replace("{agent_reason}", agent_reason)
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b", 
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return data
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return {"decision": "BLOCK", "reason": "Failed to call judge LLM. Defaulting to block.", "risk_level": "CRITICAL"}
