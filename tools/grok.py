"""
GrokTool - A tool for processing queries via a simple text transformation.
This tool implements the ToolInterface and registers a 'grok' function that performs
a basic transformation on the input query (in this case, reversing the string) as a placeholder for more advanced analysis.
"""
import os
from typing import List, Callable
from core.tools.tool_interface import ToolInterface  # Refactored naming
from core.tools.tool_context import ToolContext      # Refactored naming
from grokit import Grokit

auth_token = os.environ.get("GROKIT_AUTH_TOKEN")
csrf_token = os.environ.get("GROKIT_CSRF_TOKEN")
grok = Grokit(auth_token=auth_token, csrf_token=csrf_token)

class GrokTool(ToolInterface):
    @property
    def name(self) -> str:
        return "GrokTool"

    def register(self, context: ToolContext) -> List[Callable]:
        context.success("Registering GrokTool.")

        def grok(query: str) -> str:
            context.info(f"Performing Grok analysis for: {query}")
            result = grok.generate(query, model='grok-3')
            context.success("Grok analysis completed.")
            return f"Grok result: {result}"
        
        return [grok]

def register():
    try:
        return GrokTool()
    except Exception as e:
        from core.utils.logger import get_logger
        get_logger().error(f"Error during grok_tool registration: {e}")
        return None
