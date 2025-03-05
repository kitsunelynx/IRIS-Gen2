import json
import os

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config file: {e}")
                return {}
        else:
            return self._default_config()

    def _default_config(self) -> dict:
        return {
            "model": "gemini-2.0-flash",
            "generate_config": {
                "top_p": 0.6,
                "top_k": 64,
                "temperature": 64,
                "automatic_function_calling_disable": False,
                "seed": 42
            },
            "tts_type": "simple",
            "default_voice_mode": False,
            "default_tts_enabled": False
        }

    def get(self, key, default=None):
        return self.config.get(key, default) 