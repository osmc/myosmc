import env
import os
import unittest

from sqlite3 import OperationalError

from lib.database.osmcprefs import osmcprefs, _get_setting
from test_data.test_entries import test_items, test_items_replacements
from test_database_dbinterface import FreshDatabase


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
        del os.environ['DBPATH']
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

    def test_osmcprefs_getprefs_noargs(self):

        with FreshDatabase(preload={'a': '1234'}):
            self.assertEqual(len(osmcprefs(*['osmc_getprefs'])), 168)

            self.assertEqual(osmcprefs(*['osmc_getprefs', 'a']), '1234')

    def test_osmcprefs_getprefs_toomany_args(self):
        # the function should just ignore the extra arguments
        with FreshDatabase(preload={'mykey': 'myvalue'}) as db:
            self.assertEqual(osmcprefs(*['osmc_getprefs', 'mykey', 'extra']), 'myvalue')

    def test_osmcprefs_setprefs_insuf_args(self):
        error = 'Error, no params provided\Example: osmc_setprefs key value'
        with FreshDatabase() as db:
            self.assertEqual(osmcprefs(*['osmc_setprefs']), error)
            self.assertEqual(osmcprefs(*['osmc_setprefs', 'key']), error)

    def test_osmcprefs_setprefs_success(self):
        with FreshDatabase() as db:
            self.assertEqual(osmcprefs(*['osmc_setprefs', 'mykey', 'myvalue']), 'Set "mykey" to "myvalue"')
            self.assertEqual(db.getsetting('mykey'), 'myvalue')

    def test_osmcprefs_setprefs_toomany_args(self):
        # the function should just ignore the extra arguments
        with FreshDatabase() as db:
            self.assertEqual(osmcprefs(*['osmc_setprefs', 'mykey', 'myvalue', 'extra']), 'Set "mykey" to "myvalue"')

    def test_osmcprefs_setget_all_types(self):
        for value in ['True', '1234', '1.01', 'None']:
            with FreshDatabase() as db:
                self.assertEqual(osmcprefs(*['osmc_setprefs', 'a', str(value)]), 'Set "a" to "%s"' % value)
                self.assertEqual(osmcprefs(*['osmc_getprefs', 'a']), str(value))
