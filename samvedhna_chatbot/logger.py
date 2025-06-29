# 📁 Updated File: logger.py — Resilient Session-Based Logger

import json
import os
import uuid
from datetime import datetime

log_file = "conversation_log.json"
session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{str(uuid.uuid4())[:8]}"

# Robust loading with fallback
if not os.path.exists(log_file):
    data = {"sessions": []}
else:
    with open(log_file, "r") as f:
        try:
            data = json.load(f)
            if not isinstance(data, dict) or "sessions" not in data:
                data = {"sessions": []}
        except json.JSONDecodeError:
            data = {"sessions": []}

# Add new session entry
session_entry = {
    "session_id": session_id,
    "start_time": str(datetime.now()),
    "messages": []
}
data["sessions"].append(session_entry)

with open(log_file, "w") as f:
    json.dump(data, f, indent=2)

# Logging function

def log_message(message, emotion, score, lang):
    entry = {
        "timestamp": str(datetime.now()),
        "message": message,
        "emotion": emotion,
        "score": score,
        "lang": lang
    }

    with open(log_file, "r") as f:
        data = json.load(f)

    data["sessions"][-1]["messages"].append(entry)

    with open(log_file, "w") as f:
        json.dump(data, f, indent=2)
