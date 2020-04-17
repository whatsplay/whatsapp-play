# region IMPORTS
from pathlib import Path
import threading
import time
import json

from wplay.utils import browser_config
from wplay.utils.target_search import search_target_by_number
from wplay.utils import target_select
from wplay.utils import io
from wplay.utils import helpers
from wplay.utils import  verify_internet
from wplay.utils.Logger import Logger
from wplay.utils.MessageStack import MessageStack
# endregion


# region LOGGER
import logging
__logger = Logger(Path(__file__).name, logging.DEBUG)
# endregion


"""
Messages file structure, your program should add messages this way
inside the file "messages.json" located at user/wplay/messagesJSON folder.

{
    "messages": [
        {
            "uuid": "33bf7c667f8011ea96971c3947562893",
            "number": "5562999999999",
            "message": "*Bold Hello World*"
        },
        {
            "uuid": "46ca6d284f8058ee89354e2987862869",
            "number": "5562888888888",
            "message": ["Hello!!!","Multi-line"]
        }
    ]
}
"""


async def message_service():
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    __logger.info("Message Service On.")
    print("Message Service is ON, press CTRL+C to stop.")
    print("Listening for messages in file 'messages.json' inside user/wplay/messagesJSON folder.")
    # Initialize a instance of MessageStack
    message_stack = MessageStack()
    # Move all messages from open_messages.json to messages.json when the program starts
    message_stack.move_all_messages(
        helpers.open_messages_json_path, helpers.messages_json_path)

    while True:
        if verify_internet.internet_avalaible():
            try:
                # Try to get the message
                current_msg = next(message_stack.get_message())

                # Move message from messages.json to open_messages.json
                message_stack.move_message(
                    helpers.messages_json_path,
                    helpers.open_messages_json_path,
                    current_msg['uuid'])

                try:
                    if await search_target_by_number(page, current_msg['number']):
                        await io.send_message(page, current_msg['message'])
                    message_stack.remove_message(
                        current_msg['uuid'], helpers.open_messages_json_path)
                except ValueError:
                    __logger.debug("Wrong JSON Formatting. Message Deleted.")
                    message_stack.remove_message(
                        current_msg['uuid'], helpers.open_messages_json_path)
                except Exception as e:
                    # If any error occurs that is not because of wrong data, the message will be moved back to messages.json
                    __logger.error(f'Error handling and sending the message: {str(e)}')
                    MessageStack().move_message(helpers.open_messages_json_path,
                                                helpers.messages_json_path, current_msg['uuid'])
            except (StopIteration, json.JSONDecodeError):
                # if there are no messages to catch we will have this 'Warning', will try again after a time
                time.sleep(1)
        else:
            __logger.debug('Internet is not available, trying again after 15 seconds.')
            time.sleep(15)

        # Move messages from open_messages.json to messages.json that wasn't sended.
        message_stack.move_all_messages(
            helpers.open_messages_json_path, helpers.messages_json_path)
        