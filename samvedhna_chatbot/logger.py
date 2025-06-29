# 📁 Updated File: logger.py — Resilient Session-Based Logger

import json
import os
import uuid
from datetime import datetime
import streamlit as st

def initialize_logging():
    """Initialize logging system for both local and cloud environments"""
    session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{str(uuid.uuid4())[:8]}"
    
    # Initialize session state for logging if not exists
    if "log_data" not in st.session_state:
        st.session_state.log_data = {
            "sessions": [{
                "session_id": session_id,
                "start_time": str(datetime.now()),
                "messages": []
            }]
        }
    
    # For local environment, also maintain file-based logging
    if not os.getenv('STREAMLIT_CLOUD'):
        log_file = "conversation_log.json"
        if not os.path.exists(log_file):
            data = {"sessions": []}
        else:
            try:
                with open(log_file, "r") as f:
                    data = json.load(f)
                    if not isinstance(data, dict) or "sessions" not in data:
                        data = {"sessions": []}
            except json.JSONDecodeError:
                data = {"sessions": []}
        
        # Add new session entry to file
        session_entry = {
            "session_id": session_id,
            "start_time": str(datetime.now()),
            "messages": []
        }
        data["sessions"].append(session_entry)
        
        with open(log_file, "w") as f:
            json.dump(data, f, indent=2)

def log_message(message, emotion, score, lang):
    """Log message to both session state and file (if local)"""
    entry = {
        "timestamp": str(datetime.now()),
        "message": message,
        "emotion": emotion,
        "score": score,
        "lang": lang
    }

    # Always log to session state
    st.session_state.log_data["sessions"][-1]["messages"].append(entry)

    # For local environment, also log to file
    if not os.getenv('STREAMLIT_CLOUD'):
        log_file = "conversation_log.json"
        try:
            with open(log_file, "r") as f:
                data = json.load(f)
            
            data["sessions"][-1]["messages"].append(entry)
            
            with open(log_file, "w") as f:
                json.dump(data, f, indent=2)
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Skip file logging if there are issues

def get_log_data():
    """Get log data from the appropriate source"""
    # Always return from session state in cloud
    if os.getenv('STREAMLIT_CLOUD'):
        return st.session_state.log_data.get("sessions", [])
    
    # For local environment, try to get from file first
    log_file = "conversation_log.json"
    try:
        with open(log_file, "r") as f:
            data = json.load(f)
            return data.get("sessions", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return st.session_state.log_data.get("sessions", [])  # Fallback to session state

# Initialize logging system when the module is imported
initialize_logging()
