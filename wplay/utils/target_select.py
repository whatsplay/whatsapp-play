# region IMPORTS
from pathlib import Path

from pyppeteer.page import Page

from wplay.utils.Logger import Logger
from wplay.utils.helpers import whatsapp_selectors_dict
# endregion

# region FOR SCRIPTING
async def manual_select_target(page: Page, hide_groups: bool = False):
    __print_manual_selection_info()
    await __open_new_chat(page)
    target_focused_title = await __get_focused_target_title(page)
    await __wait_for_message_area(page)
    __print_selected_target_title(target_focused_title)
    return target_focused_title
# endregion

# region SELECT TARGET
def __print_manual_selection_info():
    print(f"You've to go to whatsapp web and select target manually")


def __print_selected_target_title(target_focused_title: str):
    print(f"You've selected the target named by: {target_focused_title}")


async def __open_new_chat(page: Page):
    await page.waitForSelector(
        whatsapp_selectors_dict['new_chat_button'],
        visible=True,
        timeout=0
    )


async def __get_focused_target_title(page: Page):
    try:
        await page.waitForSelector(whatsapp_selectors_dict['target_focused_title'], visible=True,
                                   timeout=0)
        target_focused_title = await page.evaluate(f'document.querySelector("{whatsapp_selectors_dict["target_focused_title"]}").getAttribute("title")')
    except Exception as e:
        print(f'No target selected! Error: {str(e)}')
        exit()
    return target_focused_title


async def __wait_for_message_area(page: Page):
    try:
        await page.waitForSelector(whatsapp_selectors_dict['message_area'], timeout=0)
    except Exception as e:
        print(f"You don't belong this group anymore! Error: {str(e)}")
# endregion
