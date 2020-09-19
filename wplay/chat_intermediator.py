# region IMPORTS
from wplay import terminal_chat
from wplay.utils.Logger import Logger

from pathlib import Path
# endregion

# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


async def intermediary(sender, receiver):
    """
    Function to create intermediate between two person.
    """
    __logger.info("Being and Intermediator")
    intermediary.rec = receiver
    await terminal_chat.chat(sender)
