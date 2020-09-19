# region IMPORTS
from pathlib import Path

from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import target_select
from wplay.utils.helpers import save_chat_folder_path
from wplay.utils.Logger import Logger
# endregion


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


async def save_chat(target):
    """
    Save the whole chat of the target person in .txt file.
    """
    page, _ = await browser_config.configure_browser_and_load_whatsapp()

    if target is not None:
        try:
            await target_search.search_and_select_target(page, target)
        except Exception as e:
            print(e)
            await page.reload()
            await target_search.search_and_select_target_without_new_chat_button(page, target)
    else:
        target = await target_select.manual_select_target(page)

    # selectors
    selector_values = "#main > div > div > div > div > div > div > div > div"
    selector_sender = "#main > div > div > div > div > div > div > div > div > div.copyable-text"

    # Getting all the messages of the chat
    try:
        __logger.info("Saving chats with target")
        await page.waitForSelector(selector_values)
        values = await page.evaluate(f'''() => [...document.querySelectorAll('{selector_values}')]
                                                    .map(element => element.textContent)''')
        sender = await page.evaluate(f'''() => [...document.querySelectorAll('{selector_sender}')]
                                                    .map(element => element.getAttribute("data-pre-plain-text"))''')

        final_values = [x[:-8] for x in values]
        new_list = [a + b for a, b in zip(sender, final_values)]

        # opens chat file of the target person
        with open(save_chat_folder_path / f'chat_{target}.txt', 'w') as output:
            for s in new_list:
                output.write("%s\n" % s)

    except Exception as e:
        print(e)

    finally:
        # save the chat and close the file
        output.close()
        print(f'\nChat file saved in: {str(save_chat_folder_path/"chat_")}{target}.txt')
