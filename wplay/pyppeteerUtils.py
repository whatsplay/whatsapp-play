__author__ = 'Alexandre Calil Martins Fonseca, github: xandao6'

'''
NOTE, HOW TO USE:

Go to the USER METHODS section and use the methods in your script!

#EXAMPLE OF USAGE:
from wplay import pyppeteerUtils as pyp
async def my_script(target):
    pages = pyp.await configure_browser_and_load_whatsapp(websites['whatsapp'])
    await pyp.look_for_target_and_get_ready_for_conversation(pages[0], test_target)

    message_parts = pyp.ask_user_for_message_breakline_mode()
    await pyp.send_message_breakline_mode(pages[0], message_parts)

    message = pyp.ask_user_for_message_normal_mode()
    await pypsend_message_normal_mode(pages[0], message)

'''

'''
#TODO: Wait for the last message to be sent before closing the browser
#TODO: Change __config_browser autoClose to True
#TODO: Verify if target is included in title
'''


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
    contact_list = await __search_contacts_filtered(page, target)
    group_list = await __search_groups_filtered(page, target)
    target_list = __get_target_list(contact_list, group_list)
    await __print_target_list(page, target, contact_list, group_list, target_list)
    final_target_index = __choose_filtered_target(target_list)
    await __navigate_to_target(page, target_list, final_target_index)
    target_focused_title = await __get_focused_target_title(page, target)
    __print_selected_target_title(target_focused_title)
    await __verify_target_title(page, target, target_focused_title)
    await __wait_for_message_area(page)


def ask_user_for_message():
    return str(input("Write your message: "))


def ask_user_for_message_breakline_mode():
    message = []
    i = 0
    print("Write your message ('Enter' mean breakline)(Write '#ok' to finish):")
    while True:
        message.append(str(input()))
        if message[i] == '#ok':
            message.pop(i)
            break
        i += 1
    return message


async def send_message(page, message):
    whatsapp_selectors_dict = __get_whatsapp_selectors_dict()

    for i in range(len(message)):
        await page.type(
            whatsapp_selectors_dict['message_area'],
            message[i]
        )
        if isinstance(message, list):
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
        'target_focused_title' : '#main > header div > div > span[title]',
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


async def __search_contacts_filtered(page, target):
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
    except Exception as e:
        print(f'No contact named by "{target}"! Error: {str(e)}')
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
    except Exception as e:
        print(f'No group named by "{target}"! Error: {str(e)}')
    return group_list


def __get_target_list(contact_list, group_list):
    return contact_list + group_list


# FIXME: Needs refactoring
async def __verify_contact_list(page, target, contact_list, target_list, last_contact_index, i):
    whatsapp_selectors_dict = __get_whatsapp_selectors_dict(target)

    if i == 0 and len(contact_list) > 0:
        print("Contacts found:")
        last_contact_index = 0

    contact_title = await page.evaluate(f'document.querySelectorAll("{whatsapp_selectors_dict["contact_list_filtered"]}")[{i}].getAttribute("title")')

    if (contact_title.lower().find(target.lower()) != -1
            and len(contact_list) > 0):
        print(f'{i}: {contact_title}')
        last_contact_index += 1
    else:
        target_list.pop(i)

    return last_contact_index


# FIXME: Needs refactoring
async def __verify_group_list(page, target, contact_list, group_list, target_list, last_contact_index, i):
    whatsapp_selectors_dict = __get_whatsapp_selectors_dict(target)

    if i == len(contact_list) and len(group_list) > 0:
        if (i - len(contact_list)) > last_contact_index:
            print("Groups found:")

    group_title = await page.evaluate(f'document.querySelectorAll("{whatsapp_selectors_dict["group_list_filtered"]}")[{i - len(contact_list)}].getAttribute("title")')

    if (group_title.lower().find(target.lower()) != -1
            and len(group_list) > 0):
        if (i - len(contact_list)) > last_contact_index:
            print(f'{i- len(contact_list)}: {group_title}')
    else:
        target_list.pop(i)


# FIXME: Needs refactoring
# OBS: The last_contact_index is a trick to hide a false-positive group
# False positive group -> Groups name use the same div as contact status, so we need
#   to verify if target name is in title, not in status. But, sometimes the status contain
#   the target name and shows up as false-positive group. 
async def __print_target_list(page, target, contact_list, group_list, target_list):

    try:
        last_contact_index = 0
        for i in range(len(target_list)):
            if i < len(contact_list):
                last_contact_index = await __verify_contact_list(page, target, contact_list, target_list, last_contact_index, i)
            elif i >= len(contact_list):
                await __verify_group_list(page, target, contact_list, group_list, target_list, last_contact_index, i)
    except Exception as e:
        print(f'Error: {str(e)}')


def __choose_filtered_target(target_list):
    final_target_index = int(
        input('Enter the number of the target you wish to choose: '))
    return final_target_index


async def __navigate_to_target(page, target_list, final_target_index):
    await target_list[final_target_index].click()


async def __get_focused_target_title(page, target):
    whatsapp_selectors_dict = __get_whatsapp_selectors_dict()
    try:
        await page.waitForSelector(whatsapp_selectors_dict['target_focused_title'])
        target_focused_title = await page.evaluate(f'document.querySelector("{whatsapp_selectors_dict["target_focused_title"]}").getAttribute("title")')
    except Exception as e:
        print(f'No target selected! Error: {str(e)}')
        sys.exit()
    return target_focused_title


def __print_selected_target_title(target_focused_title):
    print(f"You've selected the target named by: {target_focused_title}")


async def __verify_target_title(page, target, target_focused_title):
    if target_focused_title.lower().find(target.lower()) == -1:
        print(f"You're focused in the wrong target, {target_focused_title}")
        must_continue = str(input("Do you want to continue (yes/no)? "))
        accepted_yes = {'yes', 'y'}
        if must_continue.lower() in accepted_yes:
            pass
        else:
            sys.exit()


async def __wait_for_message_area(page):
    whatsapp_selectors_dict = __get_whatsapp_selectors_dict()
    try:
        await page.waitForSelector(whatsapp_selectors_dict['message_area'])
    except Exception as e:
        print(f"You don't belong this group anymore! Error: {str(e)}")


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