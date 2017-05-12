
import env
import os
import unittest

from mock import patch
from sqlite3 import OperationalError
from lib.database.dbinterface import DBInterface
from test_data.test_entries import test_items, test_items_replacements


class FreshDatabase(object):   # pragma: no cover

    def __init__(self, preload=None):

        self.preload = preload

    def __enter__(self, *args, **kwargs):

        self.db = DBInterface(preload=self.preload)

        return self.db

    def __exit__(self, *args, **kwargs):

        os.remove(os.environ['DBPATH'])


class DBInterfaceTest(unittest.TestCase):

    def setUp(self):

        self.dbpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data', 'test.db')

        os.environ['DBPATH'] = self.dbpath

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
        with FreshDatabase() as db:
            for k, v in test_items.iteritems():
                self.assertEqual(db.setsetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

    def test_getting(self):
        with FreshDatabase() as db:
            for k, v in test_items.iteritems():
                self.assertEqual(db.setsetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

            for k, v in test_items.iteritems():
                self.assertEqual(db.getsetting(k), v, msg='Failed to get (%s)' % (k))

    def test_all_pairs_returntype(self):
        with FreshDatabase() as db:
            for k, v in test_items.iteritems():
                self.assertEqual(db.setsetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

            self.assertIsInstance(db.all_pairs(), dict, msg='Output of all_pairs is not a dict')

    def test_all_pairs(self):
        with FreshDatabase() as db:
            for k, v in test_items.iteritems():
                self.assertEqual(db.setsetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

            ap = db.all_pairs()
            for k, v in test_items.iteritems():
                self.assertIn(k, ap, msg='Key (%s) not found in all_pairs' % k)
                self.assertEqual(ap[k], v, msg='Value in all_pairs not equal to original item')

    def test_unknownkey(self):
        with FreshDatabase() as db:
            with self.assertRaises(KeyError):
                db.getsetting('unknownkey')

    def test_bool_type_mismatch(self):
        with FreshDatabase() as db:
            with self.assertRaises(TypeError):
                db.setsetting('a', 1, datatype=bool)

    def test_int_type_mismatch(self):
        with FreshDatabase() as db:
            with self.assertRaises(TypeError):
                db.setsetting('a', 'test', datatype=int)

    def test_float_type_mismatch(self):
        with FreshDatabase() as db:
            with self.assertRaises(TypeError):
                db.setsetting('a', 'test', datatype=float)

    def test_keynotstring_set(self):
        with FreshDatabase() as db:
            with self.assertRaises(TypeError):
                db.setsetting(1, 'a')

    def test_keynotstring_get(self):
        with FreshDatabase() as db:
            with self.assertRaises(TypeError):
                db.getsetting(1)

    @patch('time.sleep')
    def test_wrongschema_startup(self, mock_sleep):
        with FreshDatabase() as db:
            db._database_execution('DROP TABLE OSMCSETTINGS', [])
            q = '''CREATE TABLE IF NOT EXISTS OSMCSETTINGS (key VARCHAR(255) PRIMARY KEY, value_bool TEXT,
                    value_int TEXT, value_float BOOLEAN, value_str BOOLEAN)'''
            db._database_execution(q, [])
            self.assertEqual(db._check_schema(), False)

    @patch('time.sleep')
    def test_wrongscheme(self, mock_sleep):
        with FreshDatabase() as db:
            db._database_execution('DROP TABLE OSMCSETTINGS', [])
            q = '''CREATE TABLE IF NOT EXISTS OSMCSETTINGS (key VARCHAR(255) PRIMARY KEY, value_bool TEXT,
                value_int TEXT, value_float BOOLEAN, value_str BOOLEAN)'''
            db._database_execution(q, [])
            self.assertEqual(db._check_schema(), False)

    @patch('time.sleep')
    def test_sqlerror(self, mock_sleep):
        # _database_execution can take 2.5 seconds to fail, mocking sleep removes this delay
        with FreshDatabase() as db:
            with self.assertRaises(OperationalError):
                db._database_execution('SELECT "', [])

    def test_replacement_setting(self):
        with FreshDatabase() as db:
            for k, v in test_items.iteritems():
                self.assertEqual(db.setsetting(k, v), [], msg='Failed to set (%s, %s)' % (k, v))

            for k, v in test_items_replacements.iteritems():
                self.assertEqual(db.setsetting(k, v), [], msg='Failed to set replacement (%s, %s)' % (k, v))

    def test_replacement_getting(self):
        with FreshDatabase() as db:
            for k, v in test_items_replacements.iteritems():
                self.assertEqual(db.setsetting(k, v), [], msg='Failed to set replacement (%s, %s)' % (k, v))

            for k, v in test_items_replacements.iteritems():
                self.assertEqual(db.getsetting(k), v, msg='Failed to get replacement (%s)' % (k))

    def test_default_processing(self):
        with FreshDatabase(test_items) as db:
            self.assertIsInstance(db, DBInterface, msg='Processing default changes class type')

    def test_default_results(self):
        with FreshDatabase(test_items) as db:
            self.assertEqual(len(db.errors), 0, msg='Importing of defaults throws error(s):\n%s' % ('\n'.join(db.errors)))

    def test_default_values(self):
        with FreshDatabase(test_items) as db:
            for k, v in test_items.iteritems():
                self.assertEqual(db.getsetting(k), v, msg='Value added as default, different to original (%s)' % k)

    def test_bad_default_dict(self):
        with self.assertRaises(AttributeError):
            with FreshDatabase([]):
                pass   # pragma: no cover

    def test_bad_default_key(self):
        preload = {1: 'a'}
        with FreshDatabase(preload) as db:
            self.assertEqual(len(db.errors), 1)
