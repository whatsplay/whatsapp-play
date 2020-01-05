from wplay import seleniumUtils as sel


def blast(name):

    # enter the number of the person by the user
    target = str(name)  # str(input("Enter the name of target: "))
    message = str(input("Enter your message: "))
    n = int(input("Enter the number of messages to blast: "))

    driver_wait, chosen_website = sel.initialize_chrome_driver(
        sel.websites['whatsapp'])

    sel.find_and_navigate_to_target(driver_wait, chosen_website, target)

    message_area = sel.navigate_to_message_area(driver_wait, chosen_website)

    # sends message multiple times
    i = 0
    while i < n:
        sel.send_message(message_area, message)
        i = i+1
