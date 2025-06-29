import streamlit as st
import streamlit.components.v1 as components

def init_voice_features():
    """Initialize browser-based voice features"""
    components.html(
        """
        <div id="voice-status"></div>
        <script>
        // Initialize speech synthesis and recognition
        let synth = null;
        let recognition = null;
        let isListening = false;

        // Initialize speech synthesis
        function initSpeechSynthesis() {
            try {
                synth = window.speechSynthesis;
                // Load voices
                let voices = synth.getVoices();
                if (voices.length === 0) {
                    // Wait for voices to load
                    window.speechSynthesis.onvoiceschanged = () => {
                        voices = synth.getVoices();
                    };
                }
                return true;
            } catch (error) {
                console.error('Speech synthesis initialization error:', error);
                return false;
            }
        }

        // Initialize speech recognition
        function initSpeechRecognition() {
            try {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    throw new Error('Speech recognition not supported');
                }
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = true;
                return true;
            } catch (error) {
                console.error('Speech recognition initialization error:', error);
                return false;
            }
        }

        // Function to speak text
        function speakText(text, lang) {
            try {
                if (!synth) {
                    if (!initSpeechSynthesis()) {
                        throw new Error('Could not initialize speech synthesis');
                    }
                }

                // Cancel any ongoing speech
                if (synth.speaking) {
                    synth.cancel();
                }

                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
                
                // Set up event handlers
                utterance.onstart = () => {
                    console.log('Started speaking');
                };
                
                utterance.onend = () => {
                    console.log('Finished speaking');
                };
                
                utterance.onerror = (event) => {
                    console.error('Speech synthesis error:', event.error);
                };

                synth.speak(utterance);
            } catch (error) {
                console.error('Error in speakText:', error);
            }
        }

        // Function to start listening
        function startListening(lang) {
            try {
                if (!recognition) {
                    if (!initSpeechRecognition()) {
                        throw new Error('Could not initialize speech recognition');
                    }
                }

                recognition.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
                
                recognition.onstart = () => {
                    isListening = true;
                    console.log('Started listening');
                };

                recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript;
                    window.parent.Streamlit.setComponentValue(transcript);
                };

                recognition.onerror = (event) => {
                    console.error('Recognition error:', event.error);
                    window.parent.Streamlit.setComponentValue('ERROR: ' + event.error);
                    isListening = false;
                };

                recognition.onend = () => {
                    if (isListening) {
                        // Restart if we're still supposed to be listening
                        recognition.start();
                    }
                };

                recognition.start();
            } catch (error) {
                console.error('Error in startListening:', error);
                window.parent.Streamlit.setComponentValue('ERROR: ' + error.message);
            }
        }

        // Function to stop listening
        function stopListening() {
            try {
                if (recognition) {
                    isListening = false;
                    recognition.stop();
                }
            } catch (error) {
                console.error('Error in stopListening:', error);
            }
        }

        // Initialize features when the page loads
        window.addEventListener('load', () => {
            initSpeechSynthesis();
            initSpeechRecognition();
        });

        // Listen for messages from Streamlit
        window.addEventListener('message', function(event) {
            switch (event.data.type) {
                case 'speak':
                    speakText(event.data.text, event.data.lang);
                    break;
                case 'start-listen':
                    startListening(event.data.lang);
                    break;
                case 'stop-listen':
                    stopListening();
                    break;
            }
        });
        </script>
        """,
        height=0
    )

def speak_browser(text: str, lang: str = 'english'):
    """Speak text using browser's speech synthesis"""
    # Create a unique component for each speech request
    components.html(
        f"""
        <script>
        // Ensure we have the latest text
        const textToSpeak = {repr(text)};
        const langToUse = {repr('hi' if lang == 'hi' else 'en')};
        
        // Send the speak message
        window.parent.postMessage({{
            type: 'speak',
            text: textToSpeak,
            lang: langToUse
        }}, '*');
        </script>
        """,
        height=0
    )

def listen_browser(lang: str = 'english'):
    """Start browser-based speech recognition"""
    # Create a container for the transcript
    transcript_container = st.empty()
    
    # Create a unique component for the recognition request
    components.html(
        f"""
        <script>
        // Send the start-listen message
        window.parent.postMessage({{
            type: 'start-listen',
            lang: {repr('hi' if lang == 'hi' else 'en')}
        }}, '*');
        </script>
        """,
        height=0
    )
    
    return transcript_container 