
import env
import os
import unittest

from sqlite3 import OperationalError

from database.dbinterface import DBInterface, cl_interface, get_setting

from test_data.test_entries import test_items, test_items_replacements


class FreshDatabase(object):   # pragma: no cover

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

        self.dbpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data', 'test.db')
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
        with FreshDatabase(self.dbpath) as db:
            for k, v in test_items.iteritems():
                self.assertEqual(db.setsetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

    def test_getting(self):
        with FreshDatabase(self.dbpath) as db:
            for k, v in test_items.iteritems():
                self.assertEqual(db.setsetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

            for k, v in test_items.iteritems():
                self.assertEqual(db.getsetting(k), v, msg='Failed to get (%s)' % (k))

    def test_all_pairs_returntype(self):
        with FreshDatabase(self.dbpath) as db:
            for k, v in test_items.iteritems():
                self.assertEqual(db.setsetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

            self.assertIsInstance(db.all_pairs(), dict, msg='Output of all_pairs is not a dict')

    def test_all_pairs(self):
        with FreshDatabase(self.dbpath) as db:
            for k, v in test_items.iteritems():
                self.assertEqual(db.setsetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

            ap = db.all_pairs()
            for k, v in test_items.iteritems():
                self.assertIn(k, ap, msg='Key (%s) not found in all_pairs' % k)
                self.assertEqual(ap[k], v, msg='Value in all_pairs not equal to original item')

    def test_unknownkey(self):
        with FreshDatabase(self.dbpath) as db:
            with self.assertRaises(KeyError):
                db.getsetting('unknownkey')

    def test_bool_type_mismatch(self):
        with FreshDatabase(self.dbpath) as db:
            with self.assertRaises(TypeError):
                db.setsetting('a', 1, datatype=bool)

    def test_int_type_mismatch(self):
        with FreshDatabase(self.dbpath) as db:
            with self.assertRaises(TypeError):
                db.setsetting('a', 'test', datatype=int)

    def test_float_type_mismatch(self):
        with FreshDatabase(self.dbpath) as db:
            with self.assertRaises(TypeError):
                db.setsetting('a', 'test', datatype=float)

    def test_keynotstring_set(self):
        with FreshDatabase(self.dbpath) as db:
            with self.assertRaises(TypeError):
                db.setsetting(1, 'a')

    def test_keynotstring_get(self):
        with FreshDatabase(self.dbpath) as db:
            with self.assertRaises(TypeError):
                db.getsetting(1)

    def test_wrongschema_startup(self):
        with FreshDatabase(self.dbpath) as db:
            db._database_execution('DROP TABLE OSMCSETTINGS', [])
            q = '''CREATE TABLE IF NOT EXISTS OSMCSETTINGS (key VARCHAR(255) PRIMARY KEY, value_bool TEXT,
                    value_int TEXT, value_float BOOLEAN, value_str BOOLEAN)'''
            db._database_execution(q, [])
            self.assertEqual(db._check_schema(), False)

    def test_wrongscheme(self):
        with FreshDatabase(self.dbpath) as db:
            db._database_execution('DROP TABLE OSMCSETTINGS', [])
            q = '''CREATE TABLE IF NOT EXISTS OSMCSETTINGS (key VARCHAR(255) PRIMARY KEY, value_bool TEXT,
                value_int TEXT, value_float BOOLEAN, value_str BOOLEAN)'''
            db._database_execution(q, [])
            self.assertEqual(db._check_schema(), False)

    def test_sqlerror(self):
        with FreshDatabase(self.dbpath) as db:
            with self.assertRaises(OperationalError):
                db._database_execution('SELECT "', [])

    def test_replacement_setting(self):
        with FreshDatabase(self.dbpath) as db:
            for k, v in test_items.iteritems():
                self.assertEqual(db.setsetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

            for k, v in test_items_replacements.iteritems():
                self.assertEqual(db.setsetting(k, v), [], msg='Failed to set replacement (%s, %s)' % (k, v))

    def test_replacement_getting(self):
        with FreshDatabase(self.dbpath) as db:
            for k, v in test_items_replacements.iteritems():
                self.assertEqual(db.setsetting(k, v), [], msg='Failed to set replacement (%s, %s)' % (k, v))

            for k, v in test_items_replacements.iteritems():
                self.assertEqual(db.getsetting(k), v, msg='Failed to get replacement (%s)' % (k))

    def test_default_processing(self):
        with FreshDatabase(self.dbpath, test_items) as db:
            self.assertIsInstance(db, DBInterface, msg='Processing default changes class type')

    def test_default_results(self):
        with FreshDatabase(self.dbpath, test_items) as db:
            self.assertEqual(len(db.errors), 0, msg='Importing of defaults throws error(s):\n%s' % ('\n'.join(db.errors)))

    def test_default_values(self):
        with FreshDatabase(self.dbpath, test_items) as db:
            for k, v in test_items.iteritems():
                self.assertEqual(db.getsetting(k), v, msg='Value added as default, different to original (%s)' % k)

    def test_cl_interface(self):

        for value in ['True', '1234', '1.01', 'None']:
            self.assertEqual(cl_interface(['dbinterface.py']), 'add help')

            self.assertEqual(cl_interface(['dbinterface.py'], provided_db=self.dbpath), 'add help')
            self.assertEqual(cl_interface(['dbinterface.py', 'a', str(value)], provided_db=self.dbpath), 'Set "a" as "%s"' % value)

            self.assertEqual(cl_interface(['dbinterface.py', 'a'], provided_db=self.dbpath), str(value))
            self.assertEqual(len(cl_interface(['dbinterface.py', '-a'], provided_db=self.dbpath)), 168)

        # too many arguments
        self.assertEqual(cl_interface(['dbinterface.py', 'a', 'b', 'c'], provided_db=self.dbpath), 'add help')

        os.remove(self.dbpath)

    def test_bad_default_dict(self):
        with self.assertRaises(AttributeError):
            with FreshDatabase(self.dbpath, []):
                pass   # pragma: no cover

    def test_bad_default_key(self):
        defaults = {1: 'a'}
        with FreshDatabase(self.dbpath, defaults) as db:
            self.assertEqual(len(db.errors), 1)

    def test_get_settingfunction(self):

        self.assertEqual(get_setting('junk_key', provided_db=self.dbpath), "KeyError: Key not found in database")

        with FreshDatabase(self.dbpath) as db:
            db.setsetting('a', '1234')
            self.assertEqual(get_setting('a', provided_db=self.dbpath), '1234')

    def test_cl_interface_osmcgetperfs_noargs(self):

        with FreshDatabase(self.dbpath, {'a': '1234'}):
            self.assertEqual(len(cl_interface(['osmc_getperfs'], provided_db=self.dbpath)), 168)

            self.assertEqual(cl_interface(['osmc_getperfs', 'a'], provided_db=self.dbpath), '1234')
