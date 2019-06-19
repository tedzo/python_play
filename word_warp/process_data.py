#! /usr/bin/env python
"""Program to process a word warp data file.

This is primarly used as a stand-alone program which validates and helps
debug a word warp (6-letter words) data file.  However, if the module is
imported, it's functions are useable to perform the same tasks, or
individual validation steps as desired.

Functions:
    line_parses(): Checks syntactic validity of a given line.
    words_are_anagrams(): Checks that the words in a line are
        anagrams of each other.
    words_are_alphabetic(): Checks that the words in a line are
        in alphabetic order.
    line_is_good(): Checks that a line passes all the above checks.

When invoked as a command-line program, there are 2 modes of operation:
    Default, or when a list of files to process is specific:
        Each line in the files is checked, as well as a check to make sure
            the lines themselves are in alphabetical order.
    When run interactively: the user is prompted for input and each line
        is individually checked for validity via line_is_good().
"""

import sys
import re
import readline  # Enables history/editing in raw_input() function.
import argparse
import fileinput
import glob

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

def get_words(line):
    """Given a line that parses, return a list of words in that line."""
    return [word.lower() for word in line.split(', ')]

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
        return (False, 0, 'Did not parse.')
    word_list = get_words(line)
    if debug: print word_list
    if not words_are_anagrams(word_list, debug):
        return (False, 0, 'Not anagrams')
    if not words_are_alphabetic(word_list, debug):
        return (False, 0, 'Not alphabetic')

    return (True, 'All is well')

def parse_args(args):
    """Parse command line arguments to the program."""
    parser = argparse.ArgumentParser(description='Process word warp data file')
    parser.add_argument('--test', '-t', action='store_true',
                        help='Run unit tests')
    parser.add_argument('--quit', action='store_true',
                        help='Quit after processing arguments')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Run interactively (line by line input)')
    parser.add_argument('--files', '-f', nargs='+', default=sorted(glob.glob('ww_data*')))
    parser.add_argument('--stats', '-s', action='store_true',
                        help='Show statistics for each file processed.')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose: show each file processed.')
    parser.add_argument('--debug_program', '-D', action='store_true',
                        help='Program debug mode: dump argument namespace, regex matches.')
    parser.add_argument('--debug_data', '-d', action='store_true',
                        help='Data debug mode: give hints about bad data.')
    parser.add_argument('--count', '-c', type=int, default=-1,
                        help='Maximum number of lines per file to process.')

    return parser.parse_args(args)

def get_user_lines(prompt):
    """Generator which returns user input to a given prompt.

    A blank line of input terminates the generator.
    """
    while True:
        line = raw_input(prompt).rstrip('\n')
        if line == '':
            break
        yield line

class Stats(object):
    MAX_ALLOWED_WORDS = 10

    def __init__(self):
        self.good_lines = 0
        self.good_words = 0
        self.histogram = [0] * Stats.MAX_ALLOWED_WORDS
        self.most_words = 0

    def add_line(self, line):
        self.good_lines += 1
        word_list = get_words(line)
        num_words = len(word_list)
        assert(num_words < Stats.MAX_ALLOWED_WORDS)
        if num_words > self.most_words:
            self.most_words = num_words
        self.good_words += num_words
        self.histogram[num_words] += 1

    # def show(self, indent):
    def show(self):
        print "  Unique 6-letter combinations: {}".format(self.good_lines)
        print "  Unique words: {}".format(self.good_words)
        for i in range(1, self.most_words+1):
            print "  Number of {}-word anagrams: {}".format(i, self.histogram[i])


def process_files(args):
    """Process lines in the files given on the command line."""

    succeeded = True
    at_beginning = True

    for line in fileinput.input(args.files):
        line = line.rstrip('\n')

        # At the beginning of each file, reset per file state, and print
        #    statistics for the previous file.
        if fileinput.isfirstline():
            if args.stats and not at_beginning:
                my_stats.show()
            last_good_line = ''
            my_stats = Stats()
            count = 0
            if args.verbose or args.stats:
                print 'Processing "{}"'.format(fileinput.filename())
        at_beginning = False
        if count == args.count:
            fileinput.nextfile()
            continue
        else:
            count += 1

        # Skip blank lines, comment lines and lines that say "Word warp".
        SKIP_RE = r'^$|^#.*$|^[Ww]ord[  ]*[Ww]arp$'
        if re.search(SKIP_RE, line):
            if args.verbose: print 'Skipping "{}".'.format(line)
            continue

        # Quit processing a file after a line starting with 3 dashes or m-dashes.
        # (Utf-8 encoding for an m-dash is \xe2\x80\x94)
        END_RE = '^(-{3})|(\xe2\x80\x94){3}.*$'
        if re.search(END_RE, line):
            if args.verbose:
                print 'Finishing at {}:"{}".'.format(fileinput.filelineno(), line)
            fileinput.nextfile()
            continue

        line_good, reason = line_is_good(line, args.debug_program)
        if not line_good:
            succeeded = False
            print 'Bad {}.{}({}): "{}"'.format(fileinput.filename(),
                    fileinput.filelineno(), reason, line)
        elif not line > last_good_line:
            succeeded = False
            print 'Bad {}.{}: "{}" after "{}"'.format(fileinput.filename(),
                    fileinput.filelineno(), line, last_good_line)
        else:
            last_good_line = line
            my_stats.add_line(line)

    # Print the stats for the last file.
    if args.stats and not at_beginning:
        my_stats.show()

    if succeeded:
        return 0
    return 1

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    if args.debug_program or args.quit:
        print args
    if args.quit:
        sys.exit(0)

    if args.test:
        from test_word_warp import main as test_main
        sys.exit(test_main())

    if args.interactive:
        for line in get_user_lines('Please type a line -> '):
            line_good, reason = line_is_good(line, args.debug_program)
            if line_good:
                print 'Good: "{}"'.format(line)
            else:
                print 'Bad ({}): "{}"'.format(reason, line)
    else:
        sys.exit(process_files(args))
