# First two lines import python libraries
import time
import random

#These lines import functions from utils pyton file in wplay.
from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import io

# This function first checks for proper whatsapp web loading.
async def msgTimer(target):
    page, _ = await browser_config.configure_browser_and_load_whatsapp()

    # Waiting till the target username is found.
    await target_search.search_and_select_target(page, target)

    # Region INPUTS
    message_type_numbers = int(
        input("How many types of messages will you send? "))
    messages = list()
    for _ in range(message_type_numbers):
        messages.append(io.ask_user_for_message_breakline_mode())
    # Asking the client for no of message inputs.
    number_of_messages = int(input("Enter the number of messages to send: "))
    # The interval of inputs that is time after which the messages are to be send
    minimumTimeInterval = int(
        input("Enter minimum interval number in seconds: "))
    maximumTimeInterval = int(
        input("Enter maximum interval number in seconds: "))
    # Endregion

    random.seed()
    for _ in range(number_of_messages):
        if not messages:
            break
        await io.send_message(page, messages[random.randrange(0, message_type_numbers)])
        if minimumTimeInterval != maximumTimeInterval:
            time.sleep(random.randrange(minimumTimeInterval, maximumTimeInterval))
        else:
            time.sleep(minimumTimeInterval)
# This script is a helper script for message blast script as the no of messages and the message time are defined here and are being using in the blast script.
