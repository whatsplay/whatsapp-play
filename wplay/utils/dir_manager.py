from pathlib import Path
from wplay.utils import helpers


def create_dirs():
    __create_log_folder()
    __create_user_data_folder()


def __create_log_folder():
    helpers.logs_path.mkdir(parents=True, exist_ok=True)


def __create_user_data_folder():
    helpers.user_data_folder_path.mkdir(parents=True, exist_ok=True)