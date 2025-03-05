from core.tools.tool_interface import ToolInterface, ToolContext
from typing import List, Callable
import socket

class IPAddressTool(ToolInterface):
    @property
    def name(self) -> str:
        return "IPAddressTool"

    def register(self, context: ToolContext) -> List[Callable]:
        context.success("Registering IPAddressTool tools.")

        def get_ip_address() -> str:
            try:
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                context.success(f"IP address obtained: {ip_address}")
                return ip_address
            except Exception as e:
                context.error(f"Error retrieving IP address: {e}")
                return "Error retrieving IP address"

        return [get_ip_address]

def register():
    try:
        return IPAddressTool()
    except Exception as e:
        from core.utils.logger import get_logger
        get_logger().error(f"Error during ip_address_tool registration: {e}")
        return None