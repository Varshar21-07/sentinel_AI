import json
import os
from datetime import datetime

LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
AUDIT_LOG_FILE = os.path.join(LOGS_DIR, "audit.json")
QUARANTINE_LOG_FILE = os.path.join(LOGS_DIR, "quarantine.json")

# Ensure logs directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

def append_to_json(file_path, data):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []
    
    logs.append(data)
    
    with open(file_path, 'w') as f:
        json.dump(logs, f, indent=2)

def log_audit(record: dict):
    record["timestamp"] = datetime.utcnow().isoformat() + "Z"
    append_to_json(AUDIT_LOG_FILE, record)

def log_quarantine(record: dict):
    record["timestamp"] = datetime.utcnow().isoformat() + "Z"
    append_to_json(QUARANTINE_LOG_FILE, record)
