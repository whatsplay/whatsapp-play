from wplay import seleniumUtils as sel


def chat(name):
    _, driver_wait, chosen_website = sel.initialize_chrome_driver(
        sel.websites['whatsapp'])

    while True:
        print("1. Chat")
        print("2. Quit")
        option = int(input("Enter choice: "))

        if option == 1:
            #name = str(input("Enter the name of target: "))
            message = str(input("Enter your message: "))

            sel.find_and_navigate_to_target(
                driver_wait, chosen_website, name)

            message_area = sel.navigate_to_message_area(
                driver_wait, chosen_website)

            sel.send_message(message_area, message)

        if option == 2:
            exit()
