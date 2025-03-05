import functools
from core.utils.logger import get_logger

logger = get_logger()

def handle_errors(default_return=None):
    """
    A decorator that catches exceptions, logs them,
    and returns a default value.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
                return default_return
        return wrapper
    return decorator 