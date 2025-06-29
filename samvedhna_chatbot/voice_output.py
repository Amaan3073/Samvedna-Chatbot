# voice_output.py

import os
import re
import uuid
import hashlib
import threading
from gtts import gTTS
from playsound import playsound

CACHE_DIR = "tts_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002700-\U000027BF"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def speak(text, lang='english'):
    def _speak_async():
        try:
            clean = remove_emojis(text)

            if lang == 'hi':
                lang_code = 'hi'
                hashed = hashlib.md5((clean + lang_code).encode()).hexdigest()
                file_path = os.path.join(CACHE_DIR, f"{hashed}.mp3")

                # Always regenerate to ensure deletion after
                tts = gTTS(text=clean, lang=lang_code)
                tts.save(file_path)

                playsound(file_path)
                os.remove(file_path)  # 🔥 Delete after playback

            else:
                import pyttsx3
                local_engine = pyttsx3.init()
                local_engine.setProperty('rate', 160)
                local_engine.setProperty('volume', 1.0)

                voices = local_engine.getProperty('voices')
                for voice in voices:
                    if 'english' in voice.name.lower():
                        local_engine.setProperty('voice', voice.id)
                        break

                local_engine.say(clean)
                local_engine.runAndWait()

        except Exception as e:
            print(f"❌ TTS Error (async): {e}")

    threading.Thread(target=_speak_async, daemon=True).start()

def speak_sync(text, lang='english'):
    try:
        clean = remove_emojis(text)

        if lang == 'hi':
            lang_code = 'hi'
            hashed = hashlib.md5((clean + lang_code).encode()).hexdigest()
            file_path = os.path.join(CACHE_DIR, f"{hashed}.mp3")

            tts = gTTS(text=clean, lang=lang_code)
            tts.save(file_path)

            playsound(file_path)
            os.remove(file_path)  # 🔥 Delete after playback

        else:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 160)
            engine.setProperty('volume', 1.0)

            voices = engine.getProperty('voices')
            for voice in voices:
                if 'english' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break

            engine.say(clean)
            engine.runAndWait()

    except Exception as e:
        print(f"❌ TTS Error (sync): {e}")
