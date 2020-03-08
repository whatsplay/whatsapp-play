# The first four lines import python library scripts.
import argparse
import asyncio
import sys
import os
from pyfiglet import Figlet
# These import wplay scripts which are in the same folder of main.
from wplay.utils import kill_process
from wplay import onlinetracker
from wplay import messageblast
from wplay import messagetimer
from wplay import wchat
from wplay import savechat
from wplay import tgbot
# The logo of wplay gets printed by this function
def print_logo(text_logo):
    figlet = Figlet(font='slant')
    print(figlet.renderText(text_logo))

# parse positional and optional arguments which are used to do various things like tracking and bombing messages etc.
def get_arguments():
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
    group = https://github.com/rpotter12/whatsapp-play/pull/199/conflict?name=wplay%252Fonlinetracker.py&ancestor_oid=098a895dcee0146565d3614cc50e82da44c4d532&base_oid=2c03f17cffb9deaf4b14def1b267e9d62ff1953f&head_oid=120a111cc8fb7771469b8e64b9f62d962c0146ffparser.add_mutually_exclusive_group(required = True)
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
            bID = int(sys.argv[3])
        except (IndexError, ValueError):
            bID = 0
        savechat.runMain('pull', str(args.target), bID)
# elif args.wlocation:
#     loactionfinder.finder(args.target)
# This fun prints logo and waits for matching arguments if not found exits.
async def main():
    print_logo("wplay")
    parser = get_arg_parser()
    try:
        await get_and_match_args(parser)
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)
try:
    asyncio.get_event_loop().run_until_complete(main())
except AssertionError:
    try:
        for task in asyncio.all_tasks():
            task.cancel()
    except RuntimeError:
        exit()
    exit()
finally:
    kill_process.kill_child_processes(os.getpid())
