import time
import os
from datetime import datetime
from playsound import playsound
from wplay import pyppeteerUtils as pyp


async def tracker(target):
    #target = str(input("Enter the name of target: "))

    pages = await pyp.configure_browser_and_load_whatsapp(pyp.websites['whatsapp'])
    await pyp.search_for_target_and_get_ready_for_conversation(pages[0], target, hide_groups=True)

    # finds if online_status directory is present
    if 'tracking_data' not in os.listdir(os.getcwd()):
        os.mkdir('tracking_data')

    # create status.txt file and overwrite if exists
    status_file = open(
        os.path.join('tracking_data', f'status_{target}.txt'), 'w'
    )
    status_file.close()

    # open status.txt in memory with append mode
    status_file = open(
        os.path.join('tracking_data', f'status_{target}.txt'), 'a'
    )

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
              f'{os.path.join(os.getcwd(),"tracking_data")}')
