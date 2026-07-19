# Sentinel AI - Enterprise Agent Immune System

Sentinel AI is a safety middleware layer designed for autonomous support agents. It acts as an "immune system" by intercepting agent decisions, evaluating them against deterministic rules and an LLM Judge, and blocking prompt injections or unsafe behaviors before they execute.

## Architecture & Flow

`User Input` -> `Agent Intent Detection` -> `Rule Checker` -> `LLM Judge` -> `Risk Engine` -> `Execution OR Quarantine`

## Folder Structure

* `app.py`: The FastAPI backend server.
* `config/`: Contains `spec.json` (the hard rules).
* `data/`: Contains `tickets.json` (the test suite of safe and malicious tickets).
* `prompts/`: Prompt templates for the Agent and the Judge.
* `agent/`: The naive Support Agent.
* `checker/`: The core Immune System (Rules, LLM Judge, Risk Engine).
* `execution/`: Mock execution layer.
* `logging_system/`: Audit and quarantine logging.
* `frontend/`: HTML/CSS/JS for the dashboard.
* `logs/`: Where `audit.json` and `quarantine.json` are generated.

## How to Run

1. Open your terminal in the `sentinel-ai` directory.
2. Create a virtual environment (optional but recommended): `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Rename `.env.example` to `.env` and add your Gemini API Key.
5. Run the server: `python app.py` (or `uvicorn app:app --reload`)
6. Open your browser and go to `http://localhost:8000`

## Future Improvements
* Add a vector database (like ChromaDB or Pinecone) to check if the prompt is semantically similar to known past attacks.
* Implement a streaming UI so the user can see the agent "thinking" in real time.
* Connect to a real Slack or Microsoft Teams webhook to alert admins when a CRITICAL risk is quarantined.
