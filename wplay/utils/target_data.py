# region IMPORTS
from pathlib import Path

from pyppeteer.page import Page

from wplay.utils.helpers import whatsapp_selectors_dict
from wplay.utils.Logger import Logger
from wplay.utils.helpers import logs_path
# endregion


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


# region FOR SCRIPTING
async def get_last_seen_from_focused_target(page: Page):
    __logger.info("Getting target's status information")
    # await page.waitForSelector(whatsapp_selectors_dict['status'], visible = True)
    try:
        status : str = await page.evaluate(f'document.querySelector("{whatsapp_selectors_dict["last_seen"]}").getAttribute("title")')
        return status
    except:
        return '#status not found'
# endregion
