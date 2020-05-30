# region IMPORTS
from pathlib import Path

from wplay.utils import browser_config
from wplay.utils.Logger import Logger
# endregion


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


async def recent_chat():
    __logger.info("Fetching recent chats...")
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    selector = '#pane-side > div > div > div > div > div > div > div > div > div'
    await page.waitForSelector(selector)
    recentChat_list = await page.evaluate(f'''() => [...document.querySelectorAll('{selector}')]
                                                    .map(element => element.textContent)''')
    new_recentChat_list = [' '.join(i) for i in zip(*[iter(recentChat_list)]*5)]
    final_recentChat_list = new_recentChat_list[::-1]
    final_recentChat_list = final_recentChat_list[-1:] + final_recentChat_list[:-1]
    print(*final_recentChat_list, sep = "\n")