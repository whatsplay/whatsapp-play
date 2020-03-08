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
    parser = argparse.ArgumentParser(description = 'WhatsApp-play')
    parser.add_argument(
        "target",
        metavar="TARGET",
        type=str,
        help="contact or group name")

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
        help = "save all chats")

    # group.add_argument(
    #     "-wl",
    #     "--wlocation",
    #     action = "store_true",
    #     help = "finds the location of the person")

    args = parser.parse_args()
    return args


# functions for different arguments
async def match_args(args):
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
    args = get_arguments()
    try:
        await match_args(args)
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
