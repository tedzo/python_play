#! /usr/bin/env python

# vim: set ai sw=4:

import sys
import os
import math
import argparse

def l10(num):
    return int(math.log10(num))

def ps(num):
    for d in xrange(l10(num), -1, -1):
        print "".join([chr(ord('0')+((x/(10**d))%10)) for x in xrange(1,num+1)])

def ps_base(num, base):
    for d in xrange(int(math.log(num,base)), -1, -1):
	def dig(num, base):
	    if base <= 10 or num < 10:
		return chr(ord('0')+num)
	    else:
		return chr(ord('a')+num-10)
        print "".join([dig((x/(base**d))%base, base) for x in xrange(1,num+1)])

def do_main(argv=None):
    if argv == None:
	argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Print numbers sideways.")
    # parser.add_argument('numbers', metavar='N', type=int, nargs='+')
    parser.add_argument('numbers', metavar='N', nargs='+')
    parser.add_argument('-b', '--base', type=int, action='store', default=0)
    args = parser.parse_args(argv)
    # print args
    if args.base == 0:
	for val in args.numbers:
	    ps(int(val))
    else:
	for val in args.numbers:
	    ps_base(int(val, args.base), args.base)

    return 0
    
if __name__ == '__main__':
    sys.exit(do_main())
    if len(sys.argv) < 2:
	print "Please specify number(s) to print sideways."
	sys.exit(1)
    for num in sys.argv[1:]:
	ps(int(num, 0))
