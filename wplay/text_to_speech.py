# region IMPORTS
from pathlib import Path

from wplay.utils.helpers import audio_file_folder_path
from wplay.utils.Logger import Logger

from gtts import gTTS
from tkinter import *
from tkinter.ttk import * 
from tkinter.filedialog import askopenfile 
# endregion


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion

def open_file():
    file = askopenfile(mode ='r', filetypes =[('Text Files', '*.txt')])
    open_file.path = file.name

async def text_to_speech(target):

    try:
        option = input("Choose(1/2) \n1.Convert text to speech \n2.To Convert a text file into spech\n")

        list_laguages=['bn: Bengali', 'de: German', 'en: English','es: Spanish','fr: French','gu: Gujarati','hi: Hindi',
            'it: Italian','ja: Japanese','kn: Kannada','ko: Korean','ml: Malayalam','mr: Marathi','pt-br: Portuguese (Brazil)','ru: Russian',
            'ta: Tamil','te: Telugu','ur: Urdu',]

        print('Choose a code for language of your choice from the following list\n')
        print(list_laguages)

        # Language in which you want to convert
        language = input("\n\nEnter the language you want to convert to audio file: ")

        if option == '1':
            __logger.info("Converting text to speech audio file")
            # The text that you want to convert to audio
            text = input("\n\nWrite the text you want to convert to audio file: ")

            # Passing the text and language to the engine,
            myobj = gTTS(text=text, lang=language, slow=False)
            # Saving the converted audio in a mp3 file named
            myobj.save( audio_file_folder_path / "{}.mp3".format(target))

        else :
            __logger.info("Converting text file to speech audio file")
            root = Tk() 
            root.geometry('200x100')
            btn = Button(root, text ='Open', command = lambda: open_file()) 
            btn.pack(side = TOP, pady = 10) 
            pathlabel = Label(root)
            pathlabel.pack()
            mainloop()
            print('\nYou choose file {}'.format(open_file.path))
            file = open(open_file.path, "r").read().replace("\n", " ")
            speech = gTTS(text = str(file), lang = language, slow = False)
            speech.save(audio_file_folder_path / "{}.mp3".format(target))

    except Exception as e:
        print(e)

    finally:
        print('\nAudio file saved in: {}/ {}.mp3'.format(audio_file_folder_path, target))