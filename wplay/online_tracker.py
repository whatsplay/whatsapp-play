import time
from pathlib import Path
from datetime import datetime
from playsound import playsound
from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import target_select
from wplay.utils import target_data
from wplay.utils.helpers import tracking_folder_path
from wplay.utils.Logger import Logger
from wplay.utils.helpers import logs_path


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


async def tracker(target):
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    if target is not None:
        try:
            target_name = await target_search.search_and_select_target(page, target, hide_groups = True)
        except Exception as e:
            print(e)
            await page.reload()
            target_name = await target_search.search_and_select_target_without_new_chat_button(page,target,hide_groups=True)
    else:
        target_name = await target_select.manual_select_target(page, hide_groups = True)
    
    status_file : str = open(tracking_folder_path / f'status_{target_name}.txt', 'w').close()
    status_file : str = open(tracking_folder_path / f'status_{target_name}.txt', 'a')

    is_sound_enabled : bool = True
    last_status : str = 'offline'
    try:
        print(f'Tracking: {target_name}')
        __logger.info("Tracking target")
        status_file.write(f'Tracking: {target_name}\n')
        while True:
            status : str = await target_data.get_last_seen_from_focused_target(page)
            if status == 'online':
                is_online : bool = True
            else:
                is_online : bool = False
                status : str = 'offline'
            if last_status != is_online:
                if is_online:
                    try:
                        if is_sound_enabled:
                            playsound('plucky.wav')
                    except:
                        print("Error: Couldn't play the sound.")
                        is_sound_enabled : bool = False
                print(
                    f'{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}' + f' - Status: {status}'
                )
                status_file.write(
                    f'{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}' + f' - Status: {status}\n')
            last_status : str = is_online
            time.sleep(0.5)
    except KeyboardInterrupt:
        __logger.error("User Pressed Ctrl+C")
    finally:
        status_file.close()
        print(f'\nStatus file saved in: {str(tracking_folder_path/"status_")}{target_name}.txt')
