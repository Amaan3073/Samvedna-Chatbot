import streamlit as st
import streamlit.components.v1 as components

def init_voice_features():
    """Initialize browser-based voice features"""
    components.html(
        """
        <script>
        // Initialize speech synthesis
        let synth = window.speechSynthesis;
        let recognition = null;
        let isListening = false;

        // Function to handle speech synthesis
        function speakText(text, lang) {
            try {
                if (synth.speaking) {
                    synth.cancel();
                }
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
                synth.speak(utterance);
            } catch (error) {
                console.error('Speech synthesis error:', error);
            }
        }

        // Function to handle speech recognition
        function setupRecognition(lang) {
            try {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    throw new Error('Speech recognition not supported in this browser');
                }

                recognition = new SpeechRecognition();
                recognition.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
                recognition.continuous = false;
                recognition.interimResults = true;

                recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript;
                    window.parent.Streamlit.setComponentValue(transcript);
                };

                recognition.onerror = (event) => {
                    console.error('Speech recognition error:', event.error);
                    window.parent.Streamlit.setComponentValue('ERROR: ' + event.error);
                    isListening = false;
                };

                recognition.onend = () => {
                    if (isListening) {
                        recognition.start();
                    }
                };

                return recognition;
            } catch (error) {
                console.error('Error setting up speech recognition:', error);
                window.parent.Streamlit.setComponentValue('ERROR: ' + error.message);
                return null;
            }
        }

        // Listen for messages from Streamlit
        window.addEventListener('message', function(event) {
            if (event.data.type === 'speak') {
                speakText(event.data.text, event.data.lang);
            } else if (event.data.type === 'start-listen') {
                try {
                    if (!recognition) {
                        recognition = setupRecognition(event.data.lang);
                    }
                    if (recognition) {
                        isListening = true;
                        recognition.start();
                    }
                } catch (error) {
                    console.error('Error starting recognition:', error);
                    window.parent.Streamlit.setComponentValue('ERROR: ' + error.message);
                }
            } else if (event.data.type === 'stop-listen') {
                try {
                    if (recognition) {
                        isListening = false;
                        recognition.stop();
                    }
                } catch (error) {
                    console.error('Error stopping recognition:', error);
                }
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
    # Create a container for the transcript
    transcript_container = st.empty()
    
    # Send message to start listening
    components.html(
        f"""
        <script>
        window.parent.postMessage({{
            type: 'start-listen',
            lang: {repr('hi' if lang == 'hi' else 'en')}
        }}, '*');
        </script>
        """,
        height=0
    )
    
    return transcript_container 