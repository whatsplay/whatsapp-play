import os
import shutil
from pathlib import Path
from whaaaaat import Validator, ValidationError, Separator, prompt

from wplay.utils.helpers import whatsapp_selectors_dict, websites
from wplay.utils.helpers import user_data_folder_path, data_folder_path
from wplay.utils.helpers import menu_style

# region SESSION MANAGEMENT
user_options = {'restore': 'Restore a session',
                'save': 'Create a new session',
                'continue': 'Continue without saving',
                'delete': 'Delete a session'}


def session_manager():
    __create_user_data_folder()
    data_filenames = __get_user_data_filenames()
    try:
        questions_menu, question_overwrite = __prepare_questions(data_filenames)
        answers_menu = prompt(questions_menu, style=menu_style)
        username, save_session = __verify_answers(answers_menu, data_filenames, question_overwrite)
    except:
        session_manager()
    return username, save_session


def __create_user_data_folder():
    Path(user_data_folder_path).mkdir(parents=True, exist_ok=True)


def __get_user_data_filenames():
    data_filenames = os.listdir(user_data_folder_path)
    return data_filenames


def __delete_session_data(path):
    shutil.rmtree(path)


def __verify_if_session_file_exists(data_filenames, username, question_overwrite):
    if username in data_filenames:
        answer_overwrite = prompt(question_overwrite, style=menu_style)
        if answer_overwrite['overwrite_data']:
            __delete_session_data(data_folder_path/username)
        else:
            session_manager()


def __prepare_questions(data_filenames):
    questions_menu = [
        {
            'type': 'rawlist',
            'name': 'user_options',
            'message': '***Session Manager***:',
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
            session_manager()
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
        session_manager()
    else:
        session_manager()
    return username, save_session
# endregions