# region IMPORTS
from pathlib import Path
from typing import List, Iterator
import json

from wplay.utils import helpers
from wplay.utils.Logger import Logger
# endregion

class MessageStack():
    def __init__(self):
        self.logger = Logger(Path(__file__).name)
        self.__create_json_file(helpers.messages_json_path)
        self.__ensure_valid_json(helpers.messages_json_path)
        self.__create_json_file(helpers.open_messages_json_path)
        self.__ensure_valid_json(helpers.open_messages_json_path)

    def __create_json_file(self, file_path: Path):
        if not file_path.is_file():
            open(file_path, 'w').close()
            self.logger.info(f'{file_path.name} created.')

    def __write_json(self, data: dict, file_path: Path):
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4) 

    def __ensure_valid_json(self, file_path: Path):
        valid_data = {"messages":list()}
        try:
            with open(file_path) as json_file:
                data = json.load(json_file)
                if not 'messages' in data:
                    self.__write_json(valid_data, file_path)                
        except json.JSONDecodeError:
            # Empty or Invalid Json
            self.__write_json(valid_data, file_path)

    def append_message(self, message: dict, file_path: Path):
        """
        Append messages into json file.

        Arguments:
            message -- dict with a message
            file_path {Path} -- open_messages_json_path or messages_json_path from helpers
        """
        self.__ensure_valid_json(file_path)

        with open(file_path) as json_file:
            json_data = json.load(json_file)
        json_data['messages'].append(message)
        
        self.__write_json(json_data, file_path)
        self.logger.info(f'Message appended to {file_path.name}')

    def get_message(
            self,
            from_file_path: Path = helpers.messages_json_path) -> Iterator[dict]:
        """
        Yield a message from a file. 

        Arguments:
            from_file_path {Path} -- open_messages_path or messages_path from helpers

        Exception:
            raise StopIteration, json.JSONDecodeError, KeyError if file is empty, or the iteration stopped or the key isn't finded.

        Yields:
            [dict] -- Yield a dict with all message data
        """
        with open(from_file_path) as json_file:
            data = json.load(json_file)
            for message in data['messages']:
                yield message

    def get_all_messages(
            self,
            from_file_path: Path = helpers.messages_json_path) -> List[dict]:
        self.__ensure_valid_json(from_file_path)
        with open(from_file_path) as json_file:
            data = json.load(json_file)
            return data['messages']

    def move_message(self, from_file_path: Path, to_file_path: Path, uuid: str):
        with open(from_file_path) as json_file:
            data = json.load(json_file)
            for message in data['messages']:
                if uuid in message['uuid']:
                    self.append_message(message, to_file_path)
                    self.remove_message(uuid, from_file_path)

    def move_all_messages(self, from_file_path: Path, to_file_path: Path):
        self.__ensure_valid_json(from_file_path)
        with open(from_file_path) as json_file:
            data = json.load(json_file)
            for message in data['messages']:
                self.append_message(message, to_file_path)
                self.remove_message(message['uuid'], from_file_path)

    def remove_message(self, uuid: str, file_path: Path):
        with open(file_path) as json_file:
            data = json.load(json_file)
            for i, message in enumerate(data['messages']):
                if uuid in message['uuid']:
                    del data['messages'][i]
                    self.__write_json(data, file_path)
                    self.logger.info(f"Message Deleted Successfully from {file_path.name}")

    def remove_all_messages(self, file_path: Path):
        with open(file_path) as json_file:
            data = json.load(json_file)
            for i, message in enumerate(data['messages']):
                del data['messages'][i]
                self.__write_json(data, file_path)
            self.logger.info(f"Deleted Successfully all messages from {file_path.name}")