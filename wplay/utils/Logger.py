# region IMPORTS
import logging
from pathlib import Path
from wplay.utils.helpers import log_file_path, logs_path, test_log_file_path
# endregion


class Logger:
    if not (log_file_path).exists():
        logs_path.mkdir(parents=True, exist_ok=True)
        open(log_file_path, 'w').close()

    if not (test_log_file_path).exists():
        logs_path.mkdir(parents=True, exist_ok=True)
        open(test_log_file_path, 'w').close()

    def __init__(self, script_name: str, level: int = logging.WARNING):
        self.logger = logging.getLogger(script_name)
        self.level = level
        self.logger.setLevel(self.level)

        if not self.logger.handlers:
            # Create handlers
            file_handler = logging.FileHandler(log_file_path)
            file_handler = logging.FileHandler(test_log_file_path)
            console = logging.StreamHandler()
            file_handler.setLevel(self.level)
            console.setLevel(self.level)

            # create formatter and add it to the handlers
            formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            console.setFormatter(formatter)
            file_handler.setFormatter(formatter)

            # add the handlers to logger
            self.logger.addHandler(console)
            self.logger.addHandler(file_handler)

    def debug(self, msg: str):
        self.logger.debug(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def info(self, msg: str):
        self.logger.info(msg)
