import os
import unittest
import env
from mock import Mock, patch

import sys
sys.modules['xbmc'] = Mock()

from common.common_tools import logger, sanitize_string


def mock_ss(string):
	return string


class loggerTest(unittest.TestCase):


	def test_whodis(self):
		name = 'disme'
		l = logger(name)
		self.assertEqual(l.whodisis, name)


	def test_log_goodstring(self):
		name = 'disme'
		l = logger(name)
		goodstring = 'goodstring'		
		try:
			l.log(goodstring)
		except:
			self.fail("logger.log() threw an exception to a good string")


	def test_log_badstring(self):
		name = 'disme'
		l = logger(name)
		badstring = u'\xa1'		
		try:
			l.log(badstring)
		except:
			self.fail("logger.log() threw an exception to a bad string")


class sanitizeTest(unittest.TestCase):


	def test_badstring_return(self):
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



