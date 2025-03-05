import os
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import asyncio
from core.agents.iris_agent import IRISAgent
from core.utils.logger import get_logger
from core.tools.tool_manager import ToolManager
from core.utils.ui import UIHandler
from core.config.config_manager import ConfigManager
from core.utils.error_handler import handle_errors

load_dotenv()
logger = get_logger()

@dataclass
class ChatEntry:
    timestamp: str
    user: str
    response: str

@dataclass
class ChatLog:
    chat_history: list = field(default_factory=list)
    reminders: list = field(default_factory=list)
    last_interaction: datetime = None

    def reset(self):
        self.chat_history.clear()
        self.reminders.clear()

class IRISCore:
    def __init__(self, ui_handler: UIHandler = None):
        self.logger = get_logger()
        self.ui = ui_handler if ui_handler else UIHandler()
        self.logger.success("Starting IRIS...")
        self.logger.success("Loading configuration...")
        self.config = ConfigManager()

        self.logger.success("Loading chat log...")
        self.chatlog = self._load_chatlog()

        # Initialize memory as an empty list for IRISAgent's usage.
        self.memory = []

        # Load system prompt from all files in the data directory (.id is preferred, .txt as fallback)
        system_prompt = self._load_system_prompt()
        self.logger.success("System prompt loaded.")

        self.logger.success("Loading web search module...")

        self.logger.success("Loading tools...")
        self.tool_manager = ToolManager()
        tools = self.tool_manager.load_tools()

        integrated_tools = [
            self.add_reminder,
            self.remove_reminder,
            self.get_current_datetime,
            self.store_memory,
            self.write_persistent_memory,
            self.read_persistent_memory,
        ]
        all_tools = tools + integrated_tools

        self.logger.success("Loading TTS module...")
        from core.utils.tts import get_tts
        self.tts = get_tts()

        self.logger.success("Loading agent...")
        self.agent = IRISAgent(system_prompt, None, self.config.config, tools=all_tools)

        self.voice_mode = self.config.get("default_voice_mode", False)
        self.tts_enabled = self.config.get("default_tts_enabled", False)

        self.logger.success("Starting background tasks...")
        self._start_background_tasks()

    def _load_system_prompt(self) -> str:
        data_dir = Path("data")
        sysdt_files = sorted(data_dir.glob("*.id"))
        if sysdt_files:
            system_prompt = "\n".join(f.read_text(encoding="utf-8") for f in sysdt_files)
        else:
            txt_files = sorted(data_dir.glob("*.txt"))
            system_prompt = "\n".join(f.read_text(encoding="utf-8") for f in txt_files) if txt_files else "Default system prompt."
        return system_prompt


    @handle_errors(default_return=ChatLog())
    def _load_chatlog(self) -> ChatLog:
        chatlog_path = "data/chatlog.json"
        if not os.path.exists(chatlog_path):
            return ChatLog()
        with open(chatlog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("chat_history", [])
        data.setdefault("reminders", [])
        if data.get("last_interaction"):
            data["last_interaction"] = datetime.fromisoformat(data["last_interaction"])
        else:
            data["last_interaction"] = None
        data["chat_history"] = [ChatEntry(**entry) for entry in data["chat_history"]]
        return ChatLog(**data)

    def _start_background_tasks(self):
        import threading

        # Start a synchronous thread for checking reminders
        thread = threading.Thread(target=self._reminder_checker_sync, daemon=True)
        thread.start()

    def _reminder_checker_sync(self):
        from datetime import datetime
        import time
        while True:
            now = datetime.now()
            due_reminders = []
            for reminder in list(self.chatlog.reminders):
                due_date_str = reminder.get("due_date")
                if due_date_str:
                    try:
                        due_date = datetime.fromisoformat(due_date_str)
                        if now >= due_date:
                            due_reminders.append(reminder)
                    except Exception as e:
                        self.logger.error(f"Error parsing reminder due_date: {e}")
            for reminder in due_reminders:
                message = f"Reminder: {reminder.get('text')} (Due: {reminder.get('due_date')})"
                self.ui.print_message(message, style="warning")
            time.sleep(60)

    def add_reminder(self, reminder_name: str, reminder_text: str, due_date: str) -> str:
        from datetime import datetime
        try:
            parsed_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
        except Exception as e:
            return f"Error parsing date: {e}"
        new_reminder = {
            "name": reminder_name,
            "text": reminder_text,
            "due_date": parsed_date.isoformat(),
            "created_at": datetime.now().isoformat()
        }
        self.chatlog.reminders.append(new_reminder)
        self._save_chatlog()
        self.logger.success(f"Reminder '{reminder_name}' set: {reminder_text} at {due_date}")
        return f"Reminder '{reminder_name}' set: {reminder_text} at {due_date}"

    @handle_errors(default_return="Error removing reminder")
    def remove_reminder(self, reminder_name: str) -> str:
        found = False
        for r in self.chatlog.reminders:
            if r.get("name") == reminder_name:
                self.chatlog.reminders.remove(r)
                found = True
                break
        self._save_chatlog()
        if found:
            return f"Removed reminder '{reminder_name}'."
        else:
            return f"No reminder found with the name '{reminder_name}'."

    def get_current_datetime(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()

    @handle_errors(default_return=None)
    def store_memory(self, content: str) -> None:
        # Use the new persistent memory module (core/memory.py) to store content with a timestamp key
        from core.memory import append_to_memory
        import datetime
        key = "memory_" + datetime.datetime.now().isoformat()
        append_to_memory(key, content)

    @handle_errors(default_return="Error writing persistent memory")
    def write_persistent_memory(self, key: str, value: str) -> str:
        from core.memory import append_to_memory
        append_to_memory(key, value)
        return f"Persistent memory written for key: {key}"

    @handle_errors(default_return="Error reading persistent memory")
    def read_persistent_memory(self, key: str) -> str:
        from core.memory import read_from_memory
        data = read_from_memory()
        return data.get(key, "")

    def _save_chatlog(self):
        try:
            chatlog_dict = {
                "chat_history": [entry.__dict__ for entry in self.chatlog.chat_history],
                "reminders": self.chatlog.reminders,
                "last_interaction": self.chatlog.last_interaction.isoformat() if self.chatlog.last_interaction else None,
            }
            chatlog_path = Path("data/chatlog.json")
            chatlog_path.parent.mkdir(exist_ok=True)
            chatlog_path.write_text(json.dumps(chatlog_dict, indent=2), encoding="utf-8")
        except Exception as e:
            self.logger.error(f"Chat log Save Error: {e}")

    def run(self):
        self.logger.success("IRISCore running. Type 'exit' or 'quit' to close the program.")
        while True:
            try:
                user_input = self.ui.get_input("IRIS> ")
            except KeyboardInterrupt:
                self.logger.success("Keyboard interrupt detected. Exiting IRISCore gracefully...")
                break

            command = user_input.strip().lower()
            if command in ("exit", "quit"):
                self.logger.success("Exiting IRISCore...")
                break

            # Handle TTS toggle commands
            if command == "/tts on":
                self.tts_enabled = True
                self.ui.print_message("Text-to-speech enabled.", style="info")
                continue
            elif command == "/tts off":
                self.tts_enabled = False
                self.ui.print_message("Text-to-speech disabled.", style="info")
                continue

            if not user_input.strip():
                continue

            response = self.agent.send_message(user_input)
            self.ui.print_message(response, style="info")
            if self.tts_enabled:
                self.tts.speak(response)