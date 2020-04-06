# region IMPORTS
import argparse
import asyncio
import sys
import os
from pathlib import Path

from pyfiglet import Figlet

from wplay import online_tracker
from wplay import message_blast
from wplay import message_timer
from wplay import terminal_chat
from wplay import save_chat
from wplay import telegram_bot
from wplay import schedule_message
from wplay import about_changer
from wplay import get_news
from wplay import get_media
from wplay.utils.Logger import Logger
from wplay.utils.helpers import create_dirs
from wplay.utils.helpers import kill_child_processes
# endregion


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


def print_logo(text_logo):
    figlet = Figlet(font='slant')
    print(figlet.renderText(text_logo))


# parse positional and optional arguments
def get_arg_parser():
    parser = argparse.ArgumentParser(description = 'WhatsApp-play')
    parser.add_argument(
        "target",
        metavar="TARGET",
        type=str,
        default=None,
        nargs="?",
        help="contact or group name, optional , target can be selected manually except for saving chat")

    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument(
        "-wc",
        "--terminal-chat",
        action = "store_true",
        help = "chatting from command line")

    group.add_argument(
        "-wb",
        "--message-blast",
        action = "store_true",
        help = "message blast to a person")

    group.add_argument(
        "-wti",
        "--message-timer",
        action = "store_true",
        help = "send messages from time to time")

    group.add_argument(
        "-wt",
        "--online-tracker",
        action = "store_true",
        help = "track online status of person")

    group.add_argument(
        "-wtb",
        "--telegram-bot",
        action = "store_true",
        help = "sends tracking status to telegram bot")

    group.add_argument(
        "-pull",
        "--pull",
        action = "store_true",
        help = "save all chats from Google Drive, target is necessary")

    group.add_argument(
        "-ws",
        "--schedule-message",
        action = "store_true",
        help = "send the message at scheduled time")

    group.add_argument(
        "-wa",
        "--about-changer",
        action = "store_true",
        help = "Changes the about section"
    )

    group.add_argument(
        "-wgn",
        "--get-news",
        action = "store_true",
        help = "Get news in whatsapp group"
    )

    group.add_argument(
        "-wgp",
        "--get-profile-photos",
        action = "store_true",
        help = "Get profile photo of all your contacts"
    )

    # group.add_argument(
    #     "-wl",
    #     "--wlocation",
    #     action = "store_true",
    #     help = "finds the location of the person")

    return parser


# functions for different arguments
async def get_and_match_args(parser):
    args = parser.parse_args()
    if args.online_tracker:
        await online_tracker.tracker(args.target)

    elif args.telegram_bot:
        telegram_bot.telegram_status(args.target)

    elif args.terminal_chat:
        await terminal_chat.chat(args.target)

    elif args.message_blast:
        await message_blast.message_blast(args.target)

    elif args.message_timer:
        await message_timer.message_timer(args.target)

    elif args.save_gdrive_chats:
        if args.target is None:
            parser.print_help()
            parser.exit()
        try:
            bID : int = int(sys.argv[3])
        except (IndexError, ValueError):
            bID : int = 0
        save_chat.runMain('pull', str(args.target), bID)

    elif args.schedule_message:
        await schedule_message.schedule_message(args.target)

    elif args.about_changer:
        await about_changer.about_changer()

    elif args.get_news:
        await get_news.get_news(args.target)

    elif args.get_profile_photos:
        await get_media.get_profile_photos()

    # elif args.wlocation:
    #     loactionfinder.finder(args.target)


async def main():
    print_logo("wplay")
    create_dirs()
    parser = get_arg_parser()
    try:
        await get_and_match_args(parser)
        sys.exit(0)
    except KeyboardInterrupt:
        __logger.error('User Pressed Ctrl+C')
        sys.exit(0)


try:
    asyncio.get_event_loop().run_until_complete(main())
except KeyboardInterrupt:
        __logger.error('User Pressed Ctrl+C')
except AssertionError:
    try:
        for task in asyncio.all_tasks():
            task.cancel()
    except RuntimeError:
        exit()
    exit()
finally:
    kill_child_processes(os.getpid())
