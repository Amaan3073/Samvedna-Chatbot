import streamlit as st
import streamlit.components.v1 as components

def init_voice_features():
    """Initialize browser-based voice features"""
    components.html(
        """
        <script>
        // Speech synthesis setup
        let synth = null;
        let recognition = null;

        function initVoiceFeatures() {
            try {
                // Initialize speech synthesis
                synth = window.speechSynthesis;
                
                // Initialize speech recognition
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    throw new Error('Speech recognition not supported in this browser');
                }
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                
                // Set up recognition event handlers
                recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript;
                    window.parent.postMessage({
                        type: 'speech-input',
                        value: transcript
                    }, '*');
                };
                
                recognition.onerror = (event) => {
                    console.error('Speech recognition error:', event.error);
                    window.parent.postMessage({
                        type: 'speech-error',
                        value: event.error
                    }, '*');
                };

                recognition.onend = () => {
                    window.parent.postMessage({
                        type: 'speech-end'
                    }, '*');
                };

                return true;
            } catch (error) {
                console.error('Error initializing voice features:', error);
                window.parent.postMessage({
                    type: 'voice-init-error',
                    value: error.message
                }, '*');
                return false;
            }
        }

        // Function to speak text
        function speakText(text, lang) {
            try {
                if (!synth) {
                    throw new Error('Speech synthesis not initialized');
                }
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
                synth.speak(utterance);
            } catch (error) {
                console.error('Error speaking text:', error);
                window.parent.postMessage({
                    type: 'speak-error',
                    value: error.message
                }, '*');
            }
        }
        
        // Function to start listening
        function startListening(lang) {
            try {
                if (!recognition) {
                    throw new Error('Speech recognition not initialized');
                }
                recognition.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
                recognition.start();
            } catch (error) {
                console.error('Error starting speech recognition:', error);
                window.parent.postMessage({
                    type: 'listen-error',
                    value: error.message
                }, '*');
            }
        }

        // Function to stop listening
        function stopListening() {
            try {
                if (recognition) {
                    recognition.stop();
                }
            } catch (error) {
                console.error('Error stopping speech recognition:', error);
            }
        }
        
        // Initialize voice features when the page loads
        window.addEventListener('load', () => {
            initVoiceFeatures();
        });

        // Listen for messages from Streamlit
        window.addEventListener('message', function(event) {
            switch (event.data.type) {
                case 'speak':
                    speakText(event.data.text, event.data.lang);
                    break;
                case 'listen':
                    startListening(event.data.lang);
                    break;
                case 'stop-listen':
                    stopListening();
                    break;
            }
        });
        </script>
        <div id="voice-status"></div>
        """,
        height=0,
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
        height=0,
    )

def listen_browser(lang: str = 'english') -> str:
    """Start browser-based speech recognition"""
    result_placeholder = st.empty()
    
    components.html(
        f"""
        <script>
        let messageHandler = function(event) {{
            if (event.data.type === 'speech-input') {{
                const transcript = event.data.value;
                window.parent.postMessage({{
                    type: 'update-transcript',
                    value: transcript
                }}, '*');
            }} else if (event.data.type === 'speech-error') {{
                window.parent.postMessage({{
                    type: 'update-transcript',
                    value: '❌ Error: ' + event.data.value
                }}, '*');
            }} else if (event.data.type === 'speech-end') {{
                window.removeEventListener('message', messageHandler);
            }}
        }};
        
        window.addEventListener('message', messageHandler);
        
        window.parent.postMessage({{
            type: 'listen',
            lang: {repr('hi' if lang == 'hi' else 'en')}
        }}, '*');
        </script>
        """,
        height=0,
    )
    
    return result_placeholder 