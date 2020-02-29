
# region IMPORTS
from wplay.utils.helpers import whatsapp_selectors_dict
# endregion


# region FOR SCRIPTING
async def get_last_seen_from_focused_target(page):
    # await page.waitForSelector(whatsapp_selectors_dict['status'], visible = True)
    try:
        status = await page.evaluate(f'document.querySelector("{whatsapp_selectors_dict["last_seen"]}").getAttribute("title")')
        return status
    except:
        return '#status not found'
# endregion
