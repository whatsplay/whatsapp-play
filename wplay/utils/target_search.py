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
from wplay.utils import Logger
from wplay.utils.helpers import logs_path
from pyppeteer.errors import ElementHandleError
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
    if any(choosed_target[0] in i for i in contact_tuple):
        complete_target_info = await get_complete_info_on_target(page)
        print_complete_target_info(complete_target_info)
        await close_contact_info_page(page)
    else:
        __print_selected_target_title(target_focused_title)
    __check_target_focused_title(page, target, target_focused_title)
    await __wait_for_message_area(page)
    return target_focused_title


async def search_and_select_target_without_new_chat_button(page,target, hide_groups=False):
    await __type_in_chat_or_message_search(page,target)
    chats_messages_groups_elements_list = await __get_chats_messages_groups_elements(page)
    contact_name_index_tuple_list = await __get_contacts_matched_with_query(chats_messages_groups_elements_list)
    group_name_index_tuple_list = await __get_groups_matched_with_query(chats_messages_groups_elements_list,hide_groups)
    target_tuple = (contact_name_index_tuple_list,group_name_index_tuple_list)
    __print_target_tuple(target_tuple)
    target_index_chosen = __ask_user_to_choose_the_filtered_target(target_tuple)

    #chosen_target will be a tuple (a,b) such that a is the name of the target and b is the
    #index of that element in chats_messages_groups_elements_list

    chosen_target = __get_choosed_target(target_tuple, target_index_chosen)
    await __open_selected_chat(chosen_target[1],chats_messages_groups_elements_list)
    target_name = chosen_target[0]
    if any(chosen_target[0] in i for i in contact_name_index_tuple_list):
        complete_target_info = await get_complete_info_on_target(page)
        print_complete_target_info(complete_target_info)
        await close_contact_info_page(page)
    else:
        __print_selected_target_title(target_name)
    await __wait_for_message_area(page)
    return target_name


# endregion


#region LOGGER create
logger : Logger = Logger.setup_logger('logs',logs_path/'logs.log')
#endregion


# region SEARCH AND SELECT TARGET
async def __type_in_chat_or_message_search(page,target):
    try:
        print(f'Looking for: {target}')
        await page.waitForSelector(
            whatsapp_selectors_dict['chat_or_message_search'],
            visible=True,
            timeout=0
        )
        await page.waitFor(500)
        await page.type(whatsapp_selectors_dict['chat_or_message_search'], target)
        await page.waitFor(3000)
    except Exception as e:
        print(e)


async def __get_chats_messages_groups_elements(page):
    chats_messages_groups_elements_list = []  # type : list[int]
    try:
        chats_messages_groups_elements_list = await page.querySelectorAll\
            (whatsapp_selectors_dict['chats_groups_messages_elements'])
        return chats_messages_groups_elements_list
    except Exception as e:
        print(e)
        exit()


async def __get_contacts_matched_with_query(chats_groups_messages_elements_list):
    contacts_to_choose_from = []  # type : list[str , int]
    get_contact_node_title_function = 'node => node.parentNode.getAttribute("title")'
    for idx, element in enumerate(chats_groups_messages_elements_list):
        try:
            contact_name = await element.querySelectorEval(whatsapp_selectors_dict['contact_element'],get_contact_node_title_function)
            contacts_to_choose_from.append((contact_name,idx))
        except ElementHandleError:
            # if it is not a contact element, move to the next one
            continue
        except Exception as e:
            print(e)

    return contacts_to_choose_from


async def __get_groups_matched_with_query(chats_groups_messages_elements_list,hide_groups):
    groups_to_choose_from = []

    if hide_groups:
        return groups_to_choose_from

    get_group_node_title_function = 'node => node.parentNode.getAttribute("title")'
    for idx, element in enumerate(chats_groups_messages_elements_list):
        try:
            group_name = await element.querySelectorEval(whatsapp_selectors_dict['group_element'],
                                                         get_group_node_title_function)
            groups_to_choose_from.append((group_name,idx))
        except ElementHandleError:
            # if it is not a contact element, move to the next one
            continue
        except Exception as e:
            print(e)

    return groups_to_choose_from


async def __open_selected_chat(target_index,chats_messages_groups_elements_list):
    try:
        await chats_messages_groups_elements_list[target_index].click()
    except Exception as e:
        print(f"This target doesn't exist! Error: {str(e)}")
        exit()


async def get_complete_info_on_target(page):
    contact_page_elements = []
    try:
        await page.waitForSelector(
            whatsapp_selectors_dict['target_chat_header'],
            visible=True,
            timeout=3000
        )
        await page.click(whatsapp_selectors_dict['target_chat_header'])
        contact_page_elements = await get_contact_page_elements(page)
        complete_target_info = {}
        await get_contact_name_info(contact_page_elements[0], complete_target_info)
        await get_contact_about_and_phone(contact_page_elements[3], complete_target_info)
        await get_contact_groups_common_with_target(complete_target_info, page)
    except Exception as e:
        print(e)
    return complete_target_info


async def get_contact_page_elements(page):
    contact_page_elements = []
    try:
        await page.waitForSelector(
            whatsapp_selectors_dict['contact_info_page_elements'],
            visible=True,
            timeout=8000
        )
        contact_page_elements = await page.querySelectorAll(whatsapp_selectors_dict['contact_info_page_elements'])
    except Exception as e:
        print(e)
    return contact_page_elements


async def get_contact_name_info(contact_name_element,complete_target_info):
    try:
        complete_target_info['Name'] = await contact_name_element.querySelectorEval('span > span', 'element => element.innerText')
        complete_target_info['Last_seen'] = await contact_name_element.querySelectorEval('div > span:last-of-type > div > span', 'element => element.getAttribute("title")')
    except:
        print(f'last seen not available')


async def get_contact_about_and_phone(contact_name_element, complete_target_info):
    try:
        complete_target_info['About'] = await contact_name_element.querySelectorEval('div:nth-child(2) > div > div > span > span', 'element => element.getAttribute("title")')
        complete_target_info['Mobile'] = await contact_name_element.querySelectorEval('div:last-of-type > div > div > span > span', 'element => element.innerText')
    except Exception as e:
        print(e)


async def get_contact_groups_common_with_target(complete_target_info,page):
    try:
        await page.waitForSelector(
            whatsapp_selectors_dict['contact_info_page_group_element_heading'],
            visible= True,
            timeout=3000
        )

        if (await page.evaluate(f'document.querySelector("{whatsapp_selectors_dict["contact_info_page_group_element_heading"]}").innerText'))\
               == "Groups in common":
            group_elements = await page.querySelectorAll(whatsapp_selectors_dict['contact_info_page_group_elements'])
            complete_target_info['Groups'] = [await ele.querySelectorEval('div>div>div:nth-child(2)>div:first-child>div>div>span', 'e => e.getAttribute("title")') for ele in group_elements]
        else:
            complete_target_info['Groups'] = []
    except:
        complete_target_info['Groups'] = []
        print(f'No groups in common')


async def close_contact_info_page(page):
    try:
        await page.waitForSelector(
            whatsapp_selectors_dict['contact_info_page_close_button'],
            visible = True,
            timeout = 5000
        )
        await page.click(whatsapp_selectors_dict['contact_info_page_close_button'])
    except Exception as e:
        print(e)


def print_complete_target_info(complete_target_info):
    for key in complete_target_info.keys():
        if key == "Groups":
            print("Groups:")
            print(*complete_target_info[key], sep=",")
        else:
            print(f'{key}: {complete_target_info[key]} ')


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
    logger.info('Searching Target')
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
        logger.info('Target not found')
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
        logger.info('Target not found in groups')
    return group_list_elements_unchecked


async def __get_contacts_titles_from_elements_unchecked(page, contact_list_elements_unchecked):
    contact_titles_unchecked = []
    for i in range(len(contact_list_elements_unchecked)):
        contact_titles_unchecked\
            .append(await page.evaluate(f'document.querySelectorAll("{whatsapp_selectors_dict["contact_list_elements_filtered_new_chat"]}")[{i}].getAttribute("title")'))
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
            logger.info('List of Targets')
        print(f'{i}: {target_tuple[0][i][0]}')

    for i in range(lenght_of_contacts_tuple, lenght_of_groups_tuple + lenght_of_contacts_tuple):
        if lenght_of_groups_tuple <= 0:
            break
        if i == lenght_of_contacts_tuple:
            print("Groups found:")
            logger.info('List of Target in groups')
        print(f'{i}: {target_tuple[1][i-lenght_of_contacts_tuple][0]}')


def __ask_user_to_choose_the_filtered_target(target_tuple):
    if len(target_tuple[0] + target_tuple[1]) > 0:
        logger.info('Input Target Number')
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
            logger.error('Invalid Target')
            exit()
    except Exception as e:
        print(f"This target doesn't exist! Error: {str(e)}")
        logger.error('Invalid Target')
        exit()
    return choosed_target


async def __navigate_to_target(page, choosed_target):
    try:
        await choosed_target[1].click()
    except Exception as e:
        print(f"This target doesn't exist! Error: {str(e)}")
        logger.error('Invalid Target')
        exit()


async def __get_focused_target_title(page, target):
    try:
        await page.waitForSelector(whatsapp_selectors_dict['target_focused_title'])
        target_focused_title = await page.evaluate(f'document.querySelector("{whatsapp_selectors_dict["target_focused_title"]}").getAttribute("title")')
    except Exception as e:
        print(f'No target selected! Error: {str(e)}')
        logger.error('Target not selected from list')
        exit()
    return target_focused_title


def __print_selected_target_title(target_focused_title):
    print(f"You've selected the target named by: {target_focused_title}")
    logger.info('Selected Target')


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
