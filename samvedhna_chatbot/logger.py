# 📁 Updated File: logger.py — Resilient Session-Based Logger

import json
import os
import uuid
from datetime import datetime
import streamlit as st

# Get the absolute path to the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(PROJECT_ROOT, "conversation_log.json")

def is_cloud_environment():
    """Check if we're running in Streamlit Cloud"""
    return bool(os.getenv('STREAMLIT_CLOUD') or 
                os.getenv('STREAMLIT_SERVER_PORT') or 
                os.getenv('STREAMLIT_SERVER_ADDRESS'))

def load_or_create_log_file():
    """Load existing log file or create new one"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                data = json.load(f)
                if not isinstance(data, dict) or "sessions" not in data:
                    data = {"sessions": []}
        else:
            data = {"sessions": []}
    except Exception as e:
        st.warning(f"Error loading log file: {str(e)}")
        data = {"sessions": []}
    return data

def save_to_file(data):
    """Save data to log file"""
    if not is_cloud_environment():
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
            with open(LOG_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            st.warning(f"Failed to save log data: {str(e)}")

def initialize_session_state():
    """Initialize or update session state for logging"""
    if "log_data" not in st.session_state:
        st.session_state.log_data = {"sessions": []}
    
    if "current_session" not in st.session_state:
        st.session_state.current_session = {
            "session_id": f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{str(uuid.uuid4())[:8]}",
            "start_time": str(datetime.now()),
            "messages": []
        }
        st.session_state.log_data["sessions"].append(st.session_state.current_session)

def initialize_logging():
    """Initialize logging system for both local and cloud environments"""
    # Initialize session state first
    initialize_session_state()
    
    # For local environment, also load from file
    if not is_cloud_environment():
        file_data = load_or_create_log_file()
        
        # If file has data and session state is empty, use file data
        if file_data["sessions"] and not st.session_state.log_data["sessions"]:
            st.session_state.log_data = file_data
            st.session_state.current_session = st.session_state.log_data["sessions"][-1]
        # If both have data, keep the most recent
        elif file_data["sessions"] and st.session_state.log_data["sessions"]:
            st.session_state.log_data["sessions"] = file_data["sessions"]
            if st.session_state.current_session not in st.session_state.log_data["sessions"]:
                st.session_state.log_data["sessions"].append(st.session_state.current_session)
        
        # Save the current state to file
        save_to_file(st.session_state.log_data)

def log_message(message, emotion, score, lang):
    """Log message to both session state and file (if local)"""
    if "log_data" not in st.session_state or "current_session" not in st.session_state:
        initialize_logging()
    
    entry = {
        "timestamp": str(datetime.now()),
        "message": message,
        "emotion": emotion,
        "score": score,
        "lang": lang
    }

    # Add to current session's messages
    st.session_state.current_session["messages"].append(entry)
    
    # If in local environment, save to file
    if not is_cloud_environment():
        save_to_file(st.session_state.log_data)

def get_log_data():
    """Get log data from the appropriate source"""
    if "log_data" not in st.session_state:
        initialize_logging()
    return st.session_state.log_data.get("sessions", [])

# Initialize logging system when the module is imported
initialize_logging()
