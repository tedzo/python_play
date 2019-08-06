#! /usr/bin/env python3
"""Test cases for process_data.py program."""

import sys
import unittest
import process_data as pd

class TestWordWarp(unittest.TestCase):
    """A class for testing the word warp processing implementation"""

    # def test_line_parser(self):
    def test_line_space_okay(self):
        """Parser"""
        PARSER_TEST_CASES = [
            ("Abcdef", True),
            ("abcdef", True),
            ("Abcdef,", False),
            ("Abcdef ", False),
            ("Xyzzyz, Abcdef", True),
            ("Xyzzyz, abcdef", True),
            ("Xyzzyz, Abcdef,", False),
            ("Xyzzyz,  Abcdef", False),
            ("Bagged, Capped, Impact, Waylay, Barley, Danger, Fanged", True),
            ]
        for line, is_proper in PARSER_TEST_CASES:
            if is_proper:
                expected = 'Passed'
            else:
                expected = 'Failed'
            debug_string = '"{}" should have {}'.format(line, expected)
            self.assertEqual(pd.line_space_okay(line, False), is_proper, debug_string)

    def test_words_okay(self):
        """Parser"""
        PARSER_TEST_CASES = [
            ("Abcdef", True),
            ("abcdef", False),
            ("Abcdef,", False),
            ("Abcdef ", True),
            ("Xyzzyz, Abcdef", True),
            ("Xyzzyz, abcdef", False),
            ("Xyzzyz, Abcdef,", False),
            ("Xyzzyz,  Abcdef", True),
            ("Bagged, Capped, Impact, Waylay, Barley, Danger, Fanged", True),
            ]
        for line, is_proper in PARSER_TEST_CASES:
            if is_proper:
                expected = 'Passed'
            else:
                expected = 'Failed'
            debug_string = '"{}" should have {}'.format(line, expected)
            self.assertEqual(pd.words_okay(pd.get_words(line), False), is_proper, debug_string)

    def test_get_words(self):
        """Word Parser"""
        TEST_CASES = [
            ("Abcdef", ["Abcdef"]),
            ("bcdefa", ["bcdefa"]),
            ("Abcdef, Bcdefa", ["Abcdef", "Bcdefa"]),
            ("A, Bc", ["A", "Bc"]),
            ("A, B, c", ["A", "B", "c"]),
            ]
        for line, expected in TEST_CASES:
            words = pd.get_words(line)
            debug_template = '"{}" produced {} instead of {}'
            debug_string = debug_template.format(line, words, expected)
            self.assertEqual(expected, words, debug_string)

    def test_anagrams(self):
        """Anagram checker"""
        TEST_CASES = [
            ("Abcdef", True),
            ("abcdef", True),
            ("Abcdef, Bcdefa", True),
            ("Abcdef, Bcdefa", True),
            ("Aaaaaa, aaaaaa", True),
            ("Abaaaa, Baaaaa", True),
            ("Abaaaa, Baaaaa", True),
            ("Abcdef, Bcdefaa", False),
            ("Abcdef, Bcdefar", False),
            ("Abaaaa, Baaaab", False),
            ("Abcdef, Abcdeg", False),
            ("aaaaaa, abbbbb", False),
            ("abcabc, acbaaa", False),
            ("aabbcc, aaddcc", False),
            ("aabbcc, bbccaa, ccaabb", True),
            ("aabbcc, bbccaa, abcabc", True),
            ("aabbcc, bbccaa, ccaadd", False),
            ("aabbcc, bbccaa, ccaabbb", False),
            ]
        for line, is_proper in TEST_CASES:
            if is_proper:
                expected = 'Passed'
            else:
                expected = 'Failed'
            words = [word.casefold() for word in pd.get_words(line)]
            debug_string = '"{}" should have {}'.format(line, expected)
            self.assertEqual(pd.words_are_anagrams(words, False), is_proper, debug_string)

    def test_alphabetic(self):
        """Alphabetic checker"""
        TEST_CASES = [
            ("Abcdef", True),
            ("abcdef", True),
            ("A, B", True),
            ("a, B, c", True),
            ("A, b, C", True),
            ("A, C, b", False),
            ("Abacab, bac", True),
            ("abacab, BAC", True),
            ("aaaca, aaaac", False),
            ("aa, aa, aa", True),
            ("aa, ab, ac", True),
            ("aa, ac, ab", False),
            ]
        for line, is_proper in TEST_CASES:
            if is_proper:
                expected = 'Passed'
            else:
                expected = 'Failed'
            words = [word.casefold() for word in pd.get_words(line)]
            debug_string = '"{}" should have {}'.format(line, expected)
            self.assertEqual(pd.words_are_alphabetic(words, False), is_proper, debug_string)

    def test_line_is_good(self):
        """line_is_good checker"""
        GOOD_LINES = [
            "Action",
            "Addles, Saddle",
            "Allure, Laurel",
            "Chines, Inches, Niches",
            "Deigns, Design, Signed, Singed",
            "Esteem",
            "Evilly, Lively, Vilely",
            "Macaws",
            "Paltry, Partly",
            "Statin, Taints, Titans",
            "Whiter, Wither, Writhe",
            "Wintry",
            ]
        BAD_LINES = [
            "WinTry",
            "wintry",
            "Wintr",
            "Wintryd",
            "Wintry, withal",
            "Wintry, WithaL",
            "Wintr, Withal",
            "Wintry, Witha",
            "Wintryz, Withal",
            "Wintry, Withala",
            "Wintry,Withal",
            "Wintry, Withal",
            ]
        for line in GOOD_LINES:
            debug_string = '"{}" should have passed.'.format(line)
            good, reason = pd.line_is_good(line, False)
            self.assertTrue(good, debug_string)
        for line in BAD_LINES:
            debug_string = '"{}" should have failed.'.format(line)
            good, reason = pd.line_is_good(line, False)
            self.assertFalse(good, debug_string)

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
