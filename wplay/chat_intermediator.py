# region IMPORTS
from wplay import terminal_chat
from wplay.utils.Logger import Logger

from pathlib import Path
# endregion

# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


async def intermediary(target):
    __logger.info("Being and Intermediator")
    intermediary.rec = target[1]
    await terminal_chat.chat(target[0])
