# Samvedhna - Emotion-Aware Chatbot 🧠

Samvedhna is an empathetic multilingual chatbot powered by Emotion Detection and Large Language Models. It provides a unique conversational experience by understanding and responding to users' emotions in both English and Hindi.

## 🌐 Live Demo

**Try the hosted version:** [https://samvedna-chatbot.streamlit.app/](https://samvedna-chatbot.streamlit.app/)

## Features 🌟

- **Emotion Detection**: Analyzes user messages to detect emotions and adapts responses accordingly
- **Multilingual Support**: Communicates in both English and Hindi
- **Voice Interaction**: Supports both voice input and output (local version only)
- **Real-time Chat Analysis**: Provides visual analytics of emotion trends and chat patterns
- **Beautiful UI**: Modern gradient-based interface with chat bubbles
- **Session Management**: Tracks conversation history and provides downloadable chat logs
- **Cloud Deployment**: Hosted version available with cloud-optimized features
- **Conversation Logging**: Automatic logging of conversations with emotion tracking

## Tech Stack 💻

- **Frontend**: Streamlit
- **Language Model**: Mistral-7b-instruct via OpenRouter
- **Translation**: Deep Translator
- **Voice Features**: gTTS, speech_recognition, pyttsx3
- **Analytics**: Pandas, Matplotlib, Altair
- **Emotion Analysis**: Custom NLP implementation
- **Cloud Deployment**: Streamlit Cloud

## Installation 🚀

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/Amaan3073/Samvedna-Chatbot.git
cd Samvedna-Chatbot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
Create a `.streamlit/secrets.toml` file with:
```toml
OPENROUTER_API_KEY = "your-api-key-here"
```

5. Run the application:
```bash
streamlit run samvedhna_chatbot/streamlit_app.py
```

### Cloud Deployment

The application is also available as a hosted version with cloud-optimized features:

- **Voice features disabled** (cloud limitations)
- **Temporary file storage** for conversation logs
- **Session-based analytics** (current session only)
- **Optimized for cloud environment**

## Usage 🎯

### Local Version Features

1. **Starting a Chat**:
   - Type your message in the chat input
   - Or click the "Speak" button to use voice input

2. **Language Selection**:
   - Choose between English and Hindi from the sidebar
   - Toggle voice output on/off as needed

3. **Chat Analysis**:
   - Enable "Show Chat Analysis" in the sidebar
   - View emotion trends, distribution, and session statistics
   - Compare current session with previous sessions

4. **Managing History**:
   - Download chat history using the sidebar button
   - Clear chat to start a fresh conversation

### Cloud Version Features

1. **Text-based Chat**: Full chat functionality with emotion detection
2. **Current Session Analytics**: View emotion trends and patterns for current session
3. **Conversation Logging**: Automatic logging of all conversations
4. **Download Chat History**: Export current conversation

## Project Structure 📁

```
samvedhna_chatbot/
├── streamlit_app.py        # Main application file (local version)
├── streamlit_deployed.py   # Cloud-optimized version
├── emotion_detector.py     # Emotion analysis implementation
├── translator.py          # Language translation utilities
├── speech_input.py       # Voice input processing
├── voice_output.py      # Text-to-speech functionality
├── logger.py           # Logging utilities
├── main.py            # Command-line interface
├── responses.py       # Response templates
├── requirements.txt   # Project dependencies
├── tts_cache/        # Text-to-speech cache directory
└── .streamlit/       # Streamlit configuration
```

## Key Differences: Local vs Cloud Version

| Feature | Local Version | Cloud Version |
|---------|---------------|---------------|
| Voice Input | ✅ Available | ❌ Disabled |
| Voice Output | ✅ Available | ❌ Disabled |
| Session Comparison | ✅ All sessions | ❌ Current only |
| File Persistence | ✅ Permanent | ❌ Temporary |
| Advanced Analytics | ✅ Full features | ⚠️ Limited |

## Dependencies 📦

- **streamlit==1.46.0**: Web framework
- **openai==1.88.0**: OpenAI API client
- **deep-translator==1.11.4**: Translation services
- **nltk==3.9.1**: Natural language processing
- **gtts==2.5.4**: Google Text-to-Speech
- **pyttsx3==2.98**: Offline text-to-speech
- **SpeechRecognition==3.10.0**: Speech recognition
- **pandas==2.2.3**: Data manipulation
- **matplotlib==3.8.2**: Plotting
- **altair==4.2.2**: Interactive charts

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Author ✨

Built with ❤️ by Amaan Ali

## Acknowledgments 🙏

- OpenRouter for providing LLM API access
- Streamlit for the amazing web framework
- The open-source community for various tools and libraries 