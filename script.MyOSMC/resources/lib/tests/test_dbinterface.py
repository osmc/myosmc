import os
import unittest
import env
from sqlite3 import OperationalError

from database.dbinterface import DBInterface, database_connection, CLI
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

	
	def test_bool_type_mismatch(self):
		db = DBInterface(self.testdb)
		with self.assertRaises(TypeError):
			db.setSetting('a', 1, datatype=bool)
		os.remove(self.testdb)	

	
	def test_int_type_mismatch(self):
		db = DBInterface(self.testdb)
		with self.assertRaises(TypeError):
			db.setSetting('a', 'test', datatype=int)
		os.remove(self.testdb)	

	
	def test_float_type_mismatch(self):
		db = DBInterface(self.testdb)
		with self.assertRaises(TypeError):
			db.setSetting('a', 'test', datatype=float)
		os.remove(self.testdb)	

	
	def test_keynotstring_set(self):
		db = DBInterface(self.testdb)
		with self.assertRaises(TypeError):
			db.setSetting(1, 'a')
		os.remove(self.testdb)		

	
	def test_keynotstring_get(self):
		db = DBInterface(self.testdb)
		with self.assertRaises(TypeError):
			db.getSetting(1)
		os.remove(self.testdb)				


	def test_wrongschema_startup(self):
		db = DBInterface(self.testdb)
		db._database_execution('DROP TABLE OSMCSETTINGS', [])
		q = 'CREATE TABLE IF NOT EXISTS OSMCSETTINGS (key VARCHAR(255) PRIMARY KEY, value_bool TEXT, value_int TEXT, value_float BOOLEAN, value_str BOOLEAN)'
		db._database_execution(q, [])
		self.assertEqual(db._check_schema(), False)
		os.remove(self.testdb)		


	
	def test_wrongscheme(self):
		db = DBInterface(self.testdb)
		db._database_execution('DROP TABLE OSMCSETTINGS', [])
		q = 'CREATE TABLE IF NOT EXISTS OSMCSETTINGS (key VARCHAR(255) PRIMARY KEY, value_bool TEXT, value_int TEXT, value_float BOOLEAN, value_str BOOLEAN)'
		db._database_execution(q, [])
		self.assertEqual(db._check_schema(), False)
		os.remove(self.testdb)		

	
	def test_sqlerror(self):
		db = DBInterface(self.testdb)
		with self.assertRaises(OperationalError):
			db._database_execution('SELECT "', [])

	
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

	
	def test_CLI(self):
		
		for value in ['True', '1234','1.01','None']:

			self.assertEqual(CLI(['dbinterface.py']), 'add help')
			self.assertEqual(CLI(['dbinterface.py', '-d', self.testdb, 'a', str(value)]), 'Set "a" as "%s"' % value)
			self.assertEqual(CLI(['dbinterface.py', '-d', self.testdb, 'a']), str(value))
			self.assertEqual(len(CLI(['dbinterface.py', '-d', self.testdb, '-a'])), 168)

			self.assertEqual(CLI(['dbinterface.py', '-z', self.testdb, 'a', str(value)]), 'add help')
			self.assertEqual(CLI(['dbinterface.py', '-z', self.testdb, 'a']), 'add help')
			self.assertEqual(CLI(['dbinterface.py', '-z', self.testdb, '-a']), 'add help')
			os.remove(self.testdb)

			self.assertEqual(CLI(['dbinterface.py'], provided_db=self.testdb), 'add help')
			self.assertEqual(CLI(['dbinterface.py', 'a', str(value)], provided_db=self.testdb), 'Set "a" as "%s"' % value)

			self.assertEqual(CLI(['dbinterface.py', 'a'], provided_db=self.testdb), str(value))
			self.assertEqual(len(CLI(['dbinterface.py', '-a'], provided_db=self.testdb)), 168)
			os.remove(self.testdb)

	
	def test_bad_default_dict(self):
		with self.assertRaises(AttributeError):
			DBInterface(self.testdb, defaults=[])

	
	def test_bad_default_key(self):
		db = DBInterface(self.testdb, defaults={1:'a'})
		self.assertEqual(len(db.errors), 1)
		os.remove(self.testdb)
