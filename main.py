import warnings
import argparse
from core import app
from core.utils.logger import get_logger

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IRIS application")
    parser.add_argument("--log-level", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], 
                        default="WARNING", help="Set the logging level (default: WARNING)")
    args = parser.parse_args()

    logger = get_logger(level=args.log_level)
    logger.success(f"Log level set to {args.log_level}")

    app.main()