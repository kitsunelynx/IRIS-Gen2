from pathlib import Path
from datetime import datetime

class Memory:
    def __init__(self, file_path: str = "data/memory.sysdt"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(exist_ok=True, parents=True)

    def append(self, content: str) -> None:
        timestamp = datetime.now().isoformat()
        try:
            with self.file_path.open('a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {content}\n")
        except Exception as e:
            raise Exception(f"Error appending to memory file: {e}")

    def read(self) -> str:
        if self.file_path.exists():
            return self.file_path.read_text()
        return ""