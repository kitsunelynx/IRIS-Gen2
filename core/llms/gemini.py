import os
from google import genai
from dotenv import load_dotenv
from core.utils.logger import get_logger

# Load environment variables

load_dotenv()

class Gemini:
    def __init__(self, model_name, config):
        """
        Initialize the Gemini agent using the Gemini API.

        Parameters:
            model_name (str): The identifier for the Gemini model to use (e.g., "gemini-2.0-flash").
            config (dict): Configuration options for text generation, including system_instruction and tools.
        """
        self.logger = get_logger()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in the environment.")
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        # Create a clean copy of the config removing any extra keys not accepted by GenerateContentConfig.
        self.config = config.copy() if config else {}
        # Create a chat session with the given model and configuration.
        self.chat = self.client.chats.create(model=model_name, config=self.config)
        # Add status tracking
        self.current_status = None
        self.status_callback = None

    def set_status_callback(self, callback):
        """Set a callback function to be called when status changes"""
        self.status_callback = callback

    def update_status(self, status):
        """Update the current status and call the callback if set"""
        self.current_status = status
        if self.status_callback:
            self.status_callback(status)

    def send_message(self, message: str) -> str:
        """
        Sends a message to Gemini using the chat conversation API and returns the generated text.

        Parameters:
            message (str): The user's input message.

        Returns:
            str: The generated response text from Gemini.
        """
        try:
            
            # Send the message to Gemini
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            self.logger.error(f"Error sending message via Gemini: {e}", exc_info=True)
            return f"Error sending message via Gemini: {str(e)}"

    def reset_chat(self):
        """
        Resets the chat conversation by creating a new chat session.
        """
        try:
            self.chat = self.client.chats.create(model=self.model_name, config=self.config)
            self.logger.success("Gemini chat session reset successfully.")
        except Exception as e:
            self.logger.error(f"Error resetting Gemini chat session: {e}", exc_info=True)
