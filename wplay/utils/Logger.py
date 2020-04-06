# region IMPORTS
import logging
from pathlib import Path
from wplay.utils.helpers import logs_path
# endregion


class Logger:
    def __init__(self, script_name: str, level : int = logging.WARNING):
        self.logger = logging.getLogger(script_name)
        self.level = level
        self.logger.setLevel(self.level)
        
        if not self.logger.handlers:
            # Create handlers
            file_handler = logging.FileHandler(logs_path/'wplay.log')
            console = logging.StreamHandler()
            file_handler.setLevel(self.level)
            console.setLevel(self.level)

            # create formatter and add it to the handlers
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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