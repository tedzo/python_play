#! /usr/bin/env python

# vim: set sw=4 ai et sm:

"""dwalk: walk a directory tree, printing entries hierarchically
   top
   |
   +-- file
   +-- file
   |
   +-- [dir]
   |   |
   |   +-- file
   |   +-- file
   |   |
   |   +-- [dir]
   |   |   |
   |   |   +-- file
   |   |
   |   +-- [dir]
   |   |   |
   |   |   +-- file
   |   |   +-- file
   |
   +-- [dir]
   |   |
   |   +-- [dir]
   |   |   |
   |   |   +--file"""

import os
import sys
import glob
import fnmatch

def dwalk(path, header='', top=True):
    if top:
        print header + path
    else:
        print '{}+-- [{}]'.format(header, os.path.basename(path))
        header = header+'|   '
    files = []
    dirs = []
    for e in os.listdir(path):
        epath = os.path.join(path, e)
        if os.path.isdir(epath):
            dirs.append(e)
        else:
            files.append(e)
    # print '{} dirs: {}'.format(header, dirs)
    # print '{} files: {}'.format(header, files)
    if files:
        print header+'|'
    for f in sorted(files):
        # print header + '| > ' + os.path.join(path, f)
        print header + '+-- ' + f
    for d in sorted(dirs):
        print header+'|'
        dwalk(os.path.join(path,d), header, top=False)

def find(path, match):
    for dirpath, dirs, files in os.walk(path):
        # for f in dirs + files:
        for f in files:
            # print 'Checking {}'.format(os.path.join(dirpath, f))
            if fnmatch.fnmatch(f, match):
                print os.path.join(dirpath, f)

if __name__ == '__main__':
    for topdir in sys.argv[1:]:
        dwalk(topdir)
