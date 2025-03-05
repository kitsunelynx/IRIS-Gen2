import logging
import os
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback

# Install rich traceback handling for better error display
install_rich_traceback()

# Default log format
LOG_FORMAT = "%(message)s"
DEFAULT_LOG_LEVEL = "INFO"
LOG_DIRECTORY = "logs"

# Ensure log directory exists
Path(LOG_DIRECTORY).mkdir(exist_ok=True)

class IRISLogger:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure only one logger instance exists"""
        if cls._instance is None:
            cls._instance = super(IRISLogger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, level=DEFAULT_LOG_LEVEL, log_to_file=True):
        """Initialize the logger with the specified level and options"""
        if self._initialized:
            return
            
        self._initialized = True
        self.console = Console()
        
        # Convert string log level to actual logging level
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        
        # Configure root logger
        self.logger = logging.getLogger("iris")
        
        # Clear any existing handlers to allow reconfiguration
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
            
        self.logger.setLevel(level)
        self.logger.propagate = False
        
        # Console handler using Rich for pretty formatting
        console_handler = RichHandler(
            console=self.console,
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            show_level=True
        )
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        self.logger.addHandler(console_handler)
        
        # File handler for persistent logs if enabled
        if log_to_file:
            log_file = os.path.join(LOG_DIRECTORY, "iris.log")
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    # Forward standard logging methods
    def debug(self, message, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message, *args, **kwargs):
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message, *args, **kwargs):
        self.logger.exception(message, *args, **kwargs)
    
    # Additional convenience methods
    def success(self, message, *args, **kwargs):
        """Log a success message (using info level with special formatting)"""
        self.logger.info(f"[bold green]✓ {message}[/bold green]", *args, **kwargs)
    
    def warn(self, message, *args, **kwargs):
        """Alias for warning"""
        self.warning(message, *args, **kwargs)

# Global function to get the logger instance
def get_logger(level=DEFAULT_LOG_LEVEL, log_to_file=True):
    """Get the singleton logger instance"""
    return IRISLogger(level, log_to_file) 