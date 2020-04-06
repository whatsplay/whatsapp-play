# region IMPORTS
from datetime import datetime
from pathlib import Path
import time
import sys

from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import target_select
from wplay.utils import io
from wplay.utils.Logger import Logger
# endregion


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


async def schedule_message(target):
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    if target is not None:
        await target_search.search_and_select_target(page, target)
    else:
        await target_select.manual_select_target(page)
    time_ = input("Enter the schedule time in HH:MM:SS format-> ")
    hour, minute, second = time_.split(':')
    current_time = datetime.now()
    delta_hour : int = int(hour) - current_time.hour
    delta_min : int = int(minute) - current_time.minute
    delta_second : int = int(second) - current_time.second
    total_seconds : int = delta_hour*3600 + delta_min*60 + delta_second
    if total_seconds < 0:
        print("Current time is ahead of the scheduled time")
        sys.exit()
    message : list[str] = io.ask_user_for_message_breakline_mode()
    print("Your message is scheduled at : ", time_)
    time.sleep(total_seconds)
    await io.send_message(page, message)
