import re
import sounddevice as sd
from kokoro import KPipeline

# Eagerly initialize the global pipeline instance at module import
_pipeline = KPipeline(lang_code='a')

def init_pipeline(lang_code: str = 'a') -> KPipeline:
    # Since pipeline is already initialized, simply return it.
    return _pipeline

def speak(
    text: str, 
    voice: str = 'af_heart', 
    speed: float = 1.0, 
    sample_rate: int = 24000,
    split_pattern: str = r'\n+'
) -> None:
    """
    Generate and play speech from text using advanced TTS.
    
    Parameters:
      text: The text to speak.
      voice: The identifier of the voice to use.
      speed: Playback speed.
      sample_rate: Sampling rate for playback.
      split_pattern: Pattern to split the text for processing.
    """
    pipeline = init_pipeline()  # Use default lang_code from config as 'a' (American English)
    generator = pipeline(text, voice=voice, speed=speed, split_pattern=split_pattern)
    for i, (gs, ps, audio) in enumerate(generator):
        sd.play(audio, sample_rate)
        sd.wait()

