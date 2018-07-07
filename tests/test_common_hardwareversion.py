import env
import os
import unittest

from lib.common.hardware import get_proc_info

class HardwareVersionTest(unittest.TestCase):

    def test_basic(self):
        try:
            get_proc_info()
        except:
            self.fail('hardware_version function failed basic test.')
