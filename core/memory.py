import os
import json
import datetime

class MemoryManager:
    def __init__(self, memory_file: str = None):
        if memory_file is None:
            self.memory_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'memory.json')
        else:
            self.memory_file = memory_file
        self.memory = self.load_memory()

    def load_memory(self) -> dict:
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    return data
                else:
                    return {}
            except Exception:
                return {}
        else:
            return {}

    def save_memory(self) -> None:
        data_dir = os.path.dirname(self.memory_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    def set(self, key: str, value: str) -> None:
        self.memory[key] = value
        self.save_memory()

    def get(self, key: str) -> str:
        return self.memory.get(key, "")

    def append(self, content: str) -> str:
        key = "memory_" + datetime.datetime.now().isoformat()
        self.set(key, content)
        return key 