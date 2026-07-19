import os
import json
from groq import Groq
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
with open(os.path.join(PROMPTS_DIR, "agent_prompt.txt"), "r") as f:
    SYSTEM_PROMPT = f.read()

def process_agent_step(messages: list) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"action": "finish", "response": "API Error: Missing GROQ_API_KEY in environment"}
        
    client = Groq(api_key=api_key) 
    
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=full_messages,
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return data
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return {"action": "finish", "response": f"API Error: {str(e)}"}
