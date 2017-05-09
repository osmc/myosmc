import os
import unittest
import env

from database.dbinterface import DBInterface, database_connection
from test_data.test_entries import test_items, test_items_replacements


class DBInterfaceTest(unittest.TestCase):

	def setUp(self):
		self.testdb = 'test.db'
		try:
			os.remove(self.testdb)
		except IOError:
			pass
		except WindowsError:
			pass

	def tearDown(self):
		try:
			os.remove(self.testdb)
		except:
			pass

	def test_setting(self):
		db = DBInterface(self.testdb)
		for k, v in test_items.iteritems():
			self.assertEqual(db.setSetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))
		os.remove(self.testdb)

	def test_getting(self):
		db = DBInterface(self.testdb)

		for k, v in test_items.iteritems():
			self.assertEqual(db.setSetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

		for k, v in test_items.iteritems():
			self.assertEqual(db.getSetting(k), v, msg='Failed to get (%s)' % (k))
		os.remove(self.testdb)

	def test_allPairs_returntype(self):
		db = DBInterface(self.testdb)

		for k, v in test_items.iteritems():
			self.assertEqual(db.setSetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

		self.assertIsInstance(db.allPairs(), dict, msg='Output of allPairs is not a dict')
		os.remove(self.testdb)

	def test_allPairs(self):
		db = DBInterface(self.testdb)

		for k, v in test_items.iteritems():
			self.assertEqual(db.setSetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

		ap = db.allPairs()
		for k, v in test_items.iteritems():
			self.assertIn(k, ap, msg='Key (%s) not found in allPairs' % k)
			self.assertEqual(ap[k], v, msg='Value in allPairs not equal to original item')
		os.remove(self.testdb)			

	def test_unknownkey(self):
		db = DBInterface(self.testdb)
		with self.assertRaises(KeyError):
			db.getSetting('unknownkey')
		os.remove(self.testdb)					

	def test_unhandled_datatype(self):
		db = DBInterface(self.testdb)
		with self.assertRaises(TypeError):
			for k, v in test_items.iteritems():
				db.setSetting(k, v, datatype=bytes)
		os.remove(self.testdb)						

	def test_keynotstring(self):
		db = DBInterface(self.testdb)
		with self.assertRaises(TypeError):
			db.setSetting(1)
		os.remove(self.testdb)	

	def test_replacement_setting(self):
		db = DBInterface(self.testdb)		

		for k, v in test_items.iteritems():
			self.assertEqual(db.setSetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))
			
		for k, v in test_items_replacements.iteritems():
			self.assertEqual(db.setSetting(k, v), [], msg='Failed to set replacement (%s, %s)' % (k, v))
		os.remove(self.testdb)	

	def test_replacement_getting(self):
		db = DBInterface(self.testdb)	

		for k, v in test_items_replacements.iteritems():
			self.assertEqual(db.setSetting(k, v), [], msg='Failed to set replacement (%s, %s)' % (k, v))
		
		for k, v in test_items_replacements.iteritems():
			self.assertEqual(db.getSetting(k), v, msg='Failed to get replacement (%s)' % (k))	
		os.remove(self.testdb)	

	def test_default_processing(self):
		self.assertIsInstance(DBInterface(self.testdb, defaults=test_items), DBInterface, msg='Processing default changes class type')
		os.remove(self.testdb)

	def test_default_results(self):
		db = DBInterface(self.testdb, defaults=test_items)
		self.assertEqual(len(db.errors), 0, msg='Importing of defaults throws error(s):\n%s' % ('\n'.join(db.errors)))
		os.remove(self.testdb)

	def test_default_values(self):
		db = DBInterface(self.testdb, defaults=test_items)

		for k, v in test_items.iteritems():
			self.assertEqual(db.getSetting(k), v, msg='Value added as default, different to original (%s)' % k)
		os.remove(self.testdb)
