import argparse
from wplay import onlinetracker
from wplay import messageblast
from wplay import wchat
import sys

# parse positional and optional arguments
def get_arguments():
	parser = argparse.ArgumentParser(description='WhatApp-play')
	parser.add_argument("name", metavar="NAME", type=str, help="contact name of the target")

	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("-wc", "--wchat", action="store_true", help="chatting from command line")
	group.add_argument("-wb", "--wblast", action="store_true", help="message blast to a person")
	group.add_argument("-wt", "--wtrack", action="store_true", help="track online status of person")

	args = parser.parse_args()
	return args

def match_args(args):
	if args.wtrack:
		onlinetracker.tracker(args.name)

	elif args.wchat:
		wchat.chat(args.name)

	elif args.wblast:
		messageblast.blast(args.name)

def main():
	args = get_arguments()
	try:
		match_args(args)
		sys.exit(0)
	except KeyboardInterrupt as e:
		sys.exit(0)


if __name__=='__main__':
	main()
