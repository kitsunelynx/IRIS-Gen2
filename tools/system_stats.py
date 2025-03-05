import psutil
from core.utils.logger import get_logger
from core.tools.tool_interface import ToolInterface, ToolContext
from typing import List, Callable

logger = get_logger()

def get_system_stats() -> str:
    """
    Retrieve real-time system statistics including CPU usage, memory usage, and disk usage.

    Returns:
        str: A formatted string with CPU usage, memory usage, and disk usage details.
    """
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        stats = (
            f"CPU Usage: {cpu_usage}%\n"
            f"Memory Usage: {memory.percent}% (Available: {memory.available // (1024**2)} MB)\n"
            f"Disk Usage: {disk.percent}% (Free: {disk.free // (1024**3)} GB)"
        )
        logger.success("System stats retrieved successfully.")
        return stats
    except Exception as e:
        logger.error(f"Error retrieving system stats: {e}")
        return f"Error retrieving system stats: {e}"

class SystemStatsTool(ToolInterface):
    @property
    def name(self) -> str:
        return "SystemStatsTool"
    
    def register(self, context: ToolContext) -> List[Callable]:
        context.success("Registering SystemStatsTool tools.")

        def get_system_stats() -> str:
            try:
                cpu = psutil.cpu_percent(interval=1)
                mem = psutil.virtual_memory().percent
                result = f"CPU usage: {cpu}%, Memory usage: {mem}%"
                context.success("System statistics retrieved.")
                return result
            except Exception as e:
                context.error(f"Error retrieving system stats: {e}")
                return f"Error retrieving system stats: {e}"

        return [get_system_stats]

def register():
    try:
        return SystemStatsTool()
    except Exception as e:
        logger.error(f"Error during system_stats_tool registration: {e}")
        return None 