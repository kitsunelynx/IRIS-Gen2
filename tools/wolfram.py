import os
import wolframalpha
from core.utils.logger import get_logger
from core.tools.tool_interface import ToolInterface, ToolContext
from typing import List, Callable

logger = get_logger()

class WolframTool(ToolInterface):
    @property
    def name(self) -> str:
        return "WolframTool"

    def register(self, context: ToolContext) -> List[Callable]:
        context.success("Registering WolframTool tools.")

        def query_wolfram_alpha(query: str) -> str:
            context.success(f"Querying Wolfram Alpha for: {query}")
            try:
                app_id = os.environ.get("WOLFRAM_APP_ID")
                if not app_id:
                    raise ValueError("WOLFRAM_APP_ID is not set in the environment.")
                client = wolframalpha.Client(app_id)
                res = client.query(query)
                result_text = ""
                for pod in res.pods:
                    if pod.text:
                        result_text += f"{pod.title}:\n{pod.text}\n\n"
                if not result_text.strip():
                    result_text = "No results found."
                context.success("Wolfram query successful.")
                return result_text.strip()
            except Exception as e:
                context.error(f"Error querying Wolfram Alpha: {e}")
                return f"Error querying Wolfram Alpha: {e}"

        return [query_wolfram_alpha]

def register():
    try:
        return WolframTool()
    except Exception as e:
        logger.error(f"Error during wolfram_tool registration: {e}")
        return None 