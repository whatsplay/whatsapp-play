__author__ = 'Alexandre Calil Martins Fonseca, github: xandao6'

'''
HOW TO USE:

Go to the USER METHODS section and use the methods in sequence in your script!

'''

import asyncio
import sys
from pyppeteer import launch

websites = {'whatsapp': 'https://web.whatsapp.com/'}


'''############################# USER METHODS ##############################'''
async def configure_browser_and_load_whatsapp(website):
    __patch_pyppeteer()
    browser = await __config_browser()
    pages = await __get_pages(browser)
    await __open_website(pages[0], website)
    return pages


async def look_for_target_and_get_ready_for_conversation(page, target):
    await __open_new_chat(page)
    await __type_in_search_bar(page, target)
    contact_list = await __contacts_filtered(page, target)
    group_list = await __search_groups_filtered(page, target)
    target_list = __get_target_list(contact_list, group_list)
    await __print_target_list(page, target, contact_list, group_list, target_list)
    final_target_index = __choose_filtered_target(target_list)
    await __navigate_to_target(page, target_list, final_target_index)
    await __wait_for_message_area(page)


def ask_user_for_message_normal_mode():
    return str(input("Write your message: "))


async def send_message_normal_mode(page, message):
    whatsapp_selectors_dict = __get_whatsapp_selectors_dict()
    await page.type(
        whatsapp_selectors_dict['message_area'],
        message
    )
    await page.keyboard.press('Enter')


def ask_user_for_message_breakline_mode():
    message_parts = []
    i = 0
    print("Write your message ('Enter' mean breakline)(Write '#ok' to finish):")
    while True:
        message_parts.append(str(input()))
        if message_parts[i] == '#ok':
            message_parts.pop(i)
            break
        i += 1
    return message_parts


async def send_message_breakline_mode(page, message_parts):
    whatsapp_selectors_dict = __get_whatsapp_selectors_dict()

    for i in range(len(message_parts)):
        await page.type(
            whatsapp_selectors_dict['message_area'],
            message_parts[i]
        )
        await page.keyboard.down('Shift')
        await page.keyboard.press('Enter')
        await page.keyboard.up('Shift')
    await page.keyboard.press('Enter')
'''#########################################################################'''


# https://github.com/miyakogi/pyppeteer/pull/160
# HACK: We need this until this update is accepted.
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


def __get_whatsapp_selectors_dict(target=None):
    whatsapp_selectors_dict = {
        'new_chat_button': '#side > header div[role="button"] span[data-icon="chat"]',
        'search_contact_input': '#app > div > div span > div > span > div div > label > input',
        'contact_list_filtered': '#app > div > div span > div > span > div div > div div > div div > span > span[title][dir]',
        'group_list_filtered': '#app > div > div span > div > span > div div > div div > div div > span[title][dir]',
        'message_area': '#main > footer div.selectable-text[contenteditable]'
    }
    return whatsapp_selectors_dict


def __exit_if_wrong_url(page, url_to_check):
    if not page.url == url_to_check:
        print("Wrong URL!")
        sys.exit()
        return


async def __config_browser():
    return await launch(headless=False, autoClose=False)


async def __open_new_page(browser):
    await browser.newPage()


async def __get_pages(browser):
    pages = await browser.pages()
    return pages


async def __open_website(page, website):
    await page.bringToFront()
    await page.goto(website, waitUntil='networkidle2', timeout=0)
    __exit_if_wrong_url(page, websites['whatsapp'])


async def __open_new_chat(page):
    whatsapp_selectors_dict = __get_whatsapp_selectors_dict()
    await page.waitForSelector(
        whatsapp_selectors_dict['new_chat_button'],
        visible=True,
        timeout=0
    )
    await page.click(whatsapp_selectors_dict['new_chat_button'])


async def __type_in_search_bar(page, target):
    whatsapp_selectors_dict = __get_whatsapp_selectors_dict(target)
    print(f'Looking for: {target}')
    await page.waitForSelector(
        whatsapp_selectors_dict['search_contact_input'],
        visible=True
    )
    await page.type(whatsapp_selectors_dict['search_contact_input'], target)
    await page.waitFor(3000)


async def __contacts_filtered(page, target):
    whatsapp_selectors_dict = __get_whatsapp_selectors_dict(target)
    contact_list = list()
    try:
        await page.waitForSelector(
            whatsapp_selectors_dict['contact_list_filtered'],
            visible=True,
            timeout=3000
        )

        contact_list = await page.querySelectorAll(
            whatsapp_selectors_dict['contact_list_filtered']
        )
    except:
        print(f'No contact named by "{target}"!')
    return contact_list


async def __search_groups_filtered(page, target):
    whatsapp_selectors_dict = __get_whatsapp_selectors_dict(target)
    group_list = list()

    try:
        await page.waitForSelector(
            whatsapp_selectors_dict['group_list_filtered'],
            visible=True,
            timeout=3000
        )

        group_list = await page.querySelectorAll(
            whatsapp_selectors_dict['group_list_filtered']
        )
    except:
        print(f'No group named by "{target}"!')
    return group_list


def __get_target_list(contact_list, group_list):
    return contact_list + group_list


# FIXME: Need Refactoration
async def __verify_contact_list(page, target, contact_list, target_list, i):
    whatsapp_selectors_dict = __get_whatsapp_selectors_dict(target)

    if i == 0 and len(contact_list) > 0:
        print("Contacts found:")

    contact_title = await page.evaluate(f'document.querySelectorAll("{whatsapp_selectors_dict["contact_list_filtered"]}")[{i}].getAttribute("title")')

    if (contact_title.lower().find(target.lower()) != -1
            and len(contact_list) > 0):
        print(f'{i}: {contact_title}')
    else:
        target_list.pop(i)


# FIXME: Need Refactoration
async def __verify_group_list(page, target, contact_list, group_list, target_list, i):
    whatsapp_selectors_dict = __get_whatsapp_selectors_dict(target)

    if i == len(contact_list) and len(group_list) > 0:
        print("Groups found:")

    group_title = await page.evaluate(f'document.querySelectorAll("{whatsapp_selectors_dict["group_list_filtered"]}")[{i - len(contact_list)}].getAttribute("title")')

    if (group_title.lower().find(target.lower()) != -1
            and len(group_list) > 0):
        print(f'{i- len(contact_list)}: {group_title}')
    else:
        target_list.pop(i)


# FIXME: Need Refactoration
async def __print_target_list(page, target, contact_list, group_list, target_list):

    try:
        for i in range(len(target_list)):
            if i < len(contact_list):
                await __verify_contact_list(page, target, contact_list, target_list, i)
            elif i >= len(contact_list):
                await __verify_group_list(page, target, contact_list, group_list, target_list, i)
    except Exception as e:
        print(str(e))


def __choose_filtered_target(target_list):
    final_target_index = int(
        input('Enter the number of the target you wish to choose: '))
    return final_target_index


async def __navigate_to_target(page, target_list, final_target_index):
    await target_list[final_target_index].click()


async def __wait_for_message_area(page):
    whatsapp_selectors_dict = __get_whatsapp_selectors_dict()
    try:
        await page.waitForSelector(whatsapp_selectors_dict['message_area'])
    except Exception as e:
        print("You don't belong this group anymore!")
        print(str(e))


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

'''
#FOR DEVS TO TEST THIS SCRIPT SOLO
test_target = ''
async def main():
    pages = await configure_browser_and_load_whatsapp(websites['whatsapp'])
    await look_for_target_and_get_ready_for_conversation(pages[0], test_target)

    message_parts = ask_user_for_message_breakline_mode()
    await send_message_breakline_mode(pages[0], message_parts)
    message = ask_user_for_message_normal_mode()
    await send_message_normal_mode(pages[0], message)
#asyncio.get_event_loop().run_until_complete(main())
'''