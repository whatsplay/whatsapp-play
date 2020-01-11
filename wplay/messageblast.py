from wplay import pyppeteerUtils as pyp


async def blast(target):
    #target = str(input("Enter the name of target: "))
    
    pages = await pyp.configure_browser_and_load_whatsapp(pyp.websites['whatsapp'])
    await pyp.search_for_target_and_get_ready_for_conversation(pages[0], target)

    #message = pyp.ask_user_for_message()
    message = pyp.ask_user_for_message_breakline_mode()

    number_of_messages = int(input("Enter the number of messages to blast: "))

    for _ in range(number_of_messages):
        await pyp.send_message(pages[0], message)
