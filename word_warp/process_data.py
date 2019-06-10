#! /usr/bin/env python

import sys
import os
import re
import readline
import argparse
import fileinput

# Regular expressions for general use.
WORD_RE = r'[A-Z][a-z]{5}'
LINE_RE = '^({0})(, {0})*$'.format(WORD_RE)

def line_parses(line, debug):
    """Verify if a line matches the parsing criteria for a word warp line.

    The criteria are:
    Basic syntax:
    - A line is composed of 6-letter words.
    - Each word is capitalized.  Only the first letter should be a capital.
    - If there is only 1 word, the line is just the 6 letters.
    - If there are more than 1 word, words are separated by a comma and a
      space.
    """
    match = re.search(LINE_RE, line)
    if match:
        if debug: print match.groups()
        return True
    else:
        return False

def words_are_anagrams(word_list, debug):
    """Return words in list are sorted anagrams of each other."""
    # Check if all the words are the same length
    length = len(word_list[0])
    for cur_len in (len(word) for word in word_list):
        if cur_len != length:
            return False

    # Check if all the words contain the same letters
    letters = sorted(word_list[0])
    for word in word_list:
        if letters != sorted(word):
            return False

    # All the words are the same lenght and have the same letters.
    return True

def words_are_alphabetic(word_list, debug):
    """Return whether words in line are sorted alphabetically."""
    return sorted(word_list) == word_list

def line_is_good(line, debug):
    """Verify if a line matches the criteria for a proper word warp line.

    The criteria are:
    Basic syntax (line parses):
    - A line is composed of 6-letter words.
    - Each word is capitalized.  Only the first letter should be a capital.
    - If there is only 1 word, the line is just the 6 letters.
    - If there are more than 1 words, words are separated by a comma and a
      space.
    Further:
    - All the words in a line should be anagrams of each other.
    - All the words in a line should be sorted alphabetically.
    - All the lines in the file should be sorted alphabetically.
    """
    if not line_parses(line, debug):
        return (False, 'Did not parse.')
    word_list = [word.lower() for word in line.split(', ')]
    if debug: print word_list
    if not words_are_anagrams(word_list, debug):
        return (False, 'Not anagrams')
    if not words_are_alphabetic(word_list, debug):
        return (False, 'Not alphabetic')

    return (True, 'All is well')

def parse_args(args):
    parser = argparse.ArgumentParser(description='Process word warp data file')
    parser.add_argument('--interactive', '-i', action='store_true',
            help='Run interactively (line by line input)')
    parser.add_argument('--files', '-f', nargs='+', default=['raw_input'])
    parser.add_argument('--debug_program', '-D', action='store_true',
            help='Program debug mode: dump argument namespace, regex matches.')
    parser.add_argument('--debug_data', '-d', action='store_true',
            help='Data debug mode: give hints about bad data.')
    parser.add_argument('--count', '-c', type=int, default=0,
            help='Maximum number of lines to process.')
    # parser.add_argument()
    # parser.add_argument()

    return parser.parse_args(args)

def get_user_lines(prompt):
    """Generator which returns user input to a given prompt.

    A blank line of input terminates the generator.
    """
    while True:
        line = raw_input('Please type a line -> ').rstrip('\n')
        if line == '':
            break
        yield line

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    if args.debug_program:
        print args

    # if args.interactive:
    #     line_producer = get_user_lines('Please type a line -> '):
    # else:
    #     line_producer = fileinput.input(args.files):

    if args.interactive:
        for line in get_user_lines('Please type a line -> '):
            line_good, reason = line_is_good(line, args.debug_program)
            if line_good:
                print 'Good: "{}"'.format(line)
            else:
                print 'Bad ({}): "{}"'.format(reason, line)
    else:
        # with open(args.file) as file:
        limit = False
        if args.count != 0:
            limit = True
            count = args.count
        last_good_line = ''
        for line in fileinput.input(args.files):
            if limit:
                if count == 0:
                    break
                else:
                    count -= 1
            line = line.rstrip('\n')
            line_good, reason = line_is_good(line, args.debug_program)
            if not line_good:
                print 'Bad {}.{}({}): "{}"'.format(fileinput.filename(),
                        fileinput.lineno(), reason, line)
            elif not line > last_good_line:
                print 'Bad {}.{}: "{}" after "{}"'.format(fileinput.filename(),
                        fileinput.lineno(), line, last_good_line)
            else:
                last_good_line = line
