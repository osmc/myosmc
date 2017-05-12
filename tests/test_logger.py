import unittest

import env

from lib.common.logger import Logger


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
