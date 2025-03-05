from core.utils.logger import get_logger
from core.config.config_manager import ConfigManager
from core.utils.ui import UIHandler
import copy

class ToolContext:
    """
    Provides a limited and safe interface for tools.
    Tools should not access core internals directly.
    """
    def __init__(self, logger=None, config=None, ui=None):
        self.logger = logger or get_logger()
        self.config = copy.deepcopy(config) if config else ConfigManager().config
        self.ui = ui or UIHandler()

    def info(self, message: str) -> None:
        self.logger.success(message)

    def error(self, message: str) -> None:
        self.logger.error(message)
        
    def debug(self, message: str) -> None:
        self.logger.debug(message)
        
    def warning(self, message: str) -> None:
        self.logger.warning(message)
        
    def success(self, message: str) -> None:
        self.logger.success(message) 