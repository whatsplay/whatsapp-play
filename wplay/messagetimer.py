import time
import random
from wplay import seleniumUtils as sel


def msgTimer(name):
    #name = str(input("Enter the name of target: "))

    message_type_numbers = int(
        input("How many types of messages will you send? "))

    messages = list()
    for _ in range(message_type_numbers):
        messages.append(str(input("Enter your message: ")))

    number_of_messages = int(input("Enter the number of messages to send: "))

    # Enter the time interval of the messages, it will be sent using a random
    # interval. For fixed interval, type the same number.
    minimumTimeInterval = int(
        input("Enter minimum interval number in seconds: "))
    maximumTimeInterval = int(
        input("Enter maximum interval number in seconds: "))

    _, driver_wait, chosen_website = sel.initialize_chrome_driver(
        sel.websites['whatsapp'])

    sel.find_and_navigate_to_target(driver_wait, chosen_website, name)

    message_area = sel.navigate_to_message_area(driver_wait, chosen_website)

    random.seed()
    for _ in range(number_of_messages):
        if not messages:
            break
        else:
            sel.send_message(
                message_area, messages[random.randrange(0, message_type_numbers)])
            if minimumTimeInterval != maximumTimeInterval:
                time.sleep(random.randrange(minimumTimeInterval,
                                            maximumTimeInterval))
            else:
                time.sleep(minimumTimeInterval)