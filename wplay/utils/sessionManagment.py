from whaaaaat import Validator, ValidationError, Separator
from whaaaaat import style_from_dict, Token, prompt
from pathlib import Path

from wplay.utils.helpers import whatsapp_selectors_dict, websites
from wplay.utils.helpers import user_data_folder_path, data_folder_path

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


user_options = {'restore': 'Restore a session',
                'save': 'Create a new session',
                'continue': 'Continue without saving',
                'delete': 'Delete a session'}


def __session_manager():
    __create_data_folder()
    __create_user_data_folder()
    data_filenames = __get_user_data_filenames()
    try:
        questions_menu, question_overwrite = __prepare_questions(data_filenames)
        answers_menu = prompt(questions_menu, style=style)
        username, save_session = __verify_answers(answers_menu, data_filenames, question_overwrite)
    except:
        __session_manager()
    return username, save_session


def __create_data_folder():
    if not os.path.isdir(data_folder_path):
        os.mkdir(data_folder_path)


def __create_user_data_folder():
    if not os.path.isdir(user_data_folder_path):
        os.mkdir(user_data_folder_path)


def __get_user_data_filenames():
    data_filenames = os.listdir(user_data_folder_path)
    return data_filenames


def __delete_session_data(path):
    shutil.rmtree(path)


def __verify_if_session_file_exists(data_filenames, username, question_overwrite):
    if username in data_filenames:
        answer_overwrite = prompt(question_overwrite, style=style)
        if answer_overwrite['overwrite_data']:
            __delete_session_data(data_folder_path/username)
        else:
            __session_manager()


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
            __session_manager()
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
        __session_manager()
    else:
        __session_manager()
    return username, save_session
# endregion