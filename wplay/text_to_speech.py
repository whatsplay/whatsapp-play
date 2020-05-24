from gtts import gTTS
import os
from wplay.utils.helpers import audio_file_folder_path


async def text_to_speech(target):

    try:
        # The text that you want to convert to audio
        text = input("\n\nWrite the text you want to convert to audio file: ")

        list_laguages=['bn: Bengali', 'de: German', 'en: English','es: Spanish','fr: French','gu: Gujarati','hi: Hindi',
        'it: Italian','ja: Japanese','kn: Kannada','ko: Korean','ml: Malayalam','mr: Marathi','pt-br: Portuguese (Brazil)','ru: Russian',
        'ta: Tamil','te: Telugu','ur: Urdu',]

        print('Choose a code for language of your choice from the following list\n')
        print(list_laguages)

        # Language in which you want to convert
        language = input("\n\nEnter the language you want to convert to audio file: ")
        
        # Passing the text and language to the engine,
        myobj = gTTS(text=text, lang=language, slow=False)
        # Saving the converted audio in a mp3 file named
        myobj.save( audio_file_folder_path / "{}.mp3".format(target))

    except Exception as e:
        print(e)

    # finally:
    #     print(f'\nAudio file saved in: {str(audio_file_folder_path/)}{target}.mp3')