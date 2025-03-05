from core.config.config_manager import ConfigManager
from core.utils.tts.simple_tts import SimpleTTS
from core.utils.tts.advanced_tts import speak as advanced_speak, init_pipeline
from core.utils.logger import get_logger

logger = get_logger()

def get_tts():
    config = ConfigManager().config
    advanced_enabled = config.get("tts_config", {}).get("advanced_tts_enabled", False)
    logger.success(f"advanced_tts_enabled from config: {advanced_enabled}")
    if advanced_enabled:
        # Use advanced TTS based on configuration
        lang = config.get("tts_config", {}).get("advanced_tts_lang", "a")
        init_pipeline(lang_code=lang)

        class AdvancedTTS:
            def speak(self, text: str):
                voice = config.get("tts_config", {}).get("advanced_tts_voice", "af_heart")
                speed = config.get("tts_config", {}).get("advanced_tts_speed", 1)
                logger.success(f"AdvancedTTS speaking with voice: {voice}, speed: {speed}")
                advanced_speak(text, voice=voice, speed=speed)
        logger.success("Returning AdvancedTTS")
        return AdvancedTTS()
    else:
        logger.success("Returning SimpleTTS")
        return SimpleTTS() 