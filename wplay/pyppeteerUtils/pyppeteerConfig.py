__author__ = 'Alexandre Calil Martins Fonseca, github: xandao6'


# region TUTORIAL
'''
Go to region 'FOR SCRIPTING' and use the methods in your script!

EXAMPLE OF USAGE:
from wplay import pyppeteerConfig as pypConfig

'''
# endregion


# region TODO and FIXME
'''

'''
# endregion


# region IMPORTS
# endregion


# region FOR SCRIPTING
import asyncio
from whaaaaat import Validator, ValidationError, Separator
from whaaaaat import style_from_dict, Token, prompt, print_json
from pyppeteer import launch
from pathlib import Path
import shutil
import json
import sys
import os
websites = {'whatsapp': 'https://web.whatsapp.com/'}


def session_mananger():
    #create_data_folder()
    data_filenames = get_data_filenames()
    questions = prepare_questions(data_filenames)
    answers = prompt(questions, style=style)
    print_json(answers)



async def configure_browser_and_load_whatsapp(website):
    session_mananger()
    __patch_pyppeteer()
    browser = await __config_browser('alexandre', save_session=True)
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

'''
0) :create_data_folder
1) Print -> 'Session Mananger' :get_data_filenames
2) Print -> Options
2.1) Restore Session :print_data_filenames
2.2) Go without save a new session
2.3) Save a new session
2.4) Delete sessions
'''
data_folder_path = Path('./wplay/pyppeteerUtils/.userData/')

user_options = {'restore':'Restore a session',
                'save':'Save a new session',
                'continue':'Continue without saving',
                'delete':'Delete a session'}

def prepare_questions(data_filenames):
    questions = [
        {
            'type': 'rawlist',
            'name': 'user_options',
            'message': 'Session Mananger:',
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
            'choices': [*(str(session) for session in data_filenames),'<---Go-back---'],
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
            'choices': list(map(lambda e: {'name':e}, data_filenames)),
            'when': lambda answers: answers['user_options'] == user_options['delete']
        }
        
    ]
    return questions


def get_data_filenames():
    data_filenames = os.listdir(data_folder_path)
    return data_filenames


def verify_answers(answers):
    username=''
    if answers['user_options'] == user_options['restore']:
        if answers['restore'] == '<---Go-back---':
            session_mananger()
        else:
            username = answers['restore'] 
            save_session = True  
    elif answers['user_options'] == user_options['save']:
        username = answers['save'] #verificar se ja existe
        save_session = True
    elif answers['user_options'] == user_options['continue']:
        save_session = False
    elif answers['user_options'] == user_options['delete']:
        if len(answers['delete']) > 0:
            delete_session_data()
    else:
        sys.exit()
    return username, save_session


def delete_session_data(path):
    shutil.rmtree(path)


#def create_data_folder():
#    try:
#        if data_folder_path not in os.listdir(os.getcwd()):
#            os.mkdir(data_folder_path)
#    except:
#        pass

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


async def main():
    pages, browser = await configure_browser_and_load_whatsapp(websites['whatsapp'])
    await pages[0].waitFor(3000)
    await browser.close()
asyncio.get_event_loop().run_until_complete(main())

# endregion
