import logging

log_time = False

def init_logging(log_file_path=None, append=False, console_loglevel=logging.INFO):
    """Set up logging to file and console."""
    message_format = "[%(levelname)s %(name)s] %(message)s"
    if log_time:
         message_format = "[%(asctime)s %(levelname)s %(name)s] %(message)s"
    logging.basicConfig(level=console_loglevel,
                        format=message_format,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            logging.FileHandler(log_file_path),
                            logging.StreamHandler()
                        ])

    logging.getLogger("discord").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("googleapiclient").setLevel(logging.ERROR)
    logging.getLogger("oauth2client").setLevel(logging.ERROR)