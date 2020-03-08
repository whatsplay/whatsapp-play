# These lines import python library files.
import time
from pathlib import Path
from datetime import datetime
from playsound import playsound

# These import from util folder in wplay
from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import target_data
from wplay.utils.helpers import data_folder_path

# After the client run the command line script, the user enters a name and that is the target which is used here.
async def tracker(target):
# Waiting for Whatsapp web to be loading
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
# Searching for the target name 
    target_name = await target_search.search_and_select_target(page, target, hide_groups = True)
    Path(data_folder_path / 'tracking_data').mkdir(parents = True, exist_ok = True)
    
    status_file = open(data_folder_path / 'tracking_data' / f'status_{target_name}.txt', 'w').close()
    status_file = open(data_folder_path / 'tracking_data' / f'status_{target_name}.txt', 'a')

    is_sound_enabled = True
    
    last_status = 'offline'
    try:
# After username is found it prints the various name if matching strings are there and asks the user for which name to track and sets that name to target.
        print(f'Tracking: {target_name}')
# It writes the status whether offline or online in tracking file.
        
# Checks for the status and plays the sound for confirmation
        status_file.write(f'Tracking: {target_name}\n')
        while True:
            status = await target_data.get_last_seen_from_focused_target(page)
            if status == 'online':
                is_online = True
            else:
                is_online = False
                status = 'offline'
            if last_status != is_online:
                if is_online:
                    try:
                        if is_sound_enabled:
                            playsound('plucky.wav')
                    except:
                        print("Error: Couldn't play the sound.")
                        is_sound_enabled = False
                print(
                    f'{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}' + f' - Status: {status}'
                )
                status_file.write(
                    f'{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}' + f' - Status: {status}\n')
            last_status = is_online
            time.sleep(0.5)
    finally:
        status_file.close()
        #The final status of the operations that is the tracking data is stored in tracking data file.
        print(f'\nStatus file saved in: {str(data_folder_path/"tracking_data"/"status_")}{target_name}.txt')
