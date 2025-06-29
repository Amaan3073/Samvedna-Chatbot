import streamlit as st
import streamlit.components.v1 as components

def init_voice_features():
    """Initialize browser-based voice features"""
    components.html(
        """
        <div id="voice-status"></div>
        <script>
        // Global variables
        let synth = null;
        let recognition = null;
        let isListening = false;
        let voices = [];

        // Update status display
        function updateStatus(message, isError = false) {
            const status = document.getElementById('voice-status');
            if (status) {
                status.textContent = message;
                status.style.color = isError ? 'red' : 'green';
                status.style.marginBottom = '10px';
                console.log(message);
            }
        }

        // Check browser compatibility
        function checkBrowserCompatibility() {
            if (!window.speechSynthesis) {
                updateStatus('Speech synthesis not supported in this browser', true);
                return false;
            }
            if (!window.SpeechRecognition && !window.webkitSpeechRecognition) {
                updateStatus('Speech recognition not supported in this browser', true);
                return false;
            }
            return true;
        }

        // Request microphone permission
        async function requestMicrophonePermission() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                stream.getTracks().forEach(track => track.stop()); // Stop the stream after permission check
                updateStatus('Microphone permission granted');
                return true;
            } catch (error) {
                updateStatus('Microphone permission denied: ' + error.message, true);
                return false;
            }
        }

        // Initialize speech synthesis
        async function initSpeechSynthesis() {
            try {
                if (!window.speechSynthesis) {
                    updateStatus('Speech synthesis not supported', true);
                    return false;
                }

                synth = window.speechSynthesis;

                // Load voices
                voices = synth.getVoices();
                if (voices.length === 0) {
                    // Wait for voices to load
                    return new Promise((resolve) => {
                        window.speechSynthesis.onvoiceschanged = () => {
                            voices = synth.getVoices();
                            console.log('Voices loaded:', voices.length);
                            updateStatus('Speech synthesis initialized with ' + voices.length + ' voices');
                            resolve(true);
                        };
                    });
                }
                updateStatus('Speech synthesis initialized with ' + voices.length + ' voices');
                return true;
            } catch (error) {
                updateStatus('Speech synthesis initialization error: ' + error.message, true);
                return false;
            }
        }

        // Initialize speech recognition
        function initSpeechRecognition() {
            try {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    updateStatus('Speech recognition not supported', true);
                    return false;
                }
                recognition = new SpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.maxAlternatives = 1;
                updateStatus('Speech recognition initialized');
                return true;
            } catch (error) {
                updateStatus('Speech recognition initialization error: ' + error.message, true);
                return false;
            }
        }

        // Function to speak text
        function speakText(text, lang) {
            return new Promise(async (resolve, reject) => {
                try {
                    if (!synth) {
                        const initialized = await initSpeechSynthesis();
                        if (!initialized) {
                            throw new Error('Could not initialize speech synthesis');
                        }
                    }

                    // Cancel any ongoing speech
                    synth.cancel();

                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
                    utterance.rate = 1.0;
                    utterance.pitch = 1.0;
                    utterance.volume = 1.0;
                    
                    // Find appropriate voice
                    const availableVoices = synth.getVoices();
                    const voice = availableVoices.find(v => v.lang === utterance.lang) || 
                                availableVoices.find(v => v.lang.startsWith(lang === 'hi' ? 'hi' : 'en')) ||
                                availableVoices[0];
                    if (voice) {
                        utterance.voice = voice;
                        console.log('Using voice:', voice.name);
                    }

                    // Set up event handlers
                    utterance.onstart = () => {
                        updateStatus('Speaking...');
                    };
                    
                    utterance.onend = () => {
                        updateStatus('Finished speaking');
                        resolve();
                    };
                    
                    utterance.onerror = (event) => {
                        updateStatus('Speech synthesis error: ' + event.error, true);
                        reject(event);
                    };

                    synth.speak(utterance);
                } catch (error) {
                    updateStatus('Error in speakText: ' + error.message, true);
                    reject(error);
                }
            });
        }

        // Function to start listening
        async function startListening(lang) {
            try {
                // Check browser compatibility first
                if (!checkBrowserCompatibility()) {
                    return;
                }

                // Request microphone permission
                const permissionGranted = await requestMicrophonePermission();
                if (!permissionGranted) {
                    return;
                }

                if (!recognition) {
                    if (!initSpeechRecognition()) {
                        throw new Error('Could not initialize speech recognition');
                    }
                }

                recognition.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
                
                recognition.onstart = () => {
                    isListening = true;
                    updateStatus('Listening...');
                    window.parent.Streamlit.setComponentValue('');
                };

                recognition.onresult = (event) => {
                    const transcript = Array.from(event.results)
                        .map(result => result[0].transcript)
                        .join(' ');
                    window.parent.Streamlit.setComponentValue(transcript);
                    updateStatus('Transcribing...');
                };

                recognition.onerror = (event) => {
                    updateStatus('Recognition error: ' + event.error, true);
                    window.parent.Streamlit.setComponentValue('ERROR: ' + event.error);
                    isListening = false;
                };

                recognition.onend = () => {
                    if (isListening) {
                        // Restart if we're still supposed to be listening
                        try {
                            recognition.start();
                            updateStatus('Restarting recognition...');
                        } catch (error) {
                            updateStatus('Error restarting recognition: ' + error.message, true);
                            isListening = false;
                        }
                    } else {
                        updateStatus('Stopped listening');
                    }
                };

                recognition.start();
            } catch (error) {
                updateStatus('Error in startListening: ' + error.message, true);
                window.parent.Streamlit.setComponentValue('ERROR: ' + error.message);
            }
        }

        // Function to stop listening
        function stopListening() {
            try {
                if (recognition) {
                    isListening = false;
                    recognition.stop();
                    updateStatus('Stopping recognition...');
                }
            } catch (error) {
                updateStatus('Error in stopListening: ' + error.message, true);
            }
        }

        // Initialize features when the page loads
        window.addEventListener('load', async () => {
            updateStatus('Initializing voice features...');
            
            // Check browser compatibility
            if (!checkBrowserCompatibility()) {
                return;
            }

            // Initialize features
            const synthInitialized = await initSpeechSynthesis();
            const recognitionInitialized = initSpeechRecognition();
            
            updateStatus('Voice features initialized: ' + 
                        'synthesis=' + (synthInitialized ? 'yes' : 'no') + ', ' +
                        'recognition=' + (recognitionInitialized ? 'yes' : 'no'));
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
        height=50  # Increased height to show status messages
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