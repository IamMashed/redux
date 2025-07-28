import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from config import APP_ROOT

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
logs_dir = Path(APP_ROOT) / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

LOG_FILE = Path(APP_ROOT) / "logs" / "my_app.log"


def get_log_file(file_name):
    return Path(APP_ROOT) / "logs" / file_name


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(log_file=LOG_FILE):
    file_handler = TimedRotatingFileHandler(log_file,
                                            when='D',
                                            interval=10,
                                            backupCount=10)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, console=True):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    if console:
        logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger


def get_file_logger(logger_name, log_file):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_file_handler(get_log_file(log_file)))
    logger.propagate = False
    return logger


def get_console_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.propagate = False
    return logger


logger = get_logger(__name__)
