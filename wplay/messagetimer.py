import time
import random
from wplay import seleniumUtils as sel


def msgTimer(name):

    target = str(name)

    # enter message type number
    nMessages = int(input("How many types of messages will you send? "))

    # type your messages
    messages = list()
    for i in range(0, nMessages):
        messages.append(str(input("Enter your message: ")))
    n = int(input("Enter the number of messages to send: "))

    # Enter the time interval of the messages, it will be sent using a random
    # interval. For fixed interval, type the same number.
    minimumTimeInterval = int(
        input("Enter minimum interval number in seconds: "))
    maximumTimeInterval = int(
        input("Enter maximum interval number in seconds: "))

    driver_wait, chosen_website = sel.initialize_chrome_driver(
        sel.websites['whatsapp'])

    sel.find_and_navigate_to_target(driver_wait, chosen_website, target)

    message_area = sel.navigate_to_message_area(driver_wait, chosen_website)

    # sends random messages multiple times
    random.seed()
    i = 0
    while i < n:
        if not messages:
            break
        else:
            sel.send_message(
                message_area, messages[random.randrange(0, nMessages)])
            if minimumTimeInterval != maximumTimeInterval:
                time.sleep(random.randrange(minimumTimeInterval,
                                            maximumTimeInterval))
            else:
                time.sleep(minimumTimeInterval)
        i = i+1
