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

        // Update status display and notify Streamlit
        function updateStatus(message, isError = false) {
            const status = document.getElementById('voice-status');
            if (status) {
                status.textContent = message;
                status.style.color = isError ? 'red' : 'green';
                status.style.marginBottom = '10px';
                console.log(message);
            }
            // Send status to Streamlit
            if (window.parent.Streamlit) {
                window.parent.Streamlit.setComponentValue({
                    type: 'status',
                    message: message,
                    isError: isError
                });
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
                        let attempts = 0;
                        const maxAttempts = 10;
                        const checkVoices = () => {
                            voices = synth.getVoices();
                            if (voices.length > 0) {
                                updateStatus('Speech synthesis initialized with ' + voices.length + ' voices');
                                resolve(true);
                            } else if (attempts < maxAttempts) {
                                attempts++;
                                setTimeout(checkVoices, 500);
                            } else {
                                updateStatus('No voices available after multiple attempts', true);
                                resolve(false);
                            }
                        };
                        window.speechSynthesis.onvoiceschanged = checkVoices;
                        checkVoices();
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
                    console.log('Available voices:', availableVoices.map(v => ({name: v.name, lang: v.lang})));
                    
                    const voice = availableVoices.find(v => v.lang === utterance.lang) || 
                                availableVoices.find(v => v.lang.startsWith(lang === 'hi' ? 'hi' : 'en')) ||
                                availableVoices[0];
                    
                    if (voice) {
                        utterance.voice = voice;
                        console.log('Using voice:', voice.name, voice.lang);
                        updateStatus('Using voice: ' + voice.name + ' (' + voice.lang + ')');
                    } else {
                        console.log('No suitable voice found, using default');
                        updateStatus('No suitable voice found, using default');
                    }

                    // Set up event handlers
                    utterance.onstart = () => {
                        updateStatus('Speaking...');
                        console.log('Speech started');
                    };
                    
                    utterance.onend = () => {
                        updateStatus('Finished speaking');
                        console.log('Speech ended');
                        resolve();
                    };
                    
                    utterance.onerror = (event) => {
                        const errorMsg = 'Speech synthesis error: ' + event.error;
                        updateStatus(errorMsg, true);
                        console.error(errorMsg);
                        reject(event);
                    };

                    console.log('Starting speech...');
                    synth.speak(utterance);
                } catch (error) {
                    const errorMsg = 'Error in speakText: ' + error.message;
                    updateStatus(errorMsg, true);
                    console.error(errorMsg);
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
                console.log('Recognition language set to:', recognition.lang);
                
                recognition.onstart = () => {
                    isListening = true;
                    updateStatus('Listening...');
                    console.log('Recognition started');
                    window.parent.Streamlit.setComponentValue({
                        type: 'transcript',
                        text: ''
                    });
                };

                recognition.onresult = (event) => {
                    const transcript = Array.from(event.results)
                        .map(result => result[0].transcript)
                        .join(' ');
                    console.log('Transcript:', transcript);
                    window.parent.Streamlit.setComponentValue({
                        type: 'transcript',
                        text: transcript
                    });
                    updateStatus('Transcribing...');
                };

                recognition.onerror = (event) => {
                    const errorMsg = 'Recognition error: ' + event.error;
                    updateStatus(errorMsg, true);
                    console.error(errorMsg);
                    window.parent.Streamlit.setComponentValue({
                        type: 'transcript',
                        text: 'ERROR: ' + event.error
                    });
                    isListening = false;
                };

                recognition.onend = () => {
                    if (isListening) {
                        // Restart if we're still supposed to be listening
                        try {
                            recognition.start();
                            updateStatus('Restarting recognition...');
                            console.log('Recognition restarted');
                        } catch (error) {
                            const errorMsg = 'Error restarting recognition: ' + error.message;
                            updateStatus(errorMsg, true);
                            console.error(errorMsg);
                            isListening = false;
                        }
                    } else {
                        updateStatus('Stopped listening');
                        console.log('Recognition stopped');
                    }
                };

                console.log('Starting recognition...');
                recognition.start();
            } catch (error) {
                const errorMsg = 'Error in startListening: ' + error.message;
                updateStatus(errorMsg, true);
                console.error(errorMsg);
                window.parent.Streamlit.setComponentValue({
                    type: 'transcript',
                    text: 'ERROR: ' + error.message
                });
            }
        }

        // Function to stop listening
        function stopListening() {
            try {
                if (recognition) {
                    isListening = false;
                    recognition.stop();
                    updateStatus('Stopping recognition...');
                    console.log('Recognition stop requested');
                }
            } catch (error) {
                const errorMsg = 'Error in stopListening: ' + error.message;
                updateStatus(errorMsg, true);
                console.error(errorMsg);
            }
        }

        // Initialize features when the page loads
        window.addEventListener('load', async () => {
            updateStatus('Initializing voice features...');
            console.log('Voice features initialization started');
            
            // Check browser compatibility
            if (!checkBrowserCompatibility()) {
                return;
            }

            // Initialize features
            const synthInitialized = await initSpeechSynthesis();
            const recognitionInitialized = initSpeechRecognition();
            
            const status = 'Voice features initialized: ' + 
                        'synthesis=' + (synthInitialized ? 'yes' : 'no') + ', ' +
                        'recognition=' + (recognitionInitialized ? 'yes' : 'no');
            updateStatus(status);
            console.log(status);
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