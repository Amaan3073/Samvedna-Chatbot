import streamlit as st
import streamlit.components.v1 as components

def init_voice_features():
    """Initialize browser-based voice features"""
    components.html(
        """
        <script>
        // Speech synthesis setup
        const synth = window.speechSynthesis;
        
        // Speech recognition setup
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        
        // Function to speak text
        function speakText(text, lang) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
            synth.speak(utterance);
        }
        
        // Function to start listening
        function startListening(lang) {
            recognition.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
            recognition.start();
            
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                window.parent.postMessage({type: 'speech-input', value: transcript}, '*');
            };
            
            recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                window.parent.postMessage({type: 'speech-error', value: event.error}, '*');
            };
        }
        
        // Listen for messages from Streamlit
        window.addEventListener('message', function(event) {
            if (event.data.type === 'speak') {
                speakText(event.data.text, event.data.lang);
            } else if (event.data.type === 'listen') {
                startListening(event.data.lang);
            }
        });
        </script>
        <div id="voice-status"></div>
        """,
        height=0,
    )

def speak_browser(text: str, lang: str = 'english'):
    """Speak text using browser's speech synthesis"""
    # Send message to browser to speak text
    st.components.v1.html(
        f"""
        <script>
        window.parent.postMessage({{
            type: 'speak',
            text: {repr(text)},
            lang: {repr('hi' if lang == 'hi' else 'en')}
        }}, '*');
        </script>
        """,
        height=0,
    )

def listen_browser(lang: str = 'english'):
    """Start browser-based speech recognition"""
    # Create a container for the transcript
    transcript_placeholder = st.empty()
    
    # Send message to browser to start listening
    components.html(
        f"""
        <script>
        window.parent.postMessage({{
            type: 'listen',
            lang: {repr('hi' if lang == 'hi' else 'en')}
        }}, '*');
        
        // Listen for transcript from recognition
        window.addEventListener('message', function(event) {{
            if (event.data.type === 'speech-input') {{
                window.parent.postMessage({{
                    type: 'update-transcript',
                    value: event.data.value
                }}, '*');
            }}
        }});
        </script>
        """,
        height=0,
    )
    
    return transcript_placeholder 