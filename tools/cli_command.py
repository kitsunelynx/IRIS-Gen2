from core.tools.tool_interface import ToolInterface, ToolContext
from typing import List, Callable
import subprocess

class CommandTool(ToolInterface):
    @property
    def name(self) -> str:
        return "CommandTool"

    def register(self, context: ToolContext) -> List[Callable]:
        context.success("Registering CommandTool tools.")

        def execute_command_tool(command: str) -> str:
            context.success(f"Executing command: {command}")
            try:
                result = subprocess.check_output(
                    command, shell=True, stderr=subprocess.STDOUT, text=True
                )
                context.success(f"Command output: {result}")
                return result
            except Exception as e:
                context.error(f"Error executing command: {e}")
                return f"Error: {e}"

        return [execute_command_tool]

def register():
    try:
        return CommandTool()
    except Exception as e:
        from core.utils.logger import get_logger
        get_logger().error(f"Error during command_tool registration: {e}")
        return None 