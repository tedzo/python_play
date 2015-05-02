#! /usr/bin/env python

import sys
import os, os.path
import argparse

class function_list(object):
    def __init__(self):
        self.list={}

    def add(self, name, command):
        self.list[name] = command

    def get(self, name):
        if name in self.list:
            return self.list[name]
        else:
            return None

    def run(self, name, *args):
        if name in self.list:
            return self.list[name](*args)
        else:
            return None

    def show(self):
        for k in self.list:
            print "%s: %s" % (k, repr(self.list[k]))

#
# echo
#
def echo (name, args):
    # Mac echo only supports -n, Linux has more options, and some
    # \ sequences it parses.
    # Go ahead and set up an arg parser, but start simple.

    description = "Echo back input arguments."
    parser = argparse.ArgumentParser(description=description,
                                     prog=name)
    parser.add_argument('-n',
                        help="don't add newline at end of output.",
                        action="store_true")
    # print repr(parser.parse_known_args(args))
    flags,params = parser.parse_known_args(args)
    output = " ".join(params)

    # Use stdout.write() instead of print, because (why?) when using print
    # (even with the trailing ","), a newline is added at the end of all
    # output.
    # TODO: Find out why.  Maybe it's Mac-specific.
    if flags.n:
        sys.stdout.write( "%s" % output)
    else:
        sys.stdout.write( "%s\n" % output)

    return 0

#
# mv
#
def move(name, args):
    description = "Move files."
    parser = argparse.ArgumentParser(description=description,
                                     prog=name)
    parser.add_argument('-f',
                        help="Don't prompt for confirmation.",
                        action="store_true")
    parser.add_argument('-i',
                        help="Prompt for confirmation before overwriting.",
                        action="store_true")
    parser.add_argument('-n',
                        help="Don't overwrite existing file.",
                        action="store_true")
    parser.add_argument('-v',
                        help="Be verbose; show files after moving.",
                        action="store_true")

    flags, params = parser.parse_known_args(args)

    print "Flags: %s" % repr(flags)
    print "Params: %s" % repr(params)


#
# Build up command list.
#
command_list = function_list()
command_list.add("echo", echo)
command_list.add("mv", move)


def runit(args):
    # Assume that we are getting argv, so we can assume at least 1 arg.
    name = os.path.basename(args[0])
    args = args[1:]

    command = command_list.get(name)
    if not command:
        print >> sys.stderr, "pybox: unknown command: %s" % name
        return 1
    return command(name, args)

if __name__ == "__main__":
    # print "Woo hoo; I'm being executed as %s." % os.path.basename(sys.argv[0])
    rv = runit(sys.argv)
    exit(rv)
