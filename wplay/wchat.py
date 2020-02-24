from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import io

async def chat(target):
    page, _ = await browser_config.configure_browser_and_load_whatsapp()

    await target_search.search_and_select_target(page, target)

    while True:
        message = io.ask_user_for_message_breakline_mode()
        await io.send_message(page, message)
