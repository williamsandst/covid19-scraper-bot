import logging
import config
from collections import deque
from pathlib import Path

log_time = False

def init_logging(log_file_path=None, append=False, console_loglevel=logging.INFO):
    """Set up logging to file and console."""
    message_format = "[%(levelname)s %(name)s] %(message)s"
    if config.LOG_TIMESTAMPS:
         message_format = "[%(asctime)s %(levelname)s %(name)s] %(message)s"
    if config.LOG_TO_FILE:
        logging.basicConfig(level=console_loglevel,
                            format=message_format,
                            datefmt='%Y-%m-%d %H:%M:%S',
                            handlers=[
                                logging.FileHandler(log_file_path),
                                logging.StreamHandler()
                            ])
    else:
         logging.basicConfig(level=console_loglevel,
                            format=message_format,
                            datefmt='%Y-%m-%d %H:%M:%S')

    if config.DISABLE_UNIMPORTANT_MODULE_LOGGING:
        logging.getLogger("discord").setLevel(logging.ERROR)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("googleapiclient").setLevel(logging.ERROR)
        logging.getLogger("oauth2client").setLevel(logging.ERROR)

def tail(file_path, line_count):
    f = open(file_path)
    result = ""
    for line in deque(f, line_count):
        result += line
    f.close()
    return result

def prepare_directories():
    Path("screenshots").mkdir(parents=True, exist_ok=True)
    Path("data").mkdir(parents=True, exist_ok=True)