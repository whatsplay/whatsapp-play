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
from pyppeteer import launch
from wplay.utils.session_manager import session_manager
from wplay.utils.helpers import websites, user_data_folder_path
from wplay.utils import Logger
from wplay.utils.helpers import logs_path
# endregion


# region FOR SCRIPTING
async def configure_browser_and_load_whatsapp():
    __patch_pyppeteer()
    username, save_session = session_manager()
    browser = await __config_browser(username, save_session)
    pages : list[int] = await __config_pages(browser)
    return pages[0], browser
# endregion


#region LOGGER create
logger : Logger = Logger.setup_logger('logs',logs_path/'logs.log')
#endregion


# region PYPPETEER PATCH
# https://github.com/miyakogi/pyppeteer/pull/160
# HACK: We need this until this PR is accepted. Solves the bug bellow.
# BUG:(Pyppeteer) The communication with Chromium are disconnected after 20s.
def __patch_pyppeteer():
    from typing import Any
    from pyppeteer import connection, launcher
    import websockets.client
    logger.debug("Using Pyppeteer for connecting to Chromium")

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
async def __config_browser(username = None, save_session = False):
    if username is not None and username != '' and save_session:
        logger.info('Configuring Browser')
        return await launch(
            headless = False,
            autoClose = False,
            userDataDir = user_data_folder_path / username
        )
    else:
        return await launch(headless = False, autoClose = False)


async def __config_pages(browser):
    logger.info('Opening Browser')
    pages : list[int] = await __get_pages(browser)
    await __set_user_agent(pages[0])
    # await __set_view_port(pages[0])
    await __open_website(pages[0], websites['whatsapp'])
    return pages


async def __open_new_page(browser):
    await browser.newPage()


async def __get_pages(browser):
    return await browser.pages()


async def __set_user_agent(page):
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')


async def __set_view_port(page):
    await page.setViewport({'width': 1280, 'height': 800})


async def __open_website(page, website):
    await page.bringToFront()
    await page.goto(website, waitUntil='networkidle2', timeout=0)


def __exit_if_wrong_url(page, browser, url_to_check):
    if not page.url == url_to_check:
        logger.error('Exit due to Wrong URL!')
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
