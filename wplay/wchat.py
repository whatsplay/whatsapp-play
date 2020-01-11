from wplay import pyppeteerUtils as pyp


def chat(target):
    #target = str(input("Enter the name of target: "))

    pages = await pyp.configure_browser_and_load_whatsapp(pyp.websites['whatsapp'])
    await pyp.search_for_target_and_get_ready_for_conversation(pages[0], target)

    while True:
        print("1. Chat")
        print("2. Quit")
        option = int(input("Enter choice: "))

        if option == 1:
            
            #message = pyp.ask_user_for_message()
            message = pyp.ask_user_for_message_breakline_mode()

            pyp.send_message(pages[0], message)

        if option == 2:
            exit()
