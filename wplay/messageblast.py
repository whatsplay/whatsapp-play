from wplay import seleniumUtils as sel


def blast(target):
    #target = str(input("Enter the name of target: "))

    message = str(input("Enter your message: "))
    number_of_messages = int(input("Enter the number of messages to blast: "))

    _, driver_wait, chosen_website = sel.initialize_chrome_driver(
        sel.websites['whatsapp'])

    sel.find_and_navigate_to_target(driver_wait, chosen_website, target)

    message_area = sel.navigate_to_message_area(driver_wait, chosen_website)

    for _ in range(number_of_messages):
        sel.send_message(message_area, message)
