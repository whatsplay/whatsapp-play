__author__ = 'Alexandre Calil Martins Fonseca, github: xandao6'


# region TUTORIAL
'''
Go to region 'FOR SCRIPTING' and use the methods in your script!

EXAMPLE OF USAGE:
from wplay import pyppeteerUtils as pyp
async def my_script(target):
    pages = wait pyp.configure_browser_and_load_whatsapp(pyp.websites['whatsapp'])
    await pyp.search_for_target_and_get_ready_for_conversation(pages[0], target)

    message = pyp.ask_user_for_message_breakline_mode()
    await pyp.send_message(pages[0], message)

    message2 = pyp.ask_user_for_message()
    await pyp.send_message(pages[0], message2)
'''
# endregion


# region TODO and FIXME
'''
#TODO: Wait for the last message to be sent before closing the browser
#TODO: Change __config_browser autoClose to True
#TODO: return browser.close and use it instead use sys.exit
#TODO: use map and filter in __check_contact_list and __check_group_list
#FIXME: False positive group -> Groups name use the same div as contact status,
        so we need to verify if target name is in title, not in status. But, 
        sometimes the status contain the target name and shows up as 
        false-positive group. 
        WHERE WE CAN FIX? __checking_group_list
#FIXME: ugly output when nobody is found
#FIXME: ugly output when 'ctrl'+'c' is pressed
'''
# endregion


# region IMPORTS
import sys
from pyppeteer import launch
# endregion


# region FOR SCRIPTING
websites = {'whatsapp': 'https://web.whatsapp.com/'}


async def configure_browser_and_load_whatsapp(website):
    __patch_pyppeteer()
    browser = await __config_browser()
    pages = await __get_pages(browser)
    await __open_website(pages[0], website)
    return pages


async def search_for_target_and_get_ready_for_conversation(page, target, hide_groups=False):
    await __open_new_chat(page)
    await __type_in_search_bar(page, target)
    contact_list_elements_unchecked = await __get_contacts_elements_filtered(page, target)
    group_list_elements_unchecked = await __get_groups_elements_filtered(page, target, hide_groups)
    contact_titles_unchecked = await __get_contacts_titles_from_elements_unchecked(page, contact_list_elements_unchecked)
    group_titles_unchecked = await __get_groups_titles_from_elements_unchecked(page, group_list_elements_unchecked)
    contact_list_unchecked = __zip_contact_titles_and_elements_unchecked(
        contact_titles_unchecked, contact_list_elements_unchecked)
    group_list_unchecked = __zip_group_titles_and_elements_unchecked(
        group_titles_unchecked, group_list_elements_unchecked)
    contact_tuple = __check_contact_list(target, contact_list_unchecked)
    group_tuple = __check_group_list(target, group_list_unchecked)
    target_tuple = __get_target_tuple(contact_tuple, group_tuple)
    __print_target_tuple(target_tuple)
    target_index_choosed = __ask_user_to_choose_the_filtered_target(target_tuple)
    choosed_target = __get_choosed_target(target_tuple, target_index_choosed)
    await __navigate_to_target(page, choosed_target)
    target_focused_title = await __get_focused_target_title(page, target)
    __print_selected_target_title(target_focused_title)
    __check_target_focused_title(page, target, target_focused_title)
    await __wait_for_message_area(page)

    return choosed_target


async def get_status_from_focused_target(page):
    #await page.waitForSelector(whatsapp_selectors_dict['status'], visible = True)
    try:
        status = await page.evaluate(f'document.querySelector("{whatsapp_selectors_dict["status"]}").getAttribute("title")')
        return status
    except:
        return '#status not found'


def ask_user_for_message():
    return str(input("Write your message: "))


def ask_user_for_message_breakline_mode():
    message = []
    i = 0
    print("Write your message ('Enter' to breakline)('.' alone to finish):")
    while True:
        message.append(str(input()))
        if message[i] == '.':
            message.pop(i)
            break
        i += 1
    return message


async def send_message(page, message):
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
# endregion


# region PYPPETEER PATCH
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
# endregion


# region UTILS
whatsapp_selectors_dict = {
    'new_chat_button': '#side > header div[role="button"] span[data-icon="chat"]',
    'search_contact_input': '#app > div > div span > div > span > div div > label > input',
    'contact_list_elements_filtered': '#app > div > div span > div > span > div div > div div > div div > span > span[title][dir]',
    'group_list_elements_filtered': '#app > div > div span > div > span > div div > div div > div div > span[title][dir]',
    'target_focused_title': '#main > header div > div > span[title]',
    'message_area': '#main > footer div.selectable-text[contenteditable]',
    'status':'#main > header > div > div > span[title]'
}


def __exit_if_wrong_url(page, url_to_check):
    if not page.url == url_to_check:
        print("Wrong URL!")
        sys.exit()
        return
# endregion


# region PYPPETEER CONFIGURATION
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
# endregion


# region SELECT TARGET
async def __open_new_chat(page):
    await page.waitForSelector(
        whatsapp_selectors_dict['new_chat_button'],
        visible=True,
        timeout=0
    )
    await page.waitFor(500)
    await page.click(whatsapp_selectors_dict['new_chat_button'])


async def __type_in_search_bar(page, target):
    print(f'Looking for: {target}')
    await page.waitForSelector(
        whatsapp_selectors_dict['search_contact_input'],
        visible=True
    )
    await page.type(whatsapp_selectors_dict['search_contact_input'], target)
    await page.waitFor(3000)


async def __get_contacts_elements_filtered(page, target):
    contact_list_elements_unchecked = list()
    try:
        await page.waitForSelector(
            whatsapp_selectors_dict['contact_list_elements_filtered'],
            visible=True,
            timeout=3000
        )

        contact_list_elements_unchecked = await page.querySelectorAll(
            whatsapp_selectors_dict['contact_list_elements_filtered']
        )
    except:
        print(f'No contact named by "{target}"!')
    return contact_list_elements_unchecked


async def __get_groups_elements_filtered(page, target, hide_groups=False):
    group_list_elements_unchecked = list()

    if hide_groups:
        return group_list_elements_unchecked

    try:
        await page.waitForSelector(
            whatsapp_selectors_dict['group_list_elements_filtered'],
            visible=True,
            timeout=3000
        )

        group_list_elements_unchecked = await page.querySelectorAll(
            whatsapp_selectors_dict['group_list_elements_filtered']
        )
    except:
        print(f'No group named by "{target}"!')
    return group_list_elements_unchecked


async def __get_contacts_titles_from_elements_unchecked(page, contact_list_elements_unchecked):
    contact_titles_unchecked = []
    for i in range(len(contact_list_elements_unchecked)):
        contact_titles_unchecked.append(await page.evaluate(f'document.querySelectorAll("{whatsapp_selectors_dict["contact_list_elements_filtered"]}")[{i}].getAttribute("title")'))
    return contact_titles_unchecked


async def __get_groups_titles_from_elements_unchecked(page, group_list_elements_unchecked):
    group_titles_unchecked = []
    for i in range(len(group_list_elements_unchecked)):
        group_titles_unchecked.append(await page.evaluate(f'document.querySelectorAll("{whatsapp_selectors_dict["group_list_elements_filtered"]}")[{i}].getAttribute("title")'))
    return group_titles_unchecked


# contact_list_unchecked is a zip (list of tuples) of contact_titles and
# contact elements, unchecked.
def __zip_contact_titles_and_elements_unchecked(
    contact_titles_unchecked,
    contact_list_elements_unchecked
):
    contact_list_unchecked = list(zip(
        contact_titles_unchecked, contact_list_elements_unchecked))
    return contact_list_unchecked


def __zip_group_titles_and_elements_unchecked(
    group_titles_unchecked,
    group_list_elements_unchecked
):
    group_list_unchecked = list(
        zip(group_titles_unchecked, group_list_elements_unchecked))
    return group_list_unchecked


# __checking_contact_list verify if target is in title, if not we pop from list
def __check_contact_list(target, contact_list_unchecked):
    i = 0
    while i < len(contact_list_unchecked):
        if len(contact_list_unchecked) <= 0:
            break

        # we can add more verifications if we are getting false-positive contacts
        if contact_list_unchecked[i][0].lower().find(target.lower()) == -1:
            try:
                contact_list_unchecked.pop(i)
            except Exception as e:
                print(f'Error: {str(e)}')
            i -= 1
        i += 1

    contact_tuple = tuple(contact_list_unchecked)
    return contact_tuple


def __check_group_list(target, group_list_unchecked):
    i = 0
    while i < len(group_list_unchecked):
        if len(group_list_unchecked) <= 0:
            break

        # we can add more verifications if we are getting false-positive groups
        if group_list_unchecked[i][0].lower().find(target.lower()) == -1:
            try:
                group_list_unchecked.pop(i)
            except Exception as e:
                print(f'Error: {str(e)}')
            i -= 1
        i += 1

    group_tuple = tuple(group_list_unchecked)
    return group_tuple


# target_list is like that: (((0, 'a'), (1, 'b')), ((3, 'c'), (4, 'd'))),
# but instead numbers and letters we have titles and elements
# the first index is the contacts and the second is the groups
def __get_target_tuple(contact_tuple, group_tuple):
    target_tuple = (contact_tuple, group_tuple)
    return target_tuple


def __print_target_tuple(target_tuple):
    lenght_of_contacts_tuple = len(target_tuple[0])
    lenght_of_groups_tuple = len(target_tuple[1])

    for i in range(lenght_of_contacts_tuple):
        if lenght_of_contacts_tuple <= 0:
            break
        if i == 0:
            print("Contacts found:")
        print(f'{i}: {target_tuple[0][i][0]}')

    for i in range(lenght_of_contacts_tuple, lenght_of_groups_tuple + lenght_of_contacts_tuple):
        if lenght_of_groups_tuple <= 0:
            break
        if i == lenght_of_contacts_tuple:
            print("Groups found:")
        print(f'{i}: {target_tuple[1][i-lenght_of_contacts_tuple][0]}')


def __ask_user_to_choose_the_filtered_target(target_tuple):
    if len(target_tuple[0]+target_tuple[1]) > 0:
        target_index_choosed = int(
            input('Enter the number of the target you wish to choose: '))
    return target_index_choosed


def __get_choosed_target(target_tuple, target_index_choosed):
    lenght_of_contacts_tuple = len(target_tuple[0])
    if target_index_choosed is None:
        sys.exit()

    try:
        if target_index_choosed < lenght_of_contacts_tuple:
            choosed_target = target_tuple[0][target_index_choosed]
        elif target_index_choosed >= lenght_of_contacts_tuple:
            choosed_target = target_tuple[1][target_index_choosed-lenght_of_contacts_tuple]
        else:
            print("This target doesn't exist!")
            sys.exit()
    except Exception as e:
        print(f"This target doesn't exist! Error: {str(e)}")
        sys.exit()
    return choosed_target


async def __navigate_to_target(page, choosed_target):
    try:
        await choosed_target[1].click()
    except Exception as e:
        print(f"This target doesn't exist! Error: {str(e)}")
        sys.exit()


async def __get_focused_target_title(page, target):
    try:
        await page.waitForSelector(whatsapp_selectors_dict['target_focused_title'])
        target_focused_title = await page.evaluate(f'document.querySelector("{whatsapp_selectors_dict["target_focused_title"]}").getAttribute("title")')
    except Exception as e:
        print(f'No target selected! Error: {str(e)}')
        sys.exit()
    return target_focused_title


def __print_selected_target_title(target_focused_title):
    print(f"You've selected the target named by: {target_focused_title}")


def __check_target_focused_title(page, target, target_focused_title):
    if target_focused_title.lower().find(target.lower()) == -1:
        print(f"You're focused in the wrong target, {target_focused_title}")
        must_continue = str(input("Do you want to continue (yes/no)? "))
        accepted_yes = {'yes', 'y'}
        if must_continue.lower() in accepted_yes:
            pass
        else:
            sys.exit()


async def __wait_for_message_area(page):
    try:
        await page.waitForSelector(whatsapp_selectors_dict['message_area'])
    except Exception as e:
        print(f"You don't belong this group anymore! Error: {str(e)}")
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


# region DEV TEST
'''
import asyncio
async def main():
    test_target = 'family'
    pages = await configure_browser_and_load_whatsapp(websites['whatsapp'])
    await search_for_target_and_get_ready_for_conversation(pages[0], test_target)

    message = ask_user_for_message_breakline_mode()
    await send_message(pages[0], message)

asyncio.get_event_loop().run_until_complete(main())
'''
# endregion
