import time
import random
from wplay import pyppeteerUtils as pyp


async def msgTimer(target):
    #name = str(input("Enter the name of target: "))

    pages = await pyp.configure_browser_and_load_whatsapp(pyp.websites['whatsapp'])
    await pyp.search_for_target_and_get_ready_for_conversation(pages[0], target)

    #region INPUTS
    message_type_numbers = int(
        input("How many types of messages will you send? "))

    messages = list()
    for _ in range(message_type_numbers):
        #messages.append(pyp.ask_user_for_message())
        messages.append(pyp.ask_user_for_message_breakline_mode())

    number_of_messages = int(input("Enter the number of messages to send: "))

    # Enter the time interval of the messages, it will be sent using a random
    # interval. For fixed interval, type the same number.
    minimumTimeInterval = int(
        input("Enter minimum interval number in seconds: "))
    maximumTimeInterval = int(
        input("Enter maximum interval number in seconds: "))
    #endregion
    
    random.seed()
    for _ in range(number_of_messages):
        if not messages:
            break
        await pyp.send_message(pages[0], messages[random.randrange(0, message_type_numbers)])
        if minimumTimeInterval != maximumTimeInterval:
            time.sleep(random.randrange(minimumTimeInterval, maximumTimeInterval))
        else:
            time.sleep(minimumTimeInterval)