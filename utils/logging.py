import enum
import logging
import os
import time

from logging.handlers import RotatingFileHandler

from utils.io import create_dir


class LoggingTypes(enum.Enum):
    info = 0
    warning = 1
    error = 2
    critical = 3


output_log_folder_path = 'logs'
create_dir(output_log_folder_path)

log_file_path = os.path.join(output_log_folder_path, "{}.log".format(time.time()))
print(log_file_path)

log_handler = RotatingFileHandler(log_file_path, mode='w', maxBytes=50 * 1024 * 1024, backupCount=10, encoding=None,
                                  delay=0)
log_formatter = logging.Formatter('%(asctime)-15s %(threadName)-10s %(levelname)-8s %(message)s')
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)

logger = logging.getLogger('root')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)


def print_and_log(msg: str, logging_type: LoggingTypes = LoggingTypes.info, print_on_console: bool = True):
    if print_on_console:
        print(msg)

    if logging_type == LoggingTypes.info:
        logger.info(msg)
    elif logging_type == LoggingTypes.warning:
        logger.warning(msg)
    elif logging_type == LoggingTypes.error:
        logger.error(msg)
    elif logging_type == LoggingTypes.critical:
        logger.critical(msg)
