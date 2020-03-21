# region IMPORTS
import logging
from pathlib import Path
from wplay.utils.helpers import logs_path
# endregion


# region for FORMAT
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# endregion


# region for logger class
def setup_logger(name : str , log_file : str , level : int = logging.DEBUG) :
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
# endregion


# region for log folder creation
Path(logs_path).mkdir(parents = True, exist_ok = True)
# endregion