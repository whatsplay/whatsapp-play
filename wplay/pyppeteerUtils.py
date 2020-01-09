'''
HOW TO USE

'''

import asyncio
import sys
from pyppeteer import launch

websites = {'whatsapp': 'https://web.whatsapp.com/'}


async def main():
    __patch_pyppeteer()
    browser = await config_browser(is_headless=False, is_auto_close=False)
    page_one, _ = await config_pages(browser)
    await page_one.bringToFront()
    await open_website(page_one, websites['whatsapp'])
    await open_new_chat(page_one)
    await type_in_search_bar(page_one, 'religare')
    contact_list = await search_contacts(page_one, 'religare')
    group_list = await search_groups(page_one, 'religare')
    # await navigate_to_target(page_one, target_list)
    # await navigate_to_message_area(page_one, websites['whatsapp'])


# https://github.com/miyakogi/pyppeteer/pull/160
# We need this until this update is accepted.
# BUG: The communication with Chromium are disconnected after 20 seconds.
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


def __get_selectors_dict(target=None):
    selectors_dict = {
        'new_chat_button': '#side > header div[role="button"] span[data-icon="chat"]',
        'search_contact_input': '#app > div > div span > div > span > div div > label > input',
        'contact_list_filtered': '#app > div > div span > div > span > div div > div div > div div > span > span[title][dir]',
        'group_list_filtered': '#app > div > div span > div > span > div div > div div > div div > span[title][dir]',
        # 'wpp_target_title_chat_list': f'#pane-side span[title="{target}"]',
        # 'wpp_target_title_contact_list': f'#app > div > div span[title="{target}"]',
        'wpp_message_area': '#main > footer div.selectable-text[contenteditable]'
    }
    return selectors_dict


def __get_XPath_dict(target=None):
    XPath_dict = {
        # 'wpp_target_titles_chat_list': f'//span[contains(@title, "{target}")]',
        # 'wpp_target_titles_contact_list': f'',
        # 'wpp_message_area': '//div[@class="_3u328 copyable-text selectable-text"]'
    }
    return XPath_dict


async def config_browser(is_headless, is_auto_close):
    return await launch(headless=is_headless, autoClose=is_auto_close)


async def config_pages(browser):
    await browser.newPage()
    pages = await browser.pages()
    page_one = pages[0]
    page_two = pages[1]
    return page_one, page_two


async def open_website(page, website):
    await page.goto(website, waitUntil='networkidle2', timeout=0)


# Clicks in 'New Chat' to open your contact list
async def open_new_chat(page):
    selectors_dict = __get_selectors_dict()
    if page.url == websites['whatsapp']:
        await page.waitForSelector(
            selectors_dict['new_chat_button'],
            visible=True,
            timeout=0
        )
        await page.click(selectors_dict['new_chat_button'])


async def type_in_search_bar(page, target):
    selectors_dict = __get_selectors_dict(target)

    print(f'Looking for: {target}')
    if page.url == websites['whatsapp']:
        await page.waitForSelector(
            selectors_dict['search_contact_input'],
            visible=True
        )
        await page.type(selectors_dict['search_contact_input'], target)
        await page.waitFor(3000)


async def search_contacts(page, target):
    selectors_dict = __get_selectors_dict(target)
    contact_list = list()

    if page.url == websites['whatsapp']:
        try:
            await page.waitForSelector(
                selectors_dict['contact_list_filtered'],
                visible=True
            )

            contact_list = await page.querySelectorAll(
                selectors_dict['contact_list_filtered']
            )

            print("Contacts found:")
            for i in range(len(contact_list)):
                contact_title = await page.evaluate(
                    f'document.querySelectorAll("{selectors_dict["contact_list_filtered"]}")[{i}].getAttribute("title")'
                )
                if (contact_title.lower().find(target.lower()) != -1):
                    print(f'{i}: {contact_title}')
                else:
                    pass

        except Exception as e:
            #print(f'No contact named by "{target}"!')
            print(str(e))
    print('\n')
    return contact_list


async def search_groups(page, target):
    selectors_dict = __get_selectors_dict(target)
    group_list = list()

    if page.url == websites['whatsapp']:
        try:
            await page.waitForSelector(
                selectors_dict['group_list_filtered'],
                visible=True
            )

            group_list = await page.querySelectorAll(
                selectors_dict['group_list_filtered']
            )

            print("Groups found:")
            for i in range(len(group_list)):
                group_title = await page.evaluate(
                    f'document.querySelectorAll("{selectors_dict["group_list_filtered"]}")[{i}].getAttribute("title")'
                )
                if (group_title.lower().find(target.lower()) != -1):
                    print(f'{i}: {group_title}')
                else:
                    pass

        except Exception as e:
            #print(f'No group named by "{target}"!')
            print(str(e))
    return group_list


'''async def navigate_to_target(page, target_list):
    if page.url == websites['whatsapp']:
        # target_title = await page.xpath(XPath_dict['wpp_target_title'])
        # target_title = await page.querySelectorAll(
        #    selectors_dict['wpp_target_titles_contact_list']
        # )
        # await target_title[0].click()
        await target_list[0].click()
        print("CLICADO NO TARGET")
    else:
        print(f'You are in wrong page! {page.url}')
        sys.exit()


async def navigate_to_message_area(page):
    selectors_dict = __get_selectors_dict()

    if page.url == websites['whatsapp']:
        await page.waitForXPath(XPath_dict['wpp_message_area'], visible=True)
        message_area = await page.xpath(XPath_dict['wpp_message_area'])
        await message_area[0].click()
    else:
        print(f'You are in wrong page! {page.url}')
        sys.exit()
    # return message_area


async def send_message(page, message):
    await page.keyboard.type(str(message))
    #message_area.send_keys(message + Keys.ENTER)

'''
#loop = asyncio.get_event_loop()
# asyncio.ensure_future(main())
# loop.run_forever()
asyncio.get_event_loop().run_until_complete(main())

'''
#To load websites faster, need fix
async def intercept(request, page_one, page_two):
    await page_one.setRequestInterception(True)
    await page_two.setRequestInterception(True)
    if any(request.resourceType == _ for _ in ('stylesheet', 'image', 'font', 'media')):
        await request.abort()
    else:
        await request.continue_()
    page.on('request', lambda req: asyncio.ensure_future(intercept(req)))
'''
