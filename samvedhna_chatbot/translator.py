# translator.py
from deep_translator import GoogleTranslator

def translate_response(text, target_lang):
    if target_lang == "hi":
        try:
            translated = GoogleTranslator(source='auto', target='hi').translate(text)
            return translated
        except Exception as e:
            return f"(⚠️ Translation failed: {e})\n\n" + text
    else:
        return text
