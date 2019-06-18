#! /usr/bin/env python
"""Test cases for process_data.py program."""

import sys
import unittest
import process_data as pd

class TestWordWarp(unittest.TestCase):
    """A class for testing the word warp processing implementation"""
    PARSER_TEST_CASES = [
        ("Abcdef", True),
        ("abcdef", False),
        ("Abcdef,", False),
        ("Abcdef ", False),
        ("Xyzzyz, Abcdef", True),
        ("Xyzzyz, abcdef", False),
        ("Xyzzyz, Abcdef,", False),
        ("Xyzzyz,  Abcdef", False),
        ("Bagged, Capped, Impact, Waylay, Barley, Danger, Fanged", True),
        ]

    # def test_line_parser(self):
    def test_parser(self):
        """Parser"""
        print "Running tests."
        for line, is_proper in self.PARSER_TEST_CASES:
            if is_proper:
                expected = 'Passed'
            else:
                expected = 'Failed'
            debug_string = '"{}" should have {}'.format(line, expected)
            self.assertEqual(pd.line_parses(line, False), is_proper, debug_string)


def main():
    """Run tests contained in this module."""
    runner = unittest.TextTestRunner()
    loader = unittest.TestLoader()
    test_suite = loader.loadTestsFromTestCase(TestWordWarp)
    result = runner.run(test_suite)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    RUN_UNIT_MAIN = True
    if RUN_UNIT_MAIN:
        unittest.main()
    else:
        sys.exit(main())
