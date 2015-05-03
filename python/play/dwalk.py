#! /usr/bin/env python

"""dwalk: walk a directory tree, printing entries hierarchically
   + top
   | > file
   | > file
   | + dir
   | | > file
   | | > file
   | | + dir
   | | | > file
   | | + dir
   | | | > file
   | | | > file
   | + dir
   | | + dir
   | | | > file"""

import os
import sys

def dwalk(path, header=''):
    print header + '+ ' + path
    files = []
    dirs = []
    for e in os.listdir(path):
	epath = os.path.join(path, e)
        if os.path.isdir(epath):
	    # print header + '{} is a dir'.format(e)
	    dirs.append(e)
        else:
	    # print header + '{} is a file'.format(e)
	    files.append(e)
    # print '{} dirs: {}'.format(header, dirs)
    # print '{} files: {}'.format(header, files)
    for f in sorted(files):
	# print header + '| > ' + os.path.join(path, f)
        print header + '| > ' + f
    for d in sorted(dirs):
        dwalk(os.path.join(path,d), header+'| ')

