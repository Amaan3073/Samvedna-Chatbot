# speech_input.py
import speech_recognition as sr

def listen_from_microphone(language="en-IN"):
    recognizer = sr.Recognizer()

    # Reduce false triggers
    recognizer.energy_threshold = 400  # Adjust if too sensitive
    recognizer.pause_threshold = 0.8   # Seconds of silence = stop listening
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("🎤 Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            text = recognizer.recognize_google(audio, language=language)  # type: ignore
            return text.strip()
        except sr.WaitTimeoutError:
            print("⚠️ No speech detected (timeout).")
        except sr.UnknownValueError:
            print("⚠️ Sorry, I didn't catch that.")
        except sr.RequestError:
            print("⚠️ Network error.")
        return None
