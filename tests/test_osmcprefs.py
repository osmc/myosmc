import env
import os
import unittest

from sqlite3 import OperationalError

from lib.database.osmcprefs import osmcprefs, _get_setting
from test_data.test_entries import test_items, test_items_replacements
from test_dbinterface import FreshDatabase


class OsmcprefsTest(unittest.TestCase):

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

        # del os.environ['DBPATH']

        try:
            os.remove(self.dbpath)   # pragma: no cover
        except:
            pass

    def test__get_setting_junkkey(self):

        with FreshDatabase() as db:
            self.assertEqual(_get_setting('junk_key', db=db), "KeyError: Key not found in database")

    def test__get_setting_validkey(self):

        with FreshDatabase(preload={'a':'1234'}) as db:
            self.assertEqual(_get_setting('a', db=db), '1234')

    def test_osmcprefs_osmcgetperfs_noargs(self):

        with FreshDatabase(preload={'a': '1234'}):
            self.assertEqual(len(osmcprefs(['osmc_getperfs'])), 168)

            self.assertEqual(osmcprefs(['osmc_getperfs', 'a']), '1234')

    def test_osmcprefs(self):

        for value in ['True', '1234', '1.01', 'None']:
            self.assertEqual(osmcprefs(['dbinterface.py']), 'add help')

            self.assertEqual(osmcprefs(['dbinterface.py']), 'add help')

            self.assertEqual(osmcprefs(['dbinterface.py', 'a', str(value)]), 'Set "a" as "%s"' % value)

            self.assertEqual(osmcprefs(['dbinterface.py', 'a']), str(value))

            self.assertEqual(len(osmcprefs(['dbinterface.py', '-a'])), 168)

        # too many arguments
        self.assertEqual(osmcprefs(['dbinterface.py', 'a', 'b', 'c']), 'add help')
