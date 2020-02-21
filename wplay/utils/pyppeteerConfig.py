__author__ = 'Alexandre Calil Martins Fonseca, github: xandao6'


# region TUTORIAL
'''
Go to region 'FOR SCRIPTING' and use the methods in your script!

EXAMPLE OF USAGE:
from wplay.pyppeteerUtils import pyppeteerConfig as pypConfig
from wplay.pyppeteerUtils import pyppeteerSearch as pypSearch

async def my_script(target):
    pages, browser = wait pyp.configure_browser_and_load_whatsapp(pypConfig.websites['whatsapp'])
    await pypSearch.search_for_target_and_get_ready_for_conversation(pages[0], target)

    message = pypSearch.ask_user_for_message_breakline_mode()
    await pypSearch.send_message(pages[0], message)

    message2 = pypSearch.ask_user_for_message()
    await pypSearch.send_message(pages[0], message2)

'''
# endregion


# region IMPORTS
import os
import json
from pathlib import Path

from pyppeteer import launch

from wplay.utils import sessionManagment
from wplay.utils.helpers import whatsapp_selectors_dict, websites
from wplay.utils.helpers import user_data_folder_path, data_folder_path
# endregion


# region FOR SCRIPTING
async def configure_browser_and_load_whatsapp():
    website = websites['whatsapp']
    __patch_pyppeteer()
    username, save_session = sessionManagment.session_manager()
    browser = await __config_browser(username, save_session)
    pages = await __get_pages(browser)
    await __open_website(pages[0], website)
    return pages[0], browser
# endregion


# region PYPPETEER PATCH
# https://github.com/miyakogi/pyppeteer/pull/160
# HACK: We need this until this PR is accepted. Solves the bug bellow.
# BUG:(Pyppeteer) The communication with Chromium are disconnected after 20s.
def __patch_pyppeteer():
    from typing import Any
    from pyppeteer import connection, launcher
    import websockets.client

    class PatchedConnection(connection.Connection):  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            self._ws = websockets.client.connect(
                self._url,
                loop=self._loop,
                max_size=None,  # type: ignore
                ping_interval=None,  # type: ignore
                ping_timeout=None,  # type: ignore
            )

    connection.Connection = PatchedConnection
    launcher.Connection = PatchedConnection
# endregion


# region PYPPETEER CONFIGURATION
async def __config_browser(username=None, save_session=False):
    if username is not None and username != '' and save_session:
        return await launch(
            headless=False,
            autoClose=False,
            userDataDir=user_data_folder_path/username
        )
    else:
        return await launch(headless=False, autoClose=False)


async def __open_new_page(browser):
    await browser.newPage()


async def __get_pages(browser):
    return await browser.pages()


async def __open_website(page, website):
    await page.bringToFront()
    await page.goto(website, waitUntil='networkidle2', timeout=0)

def __exit_if_wrong_url(page, browser, url_to_check):
    if not page.url == url_to_check:
        print("Wrong URL!")
        browser.close()
        exit()
        return
# endregion


# region CODE THAT MIGHT BE USEFUL SOMEDAY
'''
# FIX: 
# To load websites faster
async def intercept(request, page_one, page_two):
    await page_one.setRequestInterception(True)
    await page_two.setRequestInterception(True)
    if any(request.resourceType == _ for _ in ('stylesheet', 'image', 'font', 'media')):
        await request.abort()
    else:
        await request.continue_()
    page.on('request', lambda req: asyncio.ensure_future(intercept(req)))
'''
# endregion