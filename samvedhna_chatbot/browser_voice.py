import streamlit as st
import streamlit.components.v1 as components

def init_voice_features():
    """Initialize browser-based voice features"""
    components.html(
        """
        <script>
        // Initialize speech synthesis
        const synth = window.speechSynthesis;
        
        // Initialize speech recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            console.error('Speech recognition not supported');
        }
        
        // Listen for messages from Streamlit
        window.addEventListener('message', function(event) {
            if (event.data.type === 'speak') {
                const utterance = new SpeechSynthesisUtterance(event.data.text);
                utterance.lang = event.data.lang === 'hi' ? 'hi-IN' : 'en-US';
                synth.speak(utterance);
            }
        });
        </script>
        """,
        height=0
    )

def speak_browser(text: str, lang: str = 'english'):
    """Speak text using browser's speech synthesis"""
    components.html(
        f"""
        <script>
        window.parent.postMessage({{
            type: 'speak',
            text: {repr(text)},
            lang: {repr('hi' if lang == 'hi' else 'en')}
        }}, '*');
        </script>
        """,
        height=0
    )

def listen_browser(lang: str = 'english'):
    """Start browser-based speech recognition"""
    transcript_container = st.empty()
    
    components.html(
        f"""
        <div>
            <button onclick="startListening()" style="display: none;">Start</button>
        </div>
        <script>
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = {repr('hi-IN' if lang == 'hi' else 'en-US')};
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onresult = (event) => {{
            const transcript = event.results[0][0].transcript;
            window.parent.Streamlit.setComponentValue(transcript);
        }};
        
        recognition.onerror = (event) => {{
            console.error('Speech recognition error:', event.error);
            window.parent.Streamlit.setComponentValue('ERROR: ' + event.error);
        }};
        
        // Start recognition automatically
        recognition.start();
        </script>
        """,
        height=0
    )
    
    return transcript_container 