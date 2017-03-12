import argparse, os, sys


from get_pwd import get_password

def parse_args():
	parser = argparse.ArgumentParser(description = 'PayDocument Hack -s <start date> -e <end date> <target html path>')
	parser.add_argument('-s', '--startDate', help="like formmat with 2014-01-02, 20140102... ", default='19000101')
	parser.add_argument('-e', '--endDate', help="like formmat with 2014-01-02, 20140102... ", default='21000101')
	parser.add_argument('file')
	return parser.parse_args()


if __name__ == '__main__':
	args = parse_args()
	print(get_password(**vars(args)))