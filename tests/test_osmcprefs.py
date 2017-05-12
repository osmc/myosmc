import env
import os
import unittest

from sqlite3 import OperationalError

from lib.database.osmcprefs import osmcprefs, get_setting
from test_data.test_entries import test_items, test_items_replacements
from test_dbinterface import FreshDatabase


class OsmcprefsTest(unittest.TestCase):

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
            os.remove(self.dbpath)   # pragma: no cover
        except:
            pass

    def test_get_settingfunction(self):

        self.assertEqual(get_setting('junk_key', provided_db=self.dbpath), "KeyError: Key not found in database")

        with FreshDatabase(self.dbpath) as db:
            db.setsetting('a', '1234')
            self.assertEqual(get_setting('a', provided_db=self.dbpath), '1234')

    def test_osmcprefs_osmcgetperfs_noargs(self):

        with FreshDatabase(self.dbpath, {'a': '1234'}):
            self.assertEqual(len(osmcprefs(['osmc_getperfs'], provided_db=self.dbpath)), 168)

            self.assertEqual(osmcprefs(['osmc_getperfs', 'a'], provided_db=self.dbpath), '1234')

    def test_osmcprefs(self):

        for value in ['True', '1234', '1.01', 'None']:
            self.assertEqual(osmcprefs(['dbinterface.py']), 'add help')

            self.assertEqual(osmcprefs(['dbinterface.py'], provided_db=self.dbpath), 'add help')

            self.assertEqual(osmcprefs(['dbinterface.py', 'a', str(value)], provided_db=self.dbpath), 'Set "a" as "%s"' % value)

            self.assertEqual(osmcprefs(['dbinterface.py', 'a'], provided_db=self.dbpath), str(value))

            self.assertEqual(len(osmcprefs(['dbinterface.py', '-a'], provided_db=self.dbpath)), 168)

        # too many arguments
        self.assertEqual(osmcprefs(['dbinterface.py', 'a', 'b', 'c'], provided_db=self.dbpath), 'add help')

        os.remove(self.dbpath)
