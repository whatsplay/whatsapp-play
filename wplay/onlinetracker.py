import time
import os
from datetime import datetime
from playsound import playsound
from pathlib import Path
from wplay.pyppeteerUtils import pyppeteerConfig as pypConfig
from wplay.pyppeteerUtils import pyppeteerSearch as pypSearch

#BUG
async def tracker(target):
    #target = str(input("Enter the name of target: "))

    pages, browser = await pypConfig.configure_browser_and_load_whatsapp(pypConfig.websites['whatsapp'])

    try:
        target_name = await pypSearch.search_for_target_and_get_ready_for_conversation(pages[0], target, hide_groups=True)

        # finds if online_status directory is present
        if not os.path.isdir(pypConfig.data_folder_path/'tracking_data'):
            os.mkdir(pypConfig.data_folder_path/'tracking_data')

        # create status.txt file and overwrite if exists
        status_file = open(pypConfig.data_folder_path/
                           'tracking_data'/f'status_{target_name}.txt', 'w')
        status_file.close()

        # open status.txt in memory with append mode
        status_file = open(pypConfig.data_folder_path/
                           'tracking_data'/f'status_{target_name}.txt', 'a')

        # check status
        is_sound_enabled = True
        last_status = 'offline'
        try:
            while True:
                status = await pyp.get_status_from_focused_target(pages[0])
                if status == 'online':
                    is_online = True
                else:
                    # status is last seen
                    is_online = False
                    status = 'offline'

                if last_status != is_online:
                    # play sound when the person is online
                    if is_online:
                        try:
                            if is_sound_enabled:
                                playsound('plucky.wav')
                        except:
                            print("Error: Couldn't play the sound.")
                            is_sound_enabled = False

                    # print date, time and status to console
                    print(
                        f'{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}' +
                        f' - Status: {status}'
                    )

                    # writes date, time and status in status.txt
                    status_file.write(
                        f'{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}' +
                        f' - Status: {status}\n')

                last_status = is_online
                time.sleep(0.5)
        finally:
            status_file.close()
            print(f'\nStatus file saved in: ' +
                  str(pypConfig.data_folder_path/'tracking_data'/f'status_{target_name}.txt'))
    except:
        await browser.close()
