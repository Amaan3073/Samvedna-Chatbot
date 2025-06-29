from typing import Optional
from googletrans import Translator

def translate_response(text: str, target_lang: str = "english") -> str:
    """
    Translate text to target language.
    
    Args:
        text (str): Text to translate
        target_lang (str): Target language code ("english" or "hi")
        
    Returns:
        str: Translated text
    """
    try:
        if not text:
            return text
            
        # If target is English, no translation needed
        if target_lang == "english":
            return text
            
        # Initialize translator
        translator = Translator()
        
        # Translate to Hindi
        if target_lang == "hi":
            result = translator.translate(text, dest='hi')
            return result.text if result else text
            
        return text
        
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text  # Return original text on error 