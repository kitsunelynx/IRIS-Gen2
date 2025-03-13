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

    def print_message(self, message: str, style: str = None, panel_title: str = None, sender: str = None, timestamp: str = None):
        from rich import box
        if sender:
            if timestamp:
                title = f"{sender} @ {timestamp}"
            else:
                title = sender
        else:
            title = panel_title
        if style is None:
            if sender == "You":
                rich_style = "bold blue"
            elif sender == "IRIS":
                rich_style = "green"
            elif sender == "System":
                rich_style = "magenta"
            else:
                rich_style = "cyan"
        else:
            rich_style = self.STYLE_MAPPING.get(style, style)
        self.console.print(Panel(message, title=title, style=rich_style, box=box.ROUNDED, expand=False))

    def get_input(self, prompt: str = "You: ") -> str:
        from rich.prompt import Prompt
        return Prompt.ask(prompt)

    def get_voice_input(self, timeout: int = 7, retries: int = 3) -> str:
        recognizer = sr.Recognizer()
        for attempt in range(1, retries + 1):
            try:
                with sr.Microphone() as source:
                    self.print_message("Voice Input: Please speak now...", style="info")
                    audio = recognizer.listen(source, timeout=timeout)
                    text = recognizer.recognize_google(audio)
                    self.print_message(f"You (voice): {text}", sender="You", timestamp="")
                    return text
            except Exception as e:
                self.logger.error(f"Voice input error on attempt {attempt}: {e}")
        return ""

    def speak(self, text: str):
        try:
            self.tts.speak(text)
        except Exception as e:
            self.logger.error(f"TTS speak error: {e}") 