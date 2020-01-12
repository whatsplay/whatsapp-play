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
from whaaaaat import Validator, ValidationError, Separator
from whaaaaat import style_from_dict, Token, prompt
from pyppeteer import launch
from pathlib import Path
import shutil
import json
import sys
import os
# endregion


# region FOR SCRIPTING
websites = {'whatsapp': 'https://web.whatsapp.com/'}


async def configure_browser_and_load_whatsapp(website):
    __patch_pyppeteer()
    username, save_session = __session_mananger()
    browser = await __config_browser(username, save_session)
    pages = await __get_pages(browser)
    await __open_website(pages[0], website)
    return pages, browser
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
def __exit_if_wrong_url(page, url_to_check):
    if not page.url == url_to_check:
        print("Wrong URL!")
        sys.exit()
        return
# endregion


# region PYPPETEER CONFIGURATION
async def __config_browser(username='', save_session=True):
    if username != '' and save_session:
        return await launch(
            headless=False,
            autoClose=False,
            userDataDir=f'{data_folder_path}/{username}'
        )
    else:
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


# region SESSION MANAGEMENT
style = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


data_folder_path = Path(os.getcwd())/Path('wplay/pyppeteerUtils/.userData/')


user_options = {'restore': 'Restore a session',
                'save': 'Create a new session',
                'continue': 'Continue without saving',
                'delete': 'Delete a session'}


def __session_mananger():
    __create_data_folder()
    data_filenames = __get_data_filenames()
    questions_menu, question_overwrite = __prepare_questions(data_filenames)
    try:
        answers_menu = prompt(questions_menu, style=style)
    except:
        __session_mananger()
    username, save_session = __verify_answers(answers_menu, data_filenames, question_overwrite)
    return username, save_session


def __create_data_folder():
    try:
        if data_folder_path not in os.listdir(os.getcwd()):
            os.mkdir(data_folder_path)
    except:
        pass


def __get_data_filenames():
    data_filenames = os.listdir(data_folder_path)
    return data_filenames


def __delete_session_data(path):
    shutil.rmtree(path)


def __verify_if_session_file_exists(data_filenames, username, question_overwrite):
    if username in data_filenames:
        answer_overwrite = prompt(question_overwrite, style=style)
        if answer_overwrite['overwrite_data']:
            __delete_session_data(data_folder_path/username)
        else:
            __session_mananger()


def __prepare_questions(data_filenames):
    questions_menu = [
        {
            'type': 'rawlist',
            'name': 'user_options',
            'message': '***Session Mananger***:',
            'choices': [
                Separator(),
                user_options['restore'],
                user_options['save'],
                user_options['continue'],
                Separator(),
                user_options['delete'],
                Separator()
            ]
        },
        {
            'type': 'rawlist',
            'name': 'restore',
            'message': 'Select a session to try to restore:',
            'choices': [*(str(session) for session in data_filenames), '<---Go-back---'],
            'when': lambda answers: answers['user_options'] == user_options['restore']
        },
        {
            'type': 'input',
            'name': 'save',
            'message': 'Write your first name or username to save:',
            'when': lambda answers: answers['user_options'] == user_options['save']
        },
        {
            'type': 'checkbox',
            'name': 'delete',
            'message': 'Mark the sessions you want to delete:',
            'choices': list(map(lambda e: {'name': e}, data_filenames)),
            'when': lambda answers: answers['user_options'] == user_options['delete']
        }
    ]

    question_overwrite = [
        {
            'type': 'confirm',
            'name': 'overwrite_data',
            'message': 'There is already a session with that name, overwrite it?',
            'default': True
        }
    ]

    return questions_menu, question_overwrite


def __verify_answers(answers_menu, data_filenames, question_overwrite):
    username = ''; save_session = None
    if answers_menu['user_options'] == user_options['restore']:
        if answers_menu['restore'] == '<---Go-back---':
            __session_mananger()
        else:
            username = answers_menu['restore']
            save_session = True
    elif answers_menu['user_options'] == user_options['save']:
        username = answers_menu['save']  # verificar se ja existe
        save_session = True
        __verify_if_session_file_exists(data_filenames, username, question_overwrite)
    elif answers_menu['user_options'] == user_options['continue']:
        save_session = False
    elif answers_menu['user_options'] == user_options['delete']:
        if len(answers_menu['delete']) > 0:
            for el in answers_menu['delete']:
                __delete_session_data(data_folder_path/el)
        __session_mananger()
    else:
        __session_mananger()
    return username, save_session
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
    pages, browser = await configure_browser_and_load_whatsapp(websites['whatsapp'])
    await pages[0].waitFor(3000)
    await browser.close()
asyncio.get_event_loop().run_until_complete(main())
'''
# endregion
