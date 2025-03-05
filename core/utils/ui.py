from rich.console import Console
from rich.panel import Panel
import speech_recognition as sr
from core.utils.tts import get_tts
from core.utils.logger import get_logger

class UIHandler:
    STYLE_MAPPING = {
        "info": "cyan",
        "error": "bold red",
        "success": "green",
        "warning": "bold yellow",
    }

    def __init__(self):
        self.logger = get_logger()
        self.console = Console()
        self.tts = get_tts()

    def print_message(self, message: str, style: str = None, panel_title: str = None):
        rich_style = self.STYLE_MAPPING.get(style, style)
        if panel_title:
            self.console.print(Panel(message, title=panel_title, style=rich_style, expand=False))
        else:
            self.console.print(message, style=rich_style)

    def get_input(self, prompt: str = "> ") -> str:
        return input(prompt)

    def get_voice_input(self, timeout: int = 7, retries: int = 3) -> str:
        recognizer = sr.Recognizer()
        for attempt in range(1, retries + 1):
            try:
                with sr.Microphone() as source:
                    self.print_message("Voice Input: Please speak now...", style="info")
                    audio = recognizer.listen(source, timeout=timeout)
                    text = recognizer.recognize_google(audio)
                    self.print_message(f"You (voice): {text}", style="success")
                    return text
            except Exception as e:
                self.logger.error(f"Voice input error on attempt {attempt}: {e}")
        return ""

    def speak(self, text: str):
        try:
            self.tts.speak(text)
        except Exception as e:
            self.logger.error(f"TTS speak error: {e}") 