import env
import os
import unittest

from sqlite3 import OperationalError

from lib.common.defaults import DEFAULT_DICT


class OsmcprefsTest(unittest.TestCase):

    def test_basic(self):
        try:
            DEFAULT_DICT.update(DEFAULT_DICT.get('somekey', {}))
        except:
            self.fail('DEFAULT_DICT failed to act like a dictionary')
