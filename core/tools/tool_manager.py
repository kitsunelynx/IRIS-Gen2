from pathlib import Path
import importlib.util
import sys
from core.tools.tool_interface import ToolInterface
from core.tools.tool_context import ToolContext
from core.utils.logger import get_logger

logger = get_logger()

class ToolManager:
    def __init__(self):
        self.tools = []
        self.tool_dir = Path("tools")

    def load_tools(self) -> list:
        context = ToolContext(logger=get_logger(), config=None, ui=None)
        if not self.tool_dir.exists():
            logger.error("Tool directory does not exist.")
            return self.tools

        for tool_file in self.tool_dir.glob("*.py"):
            if tool_file.name == "__init__.py":
                continue
            spec = importlib.util.spec_from_file_location(tool_file.stem, str(tool_file))
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except Exception as inner_e:
                logger.error(f"Error executing module {tool_file.name}: {inner_e}")
                continue
            if hasattr(module, "register"):
                tool_instance = module.register()
                if isinstance(tool_instance, ToolInterface):
                    try:
                        tool_tools = tool_instance.register(context)
                        self.tools.extend(tool_tools)
                        logger.success(f"Successfully loaded tool: {tool_instance.name}")
                    except Exception as reg_e:
                        logger.error(f"Failed to register tool from {tool_file.name}: {reg_e}")
                else:
                    logger.error(f"Tool {tool_file.name} does not implement ToolInterface.")
            else:
                logger.error(f"No register() function found in {tool_file.name}")
        return self.tools

    def reload_tools(self) -> list:
        self.tools.clear()
        for tool_file in self.tool_dir.glob("*.py"):
            if tool_file.name == "__init__":
                continue
            module_name = tool_file.stem
            if module_name in sys.modules:
                del sys.modules[module_name]
        logger.success("Reloading tools...")
        return self.load_tools() 