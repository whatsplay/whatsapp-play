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
from wplay.utils.helpers import whatsapp_selectors_dict
# endregion


# region FOR SCRIPTING
async def search_and_select_target(page, target, hide_groups=False):
    await __open_new_chat(page)
    await __type_in_new_chat_search_bar(page, target)
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

    return target_focused_title
# endregion


# region SEARCH AND SELECT TARGET
async def __open_new_chat(page):
    await page.waitForSelector(
        whatsapp_selectors_dict['new_chat_button'],
        visible=True,
        timeout=0
    )
    await page.waitFor(500)
    await page.click(whatsapp_selectors_dict['new_chat_button'])


async def __type_in_new_chat_search_bar(page, target):
    print(f'Looking for: {target}')
    await page.waitForSelector(
        whatsapp_selectors_dict['search_contact_input_new_chat'],
        visible=True
    )
    await page.type(whatsapp_selectors_dict['search_contact_input_new_chat'], target)
    await page.waitFor(3000)


async def __get_contacts_elements_filtered(page, target):
    contact_list_elements_unchecked = list()
    try:
        await page.waitForSelector(
            whatsapp_selectors_dict['contact_list_elements_filtered_new_chat'],
            visible=True,
            timeout=3000
        )

        contact_list_elements_unchecked = await page.querySelectorAll(
            whatsapp_selectors_dict['contact_list_elements_filtered_new_chat']
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
            whatsapp_selectors_dict['group_list_elements_filtered_new_chat'],
            visible=True,
            timeout=3000
        )

        group_list_elements_unchecked = await page.querySelectorAll(
            whatsapp_selectors_dict['group_list_elements_filtered_new_chat']
        )
    except:
        print(f'No group named by "{target}"!')
    return group_list_elements_unchecked


async def __get_contacts_titles_from_elements_unchecked(page, contact_list_elements_unchecked):
    contact_titles_unchecked = []
    for i in range(len(contact_list_elements_unchecked)):
        contact_titles_unchecked.append(await page.evaluate(f'document.querySelectorAll("{whatsapp_selectors_dict["contact_list_elements_filtered_new_chat"]}")[{i}].getAttribute("title")'))
    return contact_titles_unchecked


async def __get_groups_titles_from_elements_unchecked(page, group_list_elements_unchecked):
    group_titles_unchecked = []
    for i in range(len(group_list_elements_unchecked)):
        group_titles_unchecked.append(await page.evaluate(f'document.querySelectorAll("{whatsapp_selectors_dict["group_list_elements_filtered_new_chat"]}")[{i}].getAttribute("title")'))
    return group_titles_unchecked


# contact_list_unchecked is a zip (list of tuples) of contact_titles and
# contact elements, unchecked.
def __zip_contact_titles_and_elements_unchecked(contact_titles_unchecked, contact_list_elements_unchecked):
    contact_list_unchecked = list(zip(contact_titles_unchecked, contact_list_elements_unchecked))
    return contact_list_unchecked


def __zip_group_titles_and_elements_unchecked(group_titles_unchecked, group_list_elements_unchecked):
    group_list_unchecked = list(zip(group_titles_unchecked, group_list_elements_unchecked))
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
    if len(target_tuple[0] + target_tuple[1]) > 0:
        target_index_choosed = int(
            input('Enter the number of the target you wish to choose: '))
    return target_index_choosed


def __get_choosed_target(target_tuple, target_index_choosed):
    lenght_of_contacts_tuple = len(target_tuple[0])
    if target_index_choosed is None:
        exit()

    try:
        if target_index_choosed < lenght_of_contacts_tuple:
            choosed_target = target_tuple[0][target_index_choosed]
        elif target_index_choosed >= lenght_of_contacts_tuple:
            choosed_target = target_tuple[1][target_index_choosed - lenght_of_contacts_tuple]
        else:
            print("This target doesn't exist!")
            exit()
    except Exception as e:
        print(f"This target doesn't exist! Error: {str(e)}")
        exit()
    return choosed_target


async def __navigate_to_target(page, choosed_target):
    try:
        await choosed_target[1].click()
    except Exception as e:
        print(f"This target doesn't exist! Error: {str(e)}")
        exit()


async def __get_focused_target_title(page, target):
    try:
        await page.waitForSelector(whatsapp_selectors_dict['target_focused_title'])
        target_focused_title = await page.evaluate(f'document.querySelector("{whatsapp_selectors_dict["target_focused_title"]}").getAttribute("title")')
    except Exception as e:
        print(f'No target selected! Error: {str(e)}')
        exit()
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
            exit()


async def __wait_for_message_area(page):
    try:
        await page.waitForSelector(whatsapp_selectors_dict['message_area'])
    except Exception as e:
        print(f"You don't belong this group anymore! Error: {str(e)}")
# endregion
