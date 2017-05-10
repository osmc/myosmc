import os
import unittest
import env
from sqlite3 import OperationalError

from database.dbinterface import DBInterface, database_connection, CLI, get_setting
from test_data.test_entries import test_items, test_items_replacements


class fresh_database(object):   # pragma: no cover

	def __init__(self, dbpath, defaults=None):

		self.dbpath = dbpath
		self.defaults = defaults

	def __enter__(self, *args, **kwargs):

		self.db = DBInterface(self.dbpath, defaults=self.defaults)

		return self.db
	
	def __exit__(self, *args, **kwargs):

		os.remove(self.dbpath)


class DBInterfaceTest(unittest.TestCase):

	
	def setUp(self):
		
		self.dbpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_data','test.db')
		try:
			os.remove(self.dbpath)
		except IOError:   # pragma: no cover
			pass
		except OSError:   # pragma: no cover
			pass
		except WindowsError:   # pragma: no cover
			pass

	
	def tearDown(self):
		try:
			os.remove(self.dbpath)
		except:
			pass

	
	def test_setting(self):
		with fresh_database(self.dbpath) as db:
			for k, v in test_items.iteritems():
				self.assertEqual(db.setSetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

	
	def test_getting(self):
		with fresh_database(self.dbpath) as db:
			for k, v in test_items.iteritems():
				self.assertEqual(db.setSetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

			for k, v in test_items.iteritems():
				self.assertEqual(db.getSetting(k), v, msg='Failed to get (%s)' % (k))

	
	def test_allPairs_returntype(self):
		with fresh_database(self.dbpath) as db:
			for k, v in test_items.iteritems():
				self.assertEqual(db.setSetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

			self.assertIsInstance(db.allPairs(), dict, msg='Output of allPairs is not a dict')

	
	def test_allPairs(self):
		with fresh_database(self.dbpath) as db:
			for k, v in test_items.iteritems():
				self.assertEqual(db.setSetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

			ap = db.allPairs()
			for k, v in test_items.iteritems():
				self.assertIn(k, ap, msg='Key (%s) not found in allPairs' % k)
				self.assertEqual(ap[k], v, msg='Value in allPairs not equal to original item')

	
	def test_unknownkey(self):
		with fresh_database(self.dbpath) as db:
			with self.assertRaises(KeyError):
				db.getSetting('unknownkey')

	
	def test_bool_type_mismatch(self):
		with fresh_database(self.dbpath) as db:
			with self.assertRaises(TypeError):
				db.setSetting('a', 1, datatype=bool)

	
	def test_int_type_mismatch(self):
		with fresh_database(self.dbpath) as db:
			with self.assertRaises(TypeError):
				db.setSetting('a', 'test', datatype=int)

	
	def test_float_type_mismatch(self):
		with fresh_database(self.dbpath) as db:
			with self.assertRaises(TypeError):
				db.setSetting('a', 'test', datatype=float)

	
	def test_keynotstring_set(self):
		with fresh_database(self.dbpath) as db:
			with self.assertRaises(TypeError):
				db.setSetting(1, 'a')

	
	def test_keynotstring_get(self):
		with fresh_database(self.dbpath) as db:
			with self.assertRaises(TypeError):
				db.getSetting(1)


	def test_wrongschema_startup(self):
		with fresh_database(self.dbpath) as db:
			db._database_execution('DROP TABLE OSMCSETTINGS', [])
			q = 'CREATE TABLE IF NOT EXISTS OSMCSETTINGS (key VARCHAR(255) PRIMARY KEY, value_bool TEXT, value_int TEXT, value_float BOOLEAN, value_str BOOLEAN)'
			db._database_execution(q, [])
			self.assertEqual(db._check_schema(), False)

	
	def test_wrongscheme(self):
		with fresh_database(self.dbpath) as db:
			db._database_execution('DROP TABLE OSMCSETTINGS', [])
			q = 'CREATE TABLE IF NOT EXISTS OSMCSETTINGS (key VARCHAR(255) PRIMARY KEY, value_bool TEXT, value_int TEXT, value_float BOOLEAN, value_str BOOLEAN)'
			db._database_execution(q, [])
			self.assertEqual(db._check_schema(), False)

	
	def test_sqlerror(self):
		with fresh_database(self.dbpath) as db:
			with self.assertRaises(OperationalError):
				db._database_execution('SELECT "', [])

	
	def test_replacement_setting(self):
		with fresh_database(self.dbpath) as db:		
			for k, v in test_items.iteritems():
				self.assertEqual(db.setSetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))
				
			for k, v in test_items_replacements.iteritems():
				self.assertEqual(db.setSetting(k, v), [], msg='Failed to set replacement (%s, %s)' % (k, v))

	
	def test_replacement_getting(self):
		with fresh_database(self.dbpath) as db:	
			for k, v in test_items_replacements.iteritems():
				self.assertEqual(db.setSetting(k, v), [], msg='Failed to set replacement (%s, %s)' % (k, v))
			
			for k, v in test_items_replacements.iteritems():
				self.assertEqual(db.getSetting(k), v, msg='Failed to get replacement (%s)' % (k))	

	
	def test_default_processing(self):
		with fresh_database(self.dbpath, test_items) as db:
			self.assertIsInstance(db, DBInterface, msg='Processing default changes class type')

	
	def test_default_results(self):
		with fresh_database(self.dbpath, test_items) as db:
			self.assertEqual(len(db.errors), 0, msg='Importing of defaults throws error(s):\n%s' % ('\n'.join(db.errors)))

	
	def test_default_values(self):
		with fresh_database(self.dbpath, test_items) as db:
			for k, v in test_items.iteritems():
				self.assertEqual(db.getSetting(k), v, msg='Value added as default, different to original (%s)' % k)

	
	def test_CLI(self):
		
		for value in ['True', '1234','1.01','None']:
			self.assertEqual(CLI(['dbinterface.py']), 'add help')

			self.assertEqual(CLI(['dbinterface.py'], provided_db=self.dbpath), 'add help')
			self.assertEqual(CLI(['dbinterface.py', 'a', str(value)], provided_db=self.dbpath), 'Set "a" as "%s"' % value)

			self.assertEqual(CLI(['dbinterface.py', 'a'], provided_db=self.dbpath), str(value))
			self.assertEqual(len(CLI(['dbinterface.py', '-a'], provided_db=self.dbpath)), 168)

		# too many arguments
		self.assertEqual(CLI(['dbinterface.py', 'a', 'b', 'c'], provided_db=self.dbpath), 'add help')

		os.remove(self.dbpath)

	
	def test_bad_default_dict(self):
		with self.assertRaises(AttributeError):
			with fresh_database(self.dbpath, []) as db:
				pass   # pragma: no cover

	
	def test_bad_default_key(self):
		defaults = {1:'a'}
		with fresh_database(self.dbpath, defaults) as db:
			self.assertEqual(len(db.errors), 1)


	def test_get_settingfunction(self):
			
		self.assertEqual(get_setting('junk_key', provided_db=self.dbpath), "KeyError: Key not found in database")

		with fresh_database(self.dbpath) as db:
			db.setSetting('a','1234')
			self.assertEqual(get_setting('a', provided_db=self.dbpath), '1234')


	def test_CLI_osmcgetperfs_noargs(self):

		with fresh_database(self.dbpath, {'a':'1234'}) as db:
			self.assertEqual(len(CLI(['osmc_getperfs'], provided_db=self.dbpath)), 168)

			self.assertEqual(CLI(['dbinterface.py', 'a'], provided_db=self.dbpath), '1234')

