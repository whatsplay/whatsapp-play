import argparse
import asyncio
import sys
from pyfiglet import Figlet
from wplay import onlinetracker
from wplay import messageblast
from wplay import messagetimer
from wplay import wchat
from wplay import savechat
from wplay import tgbot


#TODO: Change 'name' to 'target'


def print_logo(text_logo):
    figlet = Figlet(font='slant')
    print(figlet.renderText(text_logo))


# parse positional and optional arguments
def get_arguments():
    parser = argparse.ArgumentParser(description = 'WhatsApp-play')
    parser.add_argument(
        "name",
        metavar="NAME",
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
        await onlinetracker.tracker(args.name)

    elif args.wtgbot:
        tgbot.telegram_status(args.name)

    elif args.wchat:
        await wchat.chat(args.name)

    elif args.wblast:
        await messageblast.blast(args.name)

    elif args.wtimer:
        await messagetimer.msgTimer(args.name)

    elif args.pull:
        try:
            bID = int(sys.argv[3])
        except (IndexError, ValueError):
            bID = 0
        savechat.runMain('pull', str(args.name), bID)

    # elif args.wlocation:
    #     loactionfinder.finder(args.name)


async def main():
    print_logo("wplay")
    args = get_arguments()
    try:
        await match_args(args)
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)

asyncio.get_event_loop().run_until_complete(main())
