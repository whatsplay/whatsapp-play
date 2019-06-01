import argparse
from wplay import onlinetracker
from wplay import messageblast
from wplay import wchat
import sys

# parse positional and optional arguments
def get_arguments():
	parser = argparse.ArgumentParser(description='WhatApp-play')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("-wc", "--wchat", help="chatting from command line")
	group.add_argument("-wb", "--wblast", help="message blast to a person")
	group.add_argument("-wt", "--wtrack", help="track online status of person")

	args = parser.parse_args()
	return args

def match_args(args=None, raw_args=None):
	if args.wtrack:
		onlinetracker.tracker(raw_args)

	elif args.wchat:
		wchat.chat(raw_args)

	elif args.wblast:
		messageblast.blast(raw_args)

def main():
	args = get_arguments()

    # do not pass filename as positional argument
	raw_args = sys.argv[1]
	#args = parser.parse_args(raw_args)

	#if not args.query:
	#	parser.print_help()
	#	exit()

	try:
		match_args(args, raw_args)
		sys.exit(0)
	except KeyboardInterrupt as e:
		sys.exit(0)

	

if __name__=='__main__':
	main()
