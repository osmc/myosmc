import unittest

import env

from lib.common.string_manipulation import sanitize_string


def mock_ss(string):
    return string


class SanitizeTest(unittest.TestCase):

    def test_goodstring_return(self):
        goodstring = 'goodstring'
        try:
            sanitize_string(goodstring)
        except:
            self.fail("sanitize_string() threw an exception to a good string")

    def test_badstring_return(self):
        badstring = u'\xa1'
        try:
            sanitize_string(badstring)
        except:
            self.fail("sanitize_string() threw an exception to a bad string")
