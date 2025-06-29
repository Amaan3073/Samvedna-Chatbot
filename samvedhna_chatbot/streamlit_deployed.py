# Place at the top of the file
import streamlit as st
from emotion_detector import detect_emotion
from translator import translate_response
from logger import log_message
from openai import OpenAI
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import altair as alt
import os
import ssl
from typing import List, Dict, Any, Optional, Union
from openai.types.chat import ChatCompletionMessageParam
import tempfile

# --- File Operations ---
def get_log_path():
    """Get the path to the log file, using temporary directory in cloud"""
    return os.path.join(st.session_state.temp_dir, 'conversation_log.json')

def save_log_data(data):
    """Save log data to file"""
    try:
        log_path = get_log_path()
        with open(log_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.warning(f"Failed to save log data: {str(e)}")

def load_log_data():
    """Load log data from file"""
    try:
        log_path = get_log_path()
        if os.path.exists(log_path):
            with open(log_path) as f:
                return json.load(f)
    except Exception:
        pass
    return {"sessions": []}

def update_conversation_log(user_input: str, emotion: str, score: float, lang: str):
    """Update the conversation log with new message"""
    try:
        log_data = load_log_data()
        
        # Get current session or create new one
        if not log_data["sessions"] or len(log_data["sessions"][-1]["messages"]) > 50:
            log_data["sessions"].append({
                "start_time": datetime.now().isoformat(),
                "messages": []
            })
        
        # Add message to current session
        current_session = log_data["sessions"][-1]
        current_session["messages"].append({
            "text": user_input,
            "emotion": emotion,
            "score": score,
            "lang": lang,
            "timestamp": datetime.now().isoformat()
        })
        
        # Save updated log data
        save_log_data(log_data)
        
    except Exception as e:
        st.warning(f"Failed to update conversation log: {str(e)}")

# --- SSL Certificate Fix ---
# Set SSL certificate path or disable verification for development
try:
    # Try to use system certificates
    ssl_context = ssl.create_default_context()
except:
    # If that fails, disable SSL verification (for development only)
    os.environ['SSL_CERT_FILE'] = ''
    os.environ['REQUESTS_CA_BUNDLE'] = ''

# --- Streamlit page config
st.set_page_config(
    page_title="Samvedna",
    page_icon="🧠",
    layout="wide"
)

# --- Custom CSS Styling (Gradient Background & Bubbles) ---
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
        }

        body {
            background: linear-gradient(to bottom right, #0f0c29, #302b63, #24243e);
            color: #ffffff;
        }

        .stApp {
            background: linear-gradient(to bottom right, #0f0c29, #302b63, #24243e) !important;
        }

        .block-container {
            background: transparent !important;
        }

        .stSidebar {
            background: linear-gradient(to bottom, #1e1e2f, #2a2a40) !important;
            color: white;
        }

        .chat-message {
            border-radius: 16px;
            padding: 14px 20px;
            margin-bottom: 12px;
            max-width: 100%;
            width: fit-content;
            font-size: 15px;
            word-wrap: break-word;
            line-height: 1.5;
        }

        .chat-user {
            background: linear-gradient(145deg, #3a3d5c, #2c2f45);
            color: #e0e7ff;
            align-self: flex-end;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }

        .chat-bot {
            background: linear-gradient(145deg, #2b2e44, #1e2033);
            color: #f5f7fa;
            align-self: flex-start;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }

        .chat-container {
            display: flex;
            flex-direction: column;
        }

        h1 {
            font-size: 2.2rem;
            color: #a78bfa !important;
            font-weight: 700;
        }

        .stCaption {
            font-size: 0.9rem;
            color: #e0e7ff;
        }

        .stSidebar h2, .stSidebar h3, .stSidebar label {
            color: #e0e7ff;
        }

        div[data-testid="stChatInput"] {
            background: linear-gradient(to top left, #0f0c29, #302b63, #24243e) !important;
                padding: 3% 10% 4% 10%;
                border-radius: 0 !important;
                margin: -3% -10% -8% -11%;
        }


        .stChatInputContainer textarea {
            background-color: #1f1f2e !important;
            color: #ffffff !important;
            border: 1px solid #6b7280 !important;
            border-radius: 12px !important;
            font-size: 16px !important;
        }

        .stChatInputContainer button {
            background-color: #4b5563 !important;
            color: white !important;
            border: none !important;
        }

        .stDownloadButton > button {
            width: 100%;
            text-align: left !important;
        }

        @media only screen and (max-width: 768px) {
            h1 {
                font-size: 1.5rem !important;
            }
            h2 {
                font-size: 1.3rem !important;
            }
            .chat-message {
                font-size: 14px !important;
                padding: 10px 14px !important;
            }

            .stChatInputContainer textarea {
                font-size: 14px !important;
            }
            div[data-testid="stChatInput"] {
                background: linear-gradient(to top left, #0f0c29, #302b63, #24243e) !important;
                padding: 1.5rem 4rem 2rem 4rem;
                border-radius: 0 !important;
                margin: -1rem -4rem -4rem -4rem;
            }
        }
        .st-emotion-cache-se9ihy {
            background: transparent;
            color: #e0e7ff; 
        }
        .st-av {
            background-color: #7d58eb;
        }
        .st-emotion-cache-umot6g:hover {
            border-color: #7d58eb;
            color: #7d58eb;
        }
    </style>
""", unsafe_allow_html=True)


# --- OpenRouter client setup ---
try:
    client = OpenAI(
        api_key=st.secrets["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1"
    )
except Exception as e:
    st.error(f"Error initializing OpenAI client: {str(e)}")
    st.info("Please check your API key configuration in .streamlit/secrets.toml")
    client = None

# --- Session State Init ---
for key, default in {
    "chat_history": [],
    "lang": "english",
    "user_name": None,
    "show_emotion_analysis": False,
    "temp_dir": tempfile.mkdtemp()  # Create a temporary directory for file operations
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Sidebar Settings ---
with st.sidebar:
    st.header("⚙️ Chat Settings")

    lang = st.radio("🌐 Language", ["English", "Hindi"])
    st.session_state.lang = "hi" if lang == "Hindi" else "english"

    if st.button("🎙️ Speak"):
        st.info("🔔 Voice input/output features are only available in the local version.")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.user_name = None
        st.success("✅ Chat cleared")

    if st.session_state.chat_history:
        def format_history():
            return "\n".join([
                f"🧑 You: {u}\n🤖 Bot: {b}\n" for u, b in st.session_state.chat_history
            ])
        st.download_button("⬇️ Download Chat History", format_history(), file_name="chat_history.txt")

    st.session_state.show_emotion_analysis = st.checkbox("📊 Show Chat Analysis", value=st.session_state.show_emotion_analysis)

# --- Input Handler ---
def extract_name(text: str) -> Optional[str]:
    emotion, _ = detect_emotion(text)
    if emotion in ["happy", "sad", "confused", "angry", "greeting"]:
        return None
    for pattern in [r"my name is ([A-Za-z]+)", r"i am ([A-Za-z]+)", r"i'm ([A-Za-z]+)", r"this is ([A-Za-z]+)"]:
        match = re.search(pattern, text.lower())
        if match:
            name = match.group(1).capitalize()
            st.session_state.user_name = name
            return name
    return None

# --- Main Title
st.markdown("<h1 style='color:#FF69B4;'>🧠 Samvedna – Emotion-Aware Chatbot</h1>", unsafe_allow_html=True)
st.caption("Empathetic multilingual chatbot powered by Emotion Detection + LLM")

# --- User Input Box
user_input = st.chat_input("Type your message...")

# --- Chat Logic
if user_input:
    extract_name(user_input)
    emotion, score = detect_emotion(user_input)
    update_conversation_log(user_input, emotion, score, st.session_state.lang)

    prompt = user_input
    if st.session_state.user_name:
        prompt = f"My name is {st.session_state.user_name}. {prompt}"
    if emotion not in ["neutral", "greeting"]:
        prompt = f"[EMOTION: {emotion.upper()}]\n{prompt}"

    messages: List[ChatCompletionMessageParam] = [
        {"role": "system", "content": "You are a helpful and empathetic assistant named Samvedhna created by Amaan Ali. If the user shares their name, remember it and use it in future replies.Otherwise reply normally without name. Adjust your tone gently based on the user's emotion if it is clearly expressed. Otherwise, respond neutrally and kindly."}
    ]
    for u, b in st.session_state.chat_history:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": b})
    messages.append({"role": "user", "content": prompt})

    try:
        if client is None:
            st.error("❌ OpenAI client not initialized. Please check your API configuration.")
            reply = "I'm sorry, but I'm having trouble connecting to my AI service. Please check your API key configuration."
        else:
            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=messages,
                temperature=0.7,
                max_tokens=200
            )
            message_content = response.choices[0].message.content
            reply = message_content.strip() if message_content else "I'm sorry, I couldn't generate a response."
        
        translated = translate_response(reply, st.session_state.lang)
        st.session_state.chat_history.append((user_input, translated))
            
    except Exception as e:
        st.error(f"❌ Error generating response: {str(e)}")
        error_reply = "I'm sorry, but I encountered an error while processing your request. Please try again."
        st.session_state.chat_history.append((user_input, error_reply))

# --- Chat Display (dynamic & reversed)
if not st.session_state.show_emotion_analysis:
    for user_msg, bot_msg in st.session_state.chat_history:
        with st.container():
            st.markdown(f"<div class='chat-container'><div class='chat-message chat-user'>{user_msg}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-container'><div class='chat-message chat-bot'>{bot_msg}</div></div>", unsafe_allow_html=True)

# 📊 Emotion Analysis Section
if st.session_state.show_emotion_analysis:
    try:
        from collections import Counter
        from datetime import datetime

        def get_log_data() -> List[Dict[str, Any]]:
            try:
                log_path = get_log_path()  # Use the same path as update_conversation_log
                if os.path.exists(log_path):
                    with open(log_path) as f:
                        return json.load(f).get("sessions", [])
            except:
                return []
            return []

        def get_emotion_timeline() -> pd.DataFrame:
            sessions = get_log_data()
            if not sessions:
                return pd.DataFrame(data=[], columns=["Time", "Emotion"])  # type: ignore
            messages = sessions[-1]["messages"]
            data = []
            for msg in messages:
                if msg.get("emotion") not in ["neutral", "greeting"] and "timestamp" in msg:
                    try:
                        time = datetime.fromisoformat(msg["timestamp"])
                        data.append({"Time": time, "Emotion": msg["emotion"]})
                    except:
                        continue
            return pd.DataFrame(data)

        def get_pie() -> Counter[str]:
            trend_df = get_emotion_timeline()
            return Counter(trend_df["Emotion"].tolist())

        def mood_scores() -> tuple[List[str], List[float]]:
            score_map = {"happy": 3, "confused": 1, "neutral": 0, "greeting": 0, "sad": -2, "angry": -3}
            sessions = get_log_data()
            labels, scores = [], []
            for i, session in enumerate(sessions):
                mood = [score_map.get(m["emotion"], 0) for m in session.get("messages", [])]
                if mood:
                    labels.append(f"Session {i+1}")
                    scores.append(round(sum(mood) / len(mood), 2))
            return labels, scores

        def session_time() -> tuple[float, float]:
            sessions = get_log_data()
            times = []
            for s in sessions:
                msgs = s.get("messages", [])
                if len(msgs) > 1:
                    try:
                        start = datetime.fromisoformat(msgs[0]["timestamp"])
                        end = datetime.fromisoformat(msgs[-1]["timestamp"])
                        times.append((end - start).total_seconds() / 60)
                    except:
                        continue
            if not times:
                return 0.0, 0.0
            current = times[-1]
            average = sum(times[:-1]) / len(times[:-1]) if len(times) > 1 else 0.0
            return round(current, 2), round(average, 2)

        if not st.session_state.chat_history:
            st.warning("❗ No chat history found. Please start a conversation to view analysis.")
        else:
            st.markdown("## 📈 Emotion Trend Over Time (Current Session)")
            timeline_df = get_emotion_timeline()
            if not timeline_df.empty:
                chart = alt.Chart(timeline_df).mark_line(point=True).encode(  # type: ignore
                    x=alt.X("Time:T", axis=alt.Axis(title="Timestamp")),  # type: ignore
                    y=alt.Y("Emotion:N", axis=alt.Axis(title="Emotion")),  # type: ignore
                    tooltip=["Time", "Emotion"]  # type: ignore
                ).properties(  # type: ignore
                    width=700,
                    height=300,
                    title="Emotion Timeline"
                )
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Not enough data for emotion trend.")

            st.markdown("## 🥧 Emotion Distribution (Current Session)")
            pie = get_pie()
            if pie:
                fig1, ax1 = plt.subplots(figsize=(6, 3))
                ax1.pie(list(pie.values()), labels=list(pie.keys()), autopct="%1.1f%%", startangle=90, textprops={'fontsize': 9})
                ax1.axis("equal")
                st.pyplot(fig1, use_container_width=False)
            else:
                st.info("No emotion data available for pie chart.")

            st.markdown("## 📊 Mood Score Comparison (All Sessions)")
            labels, scores = mood_scores()
            if scores:
                fig2, ax2 = plt.subplots(figsize=(6, 3))
                bars = ax2.bar(labels, scores, color="skyblue", width=0.5)
                if bars:
                    bars[-1].set_color("royalblue")
                ax2.axhline(0, color="gray", linestyle="--")
                ax2.set_ylabel("Mood Score")
                ax2.set_title("Average Mood per Session")
                st.pyplot(fig2)
            else:
                st.info("No mood score data available.")

            st.markdown("## ⏱️ Session Duration Comparison (minutes)")
            curr, avg = session_time()
            if curr > 0:
                duration_df = pd.DataFrame({
                    "Current Session": [curr],
                    "Avg of Previous": [avg]
                })
                st.bar_chart(duration_df)
            else:
                st.info("Insufficient data for session duration.")

    except Exception as e:
        st.error(f"⚠️ Error while loading chat analysis: {str(e)}")

# Footer
st.markdown("---")
st.caption("Built with ❤️ by Amaan Ali")