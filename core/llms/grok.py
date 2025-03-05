import os
from grokit import Grokit
from dotenv import load_dotenv
from core.utils.logger import get_logger

load_dotenv()
logger = get_logger()

class Grok:
    def __init__(self, system_prompt, memory=None):
        """
        Initialize the Grok agent with a system prompt and optional memory reference.
        
        Parameters:
            system_prompt (str): The system prompt guiding Grok's responses.
            memory: Optional memory or chat log reference.

        """
        auth_token = os.environ.get("GROKIT_AUTH_TOKEN")
        csrf_token = os.environ.get("GROKIT_CSRF_TOKEN")
        if not auth_token or not csrf_token:
            raise ValueError("GROKIT_AUTH_TOKEN or GROKIT_CSRF_TOKEN not set")
        self.grok = Grokit(auth_token=auth_token, csrf_token=csrf_token)
        self.system_prompt = system_prompt
        self.memory = memory

    def _format_conversation_history(self, max_entries=5):
        history = ""
        if self.memory:
            for entry in self.memory.chat_history[-max_entries:]:
                history += f"User: {entry.user}\nIRIS: {entry.response}\n"
        return history

    def grok_response(self, message: str):
        try:
            history = self._format_conversation_history() if self.memory else ""
            full_prompt = f"<s>{self.system_prompt}</s>\n{history}User: {message}\nIRIS: "
            response = self.grok.generate(full_prompt, model_id="grok-3")
            return response
        except Exception as e:
            logger.error("Error generating response with Grok")
            return f"Grok error: {str(e)}"

#ga = Grok("You are ")
#print(ga.generate_response("Introduce yourself"))