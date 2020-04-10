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
from typing import Any, List
from pathlib import Path

import websockets.client
from pyppeteer import launch, connection, launcher
from pyppeteer.browser import Browser
from pyppeteer.page import Page

from wplay.utils.SessionManager import SessionManager
from wplay.utils.helpers import websites, user_data_folder_path
from wplay.utils.Logger import Logger
# endregion


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


# region FOR SCRIPTING
async def configure_browser_and_load_whatsapp() -> (Page, Browser):
    """
    Configure browser, configure the first page and open whatsapp website.
    
    Returns:
        Page -- return the first page, with whatsapp open
        Browser -- return the browser object
    """
    __patch_pyppeteer()
    username, save_session = SessionManager.session_manager()
    browser = await __config_browser(username, save_session)
    pages = await get_pages(browser)
    first_page = pages[0]
    await config_page(first_page)
    await load_website(first_page, websites['whatsapp'])
    return first_page, browser


async def get_pages(browser: Browser) -> List[Page]:
    __logger.debug('Getting open pages')
    return await browser.pages()


async def open_new_page(browser: Browser):
    """
    Open a new tab.
    """
    __logger.debug('Opening new page(tab)')
    await browser.newPage()


async def config_page(page: Page):
    __logger.debug('Configuring page')
    await __set_user_agent(page)
    # await __set_view_port(page)


async def load_website(page: Page, website: str):
    __logger.debug(f'Loading website: {website}')
    await page.bringToFront()
    await page.goto(website, waitUntil='networkidle2', timeout=0)


def exit_if_wrong_url(page: Page, browser: Browser, url_to_check: str):
    if not page.url == url_to_check:
        __logger.error('Exit due to Wrong URL!')
        browser.close()
        exit()
# endregion


# region PYPPETEER PATCH
# https://github.com/miyakogi/pyppeteer/pull/160
# HACK: We need this until this PR is accepted. Solves the bug bellow.
# BUG:(Pyppeteer) The communication with Chromium are disconnected after 20s.
def __patch_pyppeteer():
    __logger.debug("Patching Pyppeteer.")
    class PatchedConnection(connection.Connection):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            self._ws = websockets.client.connect(
                self._url,
                loop=self._loop,
                max_size=None,
                ping_interval=None,
                ping_timeout=None,
            )

    connection.Connection = PatchedConnection
    launcher.Connection = PatchedConnection
# endregion


# region PYPPETEER PRIVATE FUNCTIONS
async def __config_browser(username: str = None, save_session: bool = False):
    __logger.debug('Configuring Browser.')
    if username is not None and username.strip() != '' and save_session:
        return await launch(
            headless=False,
            autoClose=False,
            userDataDir=user_data_folder_path / username
        )
    else:
        return await launch(headless=False, autoClose=False)


async def __set_user_agent(page: Page):
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')


async def __set_view_port(page: Page):
    await page.setViewport({'width': 1280, 'height': 800})
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
