import streamlit as st
import streamlit.components.v1 as components
import uuid

def init_voice_features():
    """Initialize browser-based voice features"""
    components.html(
        """
        <script>
        // Initialize speech synthesis
        let synth = window.speechSynthesis;
        let recognition = null;
        
        // Function to handle speech synthesis
        function speakText(text, lang) {
            if (synth.speaking) {
                synth.cancel();
            }
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
            synth.speak(utterance);
        }

        // Listen for messages from Streamlit
        window.addEventListener('message', function(event) {
            if (event.data.type === 'speak') {
                speakText(event.data.text, event.data.lang);
            }
        });
        </script>
        """,
        height=0
    )

def speak_browser(text: str, lang: str = 'english'):
    """Speak text using browser's speech synthesis"""
    # Generate a unique key for this component
    key = f"speak_{str(uuid.uuid4())}"
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
    # Create a container for the transcript
    transcript_container = st.empty()
    
    # Generate a unique key for this component
    key = f"listen_{str(uuid.uuid4())}"
    
    # Create a component to handle speech recognition
    components.html(
        f"""
        <script>
        // Function to handle speech recognition messages
        function setupSpeechRecognition() {{
            try {{
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {{
                    window.parent.Streamlit.setComponentValue('ERROR: Speech recognition not supported in this browser');
                    return;
                }}

                const recognition = new SpeechRecognition();
                recognition.lang = {repr('hi-IN' if lang == 'hi' else 'en-US')};
                recognition.continuous = false;
                recognition.interimResults = true;

                recognition.onresult = (event) => {{
                    const transcript = event.results[0][0].transcript;
                    window.parent.Streamlit.setComponentValue(transcript);
                }};

                recognition.onerror = (event) => {{
                    console.error('Speech recognition error:', event.error);
                    window.parent.Streamlit.setComponentValue('ERROR: ' + event.error);
                }};

                recognition.onend = () => {{
                    // Restart recognition if still listening
                    if (window.isListening) {{
                        recognition.start();
                    }}
                }};

                window.isListening = true;
                recognition.start();
            }} catch (error) {{
                console.error('Error setting up speech recognition:', error);
                window.parent.Streamlit.setComponentValue('ERROR: ' + error.message);
            }}
        }}

        // Start speech recognition when the component loads
        setupSpeechRecognition();
        </script>
        """,
        height=0
    )
    
    return transcript_container 