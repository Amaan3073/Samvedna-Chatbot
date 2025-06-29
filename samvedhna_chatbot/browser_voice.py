import streamlit as st
import streamlit.components.v1 as components

def init_voice_features():
    """Initialize browser-based voice features"""
    components.html(
        """
        <script>
        // Global variables
        let synth = null;
        let recognition = null;
        let isListening = false;
        let voices = [];

        // Initialize speech synthesis
        function initSpeechSynthesis() {
            try {
                synth = window.speechSynthesis;
                if (!synth) {
                    console.error('Speech synthesis not supported');
                    return false;
                }

                // Load voices
                voices = synth.getVoices();
                if (voices.length === 0) {
                    // Wait for voices to load
                    synth.onvoiceschanged = () => {
                        voices = synth.getVoices();
                        console.log('Voices loaded:', voices.length);
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
                    console.error('Speech recognition not supported');
                    return false;
                }
                recognition = new SpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = true;
                return true;
            } catch (error) {
                console.error('Speech recognition initialization error:', error);
                return false;
            }
        }

        // Function to speak text
        function speakText(text, lang) {
            return new Promise((resolve, reject) => {
                try {
                    if (!synth) {
                        if (!initSpeechSynthesis()) {
                            throw new Error('Could not initialize speech synthesis');
                        }
                    }

                    // Cancel any ongoing speech
                    synth.cancel();

                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
                    
                    // Find appropriate voice
                    const availableVoices = synth.getVoices();
                    const voice = availableVoices.find(v => v.lang === utterance.lang) || 
                                availableVoices.find(v => v.lang.startsWith(lang === 'hi' ? 'hi' : 'en')) ||
                                availableVoices[0];
                    if (voice) {
                        utterance.voice = voice;
                    }

                    // Set up event handlers
                    utterance.onstart = () => {
                        console.log('Started speaking');
                    };
                    
                    utterance.onend = () => {
                        console.log('Finished speaking');
                        resolve();
                    };
                    
                    utterance.onerror = (event) => {
                        console.error('Speech synthesis error:', event);
                        reject(event);
                    };

                    synth.speak(utterance);
                } catch (error) {
                    console.error('Error in speakText:', error);
                    reject(error);
                }
            });
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
                    const transcript = Array.from(event.results)
                        .map(result => result[0].transcript)
                        .join(' ');
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
            console.log('Initializing voice features...');
            const synthInitialized = initSpeechSynthesis();
            const recognitionInitialized = initSpeechRecognition();
            console.log('Voice features initialized:', {
                synthesis: synthInitialized,
                recognition: recognitionInitialized
            });
        });

        // Listen for messages from Streamlit
        window.addEventListener('message', function(event) {
            console.log('Received message:', event.data);
            switch (event.data.type) {
                case 'speak':
                    speakText(event.data.text, event.data.lang)
                        .catch(error => console.error('Speech failed:', error));
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
    components.html(
        f"""
        <script>
        // Send the speak message
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