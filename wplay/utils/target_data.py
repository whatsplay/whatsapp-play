
# region IMPORTS
from wplay.utils.helpers import whatsapp_selectors_dict
from wplay.utils import Logger
from wplay.utils.helpers import logs_path
# endregion


#region LOGGER create
logger : Logger = Logger.setup_logger('logs',logs_path/'logs.log')
#endregion


# region FOR SCRIPTING
async def get_last_seen_from_focused_target(page):
    logger.info("Writing target's status information")
    # await page.waitForSelector(whatsapp_selectors_dict['status'], visible = True)
    try:
        status : str = await page.evaluate(f'document.querySelector("{whatsapp_selectors_dict["last_seen"]}").getAttribute("title")')
        return status
    except:
        return '#status not found'
# endregion
