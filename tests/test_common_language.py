import env
import os
import unittest

from lib.common.language import Translator


class mock_addon(object):

    def __init__(self):
        pass

    def getLocalizedString(self, id):

        return 'good string'


class LanguageTest(unittest.TestCase):

    def test_basic(self):
        try:
            m = mock_addon()
            a = Translator(m)
            a.lang(1)

        except:
            self.fail('language function failed basic test.')
