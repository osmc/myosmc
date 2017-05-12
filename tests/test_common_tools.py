import unittest

import env

from lib.common.logger import Logger
from lib.common.string_manipulation import sanitize_string


def mock_ss(string):
    return string


class LoggerTest(unittest.TestCase):

    def test_whodis(self):
        name = 'disme'
        l = Logger(name)
        self.assertEqual(l.whodisis, name)

    def test_log_goodstring(self):
        name = 'disme'
        l = Logger(name)
        goodstring = 'goodstring'
        try:
            l.log(goodstring)
        except:
            self.fail("logger.log() threw an exception to a good string")

    def test_log_badstring(self):
        name = 'disme'
        l = Logger(name)
        badstring = u'\xa1'
        try:
            l.log(badstring)
        except:
            self.fail("logger.log() threw an exception to a bad string")


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
