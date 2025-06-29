# translator.py
from deep_translator import GoogleTranslator

def translate_response(text, target_lang):
    """
    Translate text between English and Hindi.
    :param text: Text to translate
    :param target_lang: Target language code ('en' for English, 'hi' for Hindi)
    :return: Translated text
    """
    if not text:  # Handle empty text
        return text
        
    if target_lang == "hi":
        try:
            translated = GoogleTranslator(source='en', target='hi').translate(text)
            return translated
        except Exception as e:
            return f"(⚠️ Translation failed: {e})\n\n" + text
    elif target_lang == "en":
        try:
            # Only translate if the text appears to be in Hindi
            if any(ord(char) >= 2304 and ord(char) <= 2431 for char in text):  # Unicode range for Devanagari
                translated = GoogleTranslator(source='hi', target='en').translate(text)
                return translated
            return text  # Return as is if not in Hindi
        except Exception as e:
            return f"(⚠️ Translation failed: {e})\n\n" + text
    else:
        return text  # Return original text for unsupported languages
