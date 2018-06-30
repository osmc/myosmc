import env
import os
import unittest

from lib.common.hardwareversion import hardware_version

class HardwareVersionTest(unittest.TestCase):

    def test_basic(self):
        try:
            hardware_version()
        except:
            self.fail('hardware_version function failed basic test.')
