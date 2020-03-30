import argparse
import asyncio
import sys
import os

from pyfiglet import Figlet

from wplay.utils import kill_process
from wplay import onlinetracker
from wplay import messageblast
from wplay import messagetimer
from wplay import wchat
from wplay import savechat
from wplay import tgbot
from wplay import scheduleMessage
from wplay import changeAbout
from wplay import wnews
from wplay import get_media
from wplay.utils import Logger
from wplay.utils.helpers import logs_path


#region LOGGER create
logger = Logger.setup_logger('logs',logs_path/'logs.log')
#endregion



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
        "--wchat",
        action = "store_true",
        help = "chatting from command line")

    group.add_argument(
        "-wb",
        "--wblast",
        action = "store_true",
        help = "message blast to a person")

    group.add_argument(
        "-wti",
        "--wtimer",
        action = "store_true",
        help = "send messages from time to time")

    group.add_argument(
        "-wt",
        "--wtrack",
        action = "store_true",
        help = "track online status of person")
    group.add_argument(
        "-wtb",
        "--wtgbot",
        action = "store_true",
        help = "sends tracking status to telegram bot")

    group.add_argument(
        "-pull",
        "--pull",
        action = "store_true",
        help = "save all chats, target is necessary")

    group.add_argument(
        "-sch",
        "--schedule",
        action = "store_true",
        help = "send the message at scheduled time")

    group.add_argument(
        "-wabt",
        "--wabout",
        action = "store_true",
        help = "Changes the about section"
    )

    group.add_argument(
        "-wnews",
        "--wnews",
        action = "store_true",
        help = "Get news in whatsapp group"
    )

    group.add_argument(
        "-wmedia",
        "--wgetmedia",
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
    if args.wtrack:
        await onlinetracker.tracker(args.target)

    elif args.wtgbot:
        tgbot.telegram_status(args.target)

    elif args.wchat:
        await wchat.chat(args.target)

    elif args.wblast:
        await messageblast.blast(args.target)

    elif args.wtimer:
        await messagetimer.msgTimer(args.target)

    elif args.pull:
        if args.target is None:
            parser.print_help()
            parser.exit()
        try:
            bID : int = int(sys.argv[3])
        except (IndexError, ValueError):
            bID : int = 0
        savechat.runMain('pull', str(args.target), bID)

    elif args.schedule:
        await scheduleMessage.schedule_message(args.target)

    elif args.wabout:
        await changeAbout.changeAbout()

    elif args.wnews:
        await wnews.get_news(args.target)

    elif args.wgetmedia:
        await get_media.get_all_media()

    # elif args.wlocation:
    #     loactionfinder.finder(args.target)


async def main():
    print_logo("wplay")
    parser = get_arg_parser()
    try:
        await get_and_match_args(parser)
        sys.exit(0)
    except KeyboardInterrupt:
        logger.error('User Pressed Ctrl+C')
        sys.exit(0)

try:
    asyncio.get_event_loop().run_until_complete(main())
except KeyboardInterrupt:
        logger.error('User Pressed Ctrl+C')
except AssertionError:
    try:
        for task in asyncio.all_tasks():
            task.cancel()
    except RuntimeError:
        exit()
    exit()
finally:
    kill_process.kill_child_processes(os.getpid())
