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
from wplay import chat_intermediator
from wplay import broadcast_message
from wplay import save_chat
from wplay import telegram_bot
from wplay import schedule_message
from wplay import about_changer
from wplay import get_news
from wplay import get_media
from wplay import download_media
from wplay import message_service
from wplay import target_info
from wplay import profile_download
from wplay.utils.Logger import Logger
from wplay.utils.helpers import create_dirs
from wplay.utils.helpers import kill_child_processes
# endregion


def print_logo(text_logo):
    figlet = Figlet(font='slant')
    print(figlet.renderText(text_logo))


# parse positional and optional arguments
def get_arg_parser():
    parser = argparse.ArgumentParser(description='WhatsApp-play')
    parser.add_argument(
        "target",
        metavar="TARGET",
        type=str,
        default=None,
        nargs="?",
        help="""contact or group name, optional,
              target can be selected manually except for saving chat""")

    parser.add_argument('-s', '--sender', help='contact or group name')
    parser.add_argument('-r', '--receiver', help='contact or group name')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-wc",
        "--terminal-chat",
        action="store_true",
        help="chatting from command line")

    group.add_argument(
        "-wi",
        "--chat-intermediator",
        action="store_true",
        help='Be an Intermediator from command line -wi -s <sender> -r <receiver> ')

    group.add_argument(
        "-wpd",
        "--profile-download",
        action="store_true",
        help='Download the peofile picture of target')

    group.add_argument(
        "-wms",
        "--message-service",
        action="store_true",
        help="send messages from a JSON file")

    group.add_argument(
        "-wb",
        "--message-blast",
        action="store_true",
        help="message blast to a person")

    group.add_argument(
        "-wti",
        "--message-timer",
        action="store_true",
        help="send messages from time to time")

    group.add_argument(
        "-wt",
        "--online-tracker",
        action="store_true",
        help="track online status of person")

    group.add_argument(
        "-wtb",
        "--telegram-bot",
        action="store_true",
        help="sends tracking status to telegram bot")

    group.add_argument(
        "-wsc",
        "--save-chat",
        action="store_true",
        help="save all chats from Google Drive, target is necessary")

    group.add_argument(
        "-ws",
        "--schedule-message",
        action="store_true",
        help="send the message at scheduled time")

    group.add_argument(
        "-wa",
        "--about-changer",
        action="store_true",
        help="Changes the about section")

    group.add_argument(
        "-wgn",
        "--get-news",
        action="store_true",
        help="Get news in whatsapp group")

    group.add_argument(
        "-wgp",
        "--get-profile-photos",
        action="store_true",
        help="Get profile photo of all your contacts")

    group.add_argument(
        "-wbc",
        "--broadcast",
        action="store_true",
        help="Broadcast message")

    group.add_argument(
        "-wtf",
        "--target-info",
        action="store_true",
        help="finds the information about target's contact")

    group.add_argument(
        "-wd",
        "--download-media",
        action="store_true",
        help="Download the media of the target's contact")

    return parser


# functions for different arguments
async def get_and_match_args(parser):
    args = parser.parse_args()
    if args.online_tracker:
        await online_tracker.tracker(args.target)

    elif args.message_service:
        await message_service.message_service()

    elif args.telegram_bot:
        telegram_bot.telegram_status(args.target)

    elif args.terminal_chat:
        await terminal_chat.chat(args.target)

    elif args.chat_intermediator:
        await chat_intermediator.intermediary(args.sender, args.receiver)

    elif args.profile_download:
        await profile_download.get_profile_picture(args.target)

    elif args.broadcast:
        await broadcast_message.broadcast()

    elif args.message_blast:
        await message_blast.message_blast(args.target)

    elif args.message_timer:
        await message_timer.message_timer(args.target)

    elif args.schedule_message:
        await schedule_message.schedule_message(args.target)

    elif args.about_changer:
        await about_changer.about_changer()

    elif args.get_news:
        await get_news.get_news(args.target)

    elif args.get_profile_photos:
        await get_media.get_profile_photos()

    elif args.target_info:
        await target_info.target_info(args.target)

    elif args.download_media:
        await download_media.download_media(args.target)

    elif args.save_chat:
        await save_chat.save_chat(args.target)


async def main():
    print_logo("wplay")
    create_dirs()
    parser = get_arg_parser()
    try:
        await get_and_match_args(parser)
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)


try:
    asyncio.get_event_loop().run_until_complete(main())
except KeyboardInterrupt:
    pass
except AssertionError:
    try:
        for task in asyncio.all_tasks():
            task.cancel()
    except RuntimeError:
        exit()
    exit()
finally:
    kill_child_processes(os.getpid())
