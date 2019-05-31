import argparse
from wplay import onlinetracker
from wplay import messageblast
from wplay import wchat

# parse positional and optional arguments
def parse_args():
	parser = argparse.ArgumentParser(description='WhatApp-play')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("-wc", "--wchat", help="chatting from command line")
	group.add_argument("-wb", "--wblast", help="message blast to a person")
	group.add_argument("-wt", "--wtrack", help="track online status of person")

	args = parser.parse_args()


def main():
	parser=parse_args()

    # do not pass filename as positional argument
	raw_args = sys.argv[1:]
	args = parser.parse_args(raw_args)

	if not args.query:
		parser.print_help()
		exit()

	if args.wt:
		onlinetracker.tracker(raw_args)

	elif args.wc:
		wchat.chat(raw_args)

	elif args.wb:
		messageblast.blast(raw_args)

if __name__=='__main__':
	main()
