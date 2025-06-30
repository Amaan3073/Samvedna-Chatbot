# translator.py
from deep_translator import GoogleTranslator
import re

def clean_repetitive_text(text):
    """
    Clean repetitive words and phrases from text
    """
    # Split into words
    words = text.split()
    cleaned_words = []
    prev_word = None
    repetition_count = 0
    
    for word in words:
        if word == prev_word:
            repetition_count += 1
            if repetition_count > 2:  # Allow max 2 repetitions
                continue
        else:
            repetition_count = 0
        cleaned_words.append(word)
        prev_word = word
    
    return ' '.join(cleaned_words)

def is_hinglish(text):
    """
    Detect if text contains both Latin and Devanagari scripts
    """
    has_latin = bool(re.search(r'[a-zA-Z]', text))
    has_devanagari = bool(re.search(r'[\u0900-\u097F]', text))
    return has_latin and has_devanagari

def translate_response(text, target_lang):
    """
    Translate text between English and Hindi, with support for Hinglish.
    :param text: Text to translate
    :param target_lang: Target language code ('en' for English, 'hi' for Hindi)
    :return: Translated text
    """
    if not text:  # Handle empty text
        return text
    
    # Clean repetitive text first
    text = clean_repetitive_text(text)
    
    if target_lang == "hi":
        try:
            translated = GoogleTranslator(source='en', target='hi').translate(text)
            return translated
        except Exception as e:
            return f"(⚠️ Translation failed: {e})\n\n" + text
    elif target_lang == "en":
        try:
            # Handle Hinglish text
            if is_hinglish(text):
                # First translate the entire text to Hindi
                hindi_text = GoogleTranslator(source='en', target='hi').translate(text)
                # Then translate to English
                translated = GoogleTranslator(source='hi', target='en').translate(hindi_text)
                return translated
            # Only translate if the text appears to be in Hindi
            elif any(ord(char) >= 2304 and ord(char) <= 2431 for char in text):  # Unicode range for Devanagari
                translated = GoogleTranslator(source='hi', target='en').translate(text)
                return translated
            return text  # Return as is if not in Hindi
        except Exception as e:
            return f"(⚠️ Translation failed: {e})\n\n" + text
    else:
        return text  # Return original text for unsupported languages
