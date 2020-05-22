from wplay import terminal_chat

async def intermediary(sender, receiver):
    intermediary.rec = receiver
    await terminal_chat.chat(sender)
