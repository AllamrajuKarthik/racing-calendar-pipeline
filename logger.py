# Logs everything.

import logging
from config import LOG_FILE


def get_logger():
    logger = logging.getLogger("racing_pipeline")
    logger.setLevel(logging.INFO)

    # avoid adding duplicate handlers if this gets called more than once
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
