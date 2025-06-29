responses = {
    "english": {
        "happy": "I'm glad to hear that! 😊",
        "confused": "Let me try to explain that better. Can you please clarify your question?",
        "sad": "I'm here for you. Let’s try to solve this together.",
        "greeting": "Hi there! How can I assist you today? 😊",
        "angry-low": "I understand this may be frustrating. Let's work through it together.",
        "angry-high": "I'm really sorry. This seems serious. I'm escalating this to a human agent now.",
        "neutral": "How can I assist you today?"
    },
    "hindi": {
        "happy": "यह सुनकर खुशी हुई! 😊",
        "confused": "कोई बात नहीं, मैं बेहतर तरीके से समझाने की कोशिश करता हूँ।",
        "sad": "मैं आपकी मदद के लिए यहाँ हूँ। चलिए मिलकर हल निकालते हैं।",
        "greeting": "नमस्ते! मैं आपकी किस प्रकार सहायता कर सकता हूँ? 😊",
        "angry-low": "मुझे खेद है कि आपको परेशानी हुई। चलिए इसे मिलकर हल करते हैं।",
        "angry-high": "मुझे वास्तव में खेद है। मैं इसे किसी एजेंट को सौंप रहा हूँ।",
        "neutral": "मैं आपकी कैसे सहायता कर सकता हूँ?"
    }
}

def get_response(emotion, lang="english", intensity=0):
    if emotion == "angry":
        return responses[lang]["angry-high"] if intensity < -0.75 else responses[lang]["angry-low"]
    return responses[lang].get(emotion, responses[lang]["neutral"])