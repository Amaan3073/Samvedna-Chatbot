# Samvedhna - Emotion-Aware Chatbot 🧠

Samvedhna is an empathetic multilingual chatbot powered by Emotion Detection and Large Language Models. It provides a unique conversational experience by understanding and responding to users' emotions in both English and Hindi.

## Features 🌟

- **Emotion Detection**: Analyzes user messages to detect emotions and adapts responses accordingly
- **Multilingual Support**: Communicates in both English and Hindi
- **Voice Interaction**: Supports both voice input and output
- **Real-time Chat Analysis**: Provides visual analytics of emotion trends and chat patterns
- **Beautiful UI**: Modern gradient-based interface with chat bubbles
- **Session Management**: Tracks conversation history and provides downloadable chat logs

## Tech Stack 💻

- **Frontend**: Streamlit
- **Language Model**: Mistral-7b-instruct via OpenRouter
- **Translation**: Deep Translator
- **Voice Features**: gTTS, speech_recognition
- **Analytics**: Pandas, Matplotlib, Altair
- **Emotion Analysis**: Custom NLP implementation

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/yourusername/samvedhna-chatbot.git
cd samvedhna-chatbot
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

## Usage 🎯

1. **Starting a Chat**:
   - Type your message in the chat input
   - Or click the "Speak" button to use voice input

2. **Language Selection**:
   - Choose between English and Hindi from the sidebar
   - Toggle voice output on/off as needed

3. **Chat Analysis**:
   - Enable "Show Chat Analysis" in the sidebar
   - View emotion trends, distribution, and session statistics

4. **Managing History**:
   - Download chat history using the sidebar button
   - Clear chat to start a fresh conversation

## Project Structure 📁

```
samvedhna_chatbot/
├── streamlit_app.py      # Main application file
├── emotion_detector.py   # Emotion analysis implementation
├── translator.py        # Language translation utilities
├── speech_input.py     # Voice input processing
├── voice_output.py    # Text-to-speech functionality
├── logger.py         # Logging utilities
└── requirements.txt  # Project dependencies
```

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