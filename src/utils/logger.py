from loguru import logger
import sys, os
def setup_logger():
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "logs")
    os.makedirs(log_dir, exist_ok=True)
    logger.add(os.path.join(log_dir, "app.log"), rotation="1 MB", level="DEBUG")
    return logger
