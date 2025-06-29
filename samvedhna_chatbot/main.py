from emotion_detector import detect_emotion
from translator import translate_response
from logger import log_message
from speech_input import listen_from_microphone
import json
import os
import re
from openai import OpenAI
from voice_output import speak, speak_sync

# ✅ OpenRouter-compatible OpenAI client
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

print("\nWelcome to Samvedna: Emotion-Aware Chat Assistant with Name Memory")
print("Type '/lang hi' for Hindi, '/lang en' for English, '/voice' to speak, '/clear' to reset history, '/mute' to silence, '/unmute' to enable TTS, or 'exit' to quit.\n")

lang = "english"
user_name = None
tts_enabled = True  # 🔇 Toggle for TTS
history_file = "chat_history.json"

chat_history = [
    {"role": "system", "content": "You are a helpful and empathetic assistant. If the user shares their name, remember it and use it in future replies. Otherwise reply normally without name. Adjust your tone gently based on the user's emotion if it is clearly expressed. Otherwise, respond neutrally and kindly."}
]

def save_chat_history():
    with open(history_file, "w") as f:
        json.dump(chat_history, f, indent=2)

def clear_chat_history():
    global chat_history, user_name
    chat_history = [
        {"role": "system", "content": "You are a helpful and empathetic assistant. If the user shares their name, remember it and use it in future replies. Otherwise reply normally without name. Adjust your tone gently based on the user's emotion if it is clearly expressed. Otherwise, respond neutrally and kindly."}
    ]
    user_name = None
    save_chat_history()
    print("Bot: Chat history has been cleared. Starting fresh.")
    if tts_enabled:
        speak("Chat history has been cleared. Starting fresh.", lang)

save_chat_history()

# --------------------- Name Extractor ---------------------
def extract_name(text):
    emotion_words = {
        "happy", "fine", "good", "okay", "great", "excited", "calm", "loved", "peaceful", "proud", "cheerful", "joyful", "optimistic",
        "confused", "unsure", "uncertain", "lost", "stuck", "puzzled",
        "sad", "depressed", "disappointed", "hurt", "lonely", "down", "heartbroken", "gloomy", "miserable", "hopeless",
        "angry", "frustrated", "mad", "upset", "annoyed", "furious", "irritated", "enraged",
        "scared", "afraid", "nervous", "anxious", "worried", "tense", "panicked",
        "tired", "sleepy", "exhausted", "drained", "burnt-out",
        "blank", "numb", "weird", "meh", "chill", "neutral", "overwhelmed"
    }
    patterns = [
        r"my name is ([A-Za-z]+)",
        r"i am ([A-Za-z]+)",
        r"i'm ([A-Za-z]+)",
        r"this is ([A-Za-z]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            name_candidate = match.group(1).lower()
            if name_candidate not in emotion_words:
                return name_candidate.capitalize()
    return None

# --------------------- LLM Response ---------------------
def get_llm_response(prompt, emotion):
    try:
        if user_name:
            prompt = f"My name is {user_name}. {prompt}"
        if emotion not in ["neutral", "greeting"]:
            user_message = f"[EMOTION: {emotion.upper()}]\n{prompt}"
        else:
            user_message = prompt

        chat_history.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=chat_history,
            temperature=0.7,
            max_tokens=200
        )

        reply = response.choices[0].message.content.strip()
        chat_history.append({"role": "assistant", "content": reply})
        save_chat_history()
        return reply
    except Exception as e:
        return f"❌ Error reaching OpenRouter: {e}"

# --------------------- Main Chat Loop ---------------------
while True:
    user_input = input("You (or type '/voice' to speak): ").strip()
    lowered_input = user_input.lower()

    if lowered_input == "exit":
        reply = "Take care! 😊"
        print("Bot:", reply)
        if tts_enabled:
            speak_sync(reply, lang)
        break

    if lowered_input == "/voice":
        speech_lang = "hi-IN" if lang == "hi" else "en-IN"
        user_input = listen_from_microphone(speech_lang)
        print(f"You(speak): {user_input}")
        lowered_input = user_input.lower()

    if lowered_input == "/lang hi":
        lang = "hi"
        reply = "भाषा हिंदी में बदल दी गई है।"
        print(f"Bot: {reply}")
        if tts_enabled:
            speak(reply, lang)
        continue

    elif lowered_input == "/lang en":
        lang = "english"
        reply = "Language switched to English."
        print(f"Bot: {reply}")
        if tts_enabled:
            speak(reply, lang)
        continue

    elif lowered_input == "/clear":
        clear_chat_history()
        continue

    elif lowered_input == "/mute":
        tts_enabled = False
        print("🔇 Bot is now muted.")
        continue

    elif lowered_input == "/unmute":
        tts_enabled = True
        print("🔊 Bot is now unmuted.")
        continue

    name = extract_name(user_input)
    if name:
        user_name = name
        reply = f"Nice to meet you, {user_name}!"
        print("Bot:", reply)
        if tts_enabled:
            speak(reply, lang)
        continue

    if lowered_input in ["i'm fine", "no i'm ok", "i'm okay", "i'm good"]:
        chat_history.append({"role": "user", "content": "Reset emotion context."})

    emotion, score = detect_emotion(user_input)
    log_message(user_input, emotion, score, lang)
    llm_reply = get_llm_response(user_input, emotion)
    translated_reply = translate_response(llm_reply, lang)

    print("Bot:", translated_reply)
    if tts_enabled:
        speak(translated_reply, lang)
