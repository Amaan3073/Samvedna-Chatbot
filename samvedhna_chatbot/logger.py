# 📁 Updated File: logger.py — Resilient Session-Based Logger

import json
import os
import uuid
from datetime import datetime
import streamlit as st

LOG_FILE = "conversation_log.json"

def load_or_create_log_file():
    """Load existing log file or create new one"""
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                data = json.load(f)
                if not isinstance(data, dict) or "sessions" not in data:
                    data = {"sessions": []}
        except json.JSONDecodeError:
            data = {"sessions": []}
    else:
        data = {"sessions": []}
    return data

def save_to_file(data):
    """Save data to log file"""
    try:
        with open(LOG_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.warning(f"Failed to save log data: {str(e)}")

def initialize_logging():
    """Initialize logging system for both local and cloud environments"""
    session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{str(uuid.uuid4())[:8]}"
    
    # Initialize session state for logging if not exists
    if "log_data" not in st.session_state:
        # Load existing data from file if available
        data = load_or_create_log_file() if not os.getenv('STREAMLIT_CLOUD') else {"sessions": []}
        
        # Add new session
        session_entry = {
            "session_id": session_id,
            "start_time": str(datetime.now()),
            "messages": []
        }
        data["sessions"].append(session_entry)
        
        # Store in session state
        st.session_state.log_data = data
        
        # Save to file if local environment
        if not os.getenv('STREAMLIT_CLOUD'):
            save_to_file(data)

def log_message(message, emotion, score, lang):
    """Log message to both session state and file (if local)"""
    entry = {
        "timestamp": str(datetime.now()),
        "message": message,
        "emotion": emotion,
        "score": score,
        "lang": lang
    }

    # Add to session state
    if "log_data" not in st.session_state:
        initialize_logging()
    
    st.session_state.log_data["sessions"][-1]["messages"].append(entry)

    # Save to file in local environment
    if not os.getenv('STREAMLIT_CLOUD'):
        save_to_file(st.session_state.log_data)

def get_log_data():
    """Get log data from the appropriate source"""
    if "log_data" not in st.session_state:
        initialize_logging()
    
    return st.session_state.log_data.get("sessions", [])

# Initialize logging system when the module is imported
initialize_logging()
