import pyttsx3
from core.utils.logger import get_logger

logger = get_logger()

class SimpleTTS:
    """
    A simple text-to-speech implementation using pyttsx3.
    """
    def __init__(self, config=None):
        """
        Initialize the SimpleTTS instance with optional configuration.
        """
        if config is None:
            config = {}
        self.engine = pyttsx3.init()

        # Retrieve available voices from the engine
        voices = self.engine.getProperty("voices")
        voice_target = config.get("voice", "IVONA 2 Salli - US English female voice [22kHz]")

        logger.info("Available voices:")
        for voice in voices:
            logger.info(f"{voice.name} - {voice.id}")

        # Select the configured voice if available
        for voice in voices:
            if voice_target.lower() in voice.name.lower():
                self.engine.setProperty("voice", voice.id)
                logger.success(f"Selected voice: {voice.name}")
                break
        else:
            logger.info(f"Voice '{voice_target}' not found. Using default voice.")

    def speak(self, text: str) -> None:
        """
        Convert the provided text to speech using pyttsx3.
        """
        self.engine.say(text)
        self.engine.runAndWait()