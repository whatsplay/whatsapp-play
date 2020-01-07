import asyncio
import sys
from pyppeteer import launch

websites = {'whatsapp': 'https://web.whatsapp.com/'}


async def main():
    browser = await config_browser(is_headless=False, is_auto_close=False)
    page_one, _ = await config_pages(browser)
    await page_one.bringToFront()
    await open_website(page_one, websites['whatsapp'])
    await open_new_chat(page_one)
    await find_target(page_one, 'Amor')
    await navigate_to_target(page_one, 'Amor')
    # await navigate_to_message_area(page_one, websites['whatsapp'])


def __get_selectors_dict():
    selectors_dict = {
        'new_chat_button': '#side > header div[role="button"][title="New chat"]'
    }
    return selectors_dict


def __get_XPath_dict(target=' '):
    XPath_dict = {
        'wpp_target_title': f'//span[contains(@title, "{target}")]',
        'wpp_message_area': '//div[@class="_3u328 copyable-text selectable-text"]'
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
    await page.goto(website, waitUntil='load')


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


# Search for target in contact list
async def find_target(page, target):
    XPath_dict = __get_XPath_dict(target)
    target_list = []
    print(f'Looking for: {target}')
    if page.url == websites['whatsapp']:
        target_list = await page.waitForXPath(
            XPath_dict['wpp_target_title'],
            visible=True,
            timeout=0
        )
        #print(f'{target_list} finded!')
    else:
        print(f'You are in wrong page! {page.url}')
        sys.exit()
    return target_list


async def navigate_to_target(page, target):
    if page.url == websites['whatsapp']:
        # target_title = await page.xpath(XPath_dict['wpp_target_title'])
        target_title = await page.querySelector('#pane-side span[title="Danilo Help"]')
        await target_title[0].click()
    else:
        print(f'You are in wrong page! {page.url}')
        sys.exit()


async def navigate_to_message_area(page):
    XPath_dict = __get_XPath_dict()
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
