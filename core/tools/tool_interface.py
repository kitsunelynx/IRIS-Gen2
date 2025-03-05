from abc import ABC, abstractmethod
from typing import List, Callable
from core.tools.tool_context import ToolContext

class ToolInterface(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the tool."""
        pass

    @abstractmethod
    def register(self, context: ToolContext) -> List[Callable]:
        """
        Register the tool with the provided limited context.
        """
        pass 