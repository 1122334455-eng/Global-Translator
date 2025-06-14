from deep_translator import (
    GoogleTranslator,
    LibreTranslator,
    MyMemoryTranslator
)
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversationAssistant:
    def __init__(self):
        self.translation_services = [
            'google',
            'libre',
            'mymemory'
        ]
        self.current_service = 0  # Start with Google
        self.max_retries = 3

    def translate_text(self, text, source_lang, target_lang):
        last_error = None
        
        # Try all available services until one works
        for i in range(len(self.translation_services)):
            service = self.translation_services[(self.current_service + i) % len(self.translation_services)]
            
            try:
                if service == 'google':
                    logger.info(f"Trying Google Translate ({source_lang}→{target_lang})")
                    return GoogleTranslator(
                        source=source_lang,
                        target=target_lang
                    ).translate(text)
                    
                elif service == 'libre':
                    logger.info(f"Trying LibreTranslate ({source_lang}→{target_lang})")
                    api_key = os.getenv('LIBRE_API_KEY')
                    return LibreTranslator(
                        source=source_lang,
                        target=target_lang,
                        base_url='https://libretranslate.de',
                        api_key=api_key
                    ).translate(text)
                    
                elif service == 'mymemory':
                    logger.info(f"Trying MyMemory ({source_lang}→{target_lang})")
                    return MyMemoryTranslator(
                        source=source_lang,
                        target=target_lang
                    ).translate(text[:500])  # MyMemory has length limits
                    
            except Exception as e:
                last_error = e
                logger.warning(f"{service} failed: {str(e)}")
                continue
                
        # If all services failed
        error_msg = f"All translation services failed. Last error: {str(last_error)}"
        logger.error(error_msg)
        raise Exception(error_msg)