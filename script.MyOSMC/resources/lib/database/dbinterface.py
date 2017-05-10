#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dbinterface.py
#
#  Copyright 2017 sam <sam@sam-XPS-15-9550>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from __future__ import print_function

import sqlite3
import sys
from time import sleep


DATABASE_PATH = "/home/osmc/.myosmc/preferences.db"


class DatabaseConnection(object):
    ''' Context manager for database activity.

    Context managers ensure clean exiting of database interaction. The code
    in the __exit__ method always runs, even if the function throws an error.
    '''

    def __init__(self, dbpath, *args, **kwargs):
        self.dbpath = dbpath
        self.con = None

    def __enter__(self, *args, **kwargs):

        self.con = sqlite3.connect(self.dbpath, timeout=1)

        return self.con.cursor()

    def __exit__(self, *args):
        self.con.commit()
        self.con.close()


class DBInterface(object):
    ''' Python Interface for the OSMC settings database.

    The OSMC settings database stores the settings for the OSMC addon and
    other clients.

    The database stores booleans, integers, floats and strings only.

    Keys are intended to be unique across all the standard tables.

    Attributes:
        errors: list of errors encountered during default import.

    Raises:
        sqlite3.OperationalError: when the database is locked and unable to execute an action within 2.5 seconds.
    '''

    def __init__(self, path=None, defaults=None):
        ''' The __init__ method checks for the existence of the database file. If
        the database is not found, a new file is created. The new database is pre-loaded with
        the default values of certain vital OSMC settings.

        Arguments:
            path (str): path to the database file.
            defaults (dict): a dictionary containing the default values for a number of settings.

        Raises:
            AttributeError: when the defaults argument is not a valid dictionary.
        '''

        self.errors = []

        self.path = DATABASE_PATH if path is None else path

        if not self._check_schema():
            self._create_schema()

        self.defaults = defaults

        if defaults is not None:
            try:
                for key, value in defaults.iteritems():
                    try:
                        self.setsetting(key, value)
                    except Exception as e:
                        self.errors.append((key, e))
                        continue

            except AttributeError:
                raise AttributeError('defaults not a dictionary')

    def getsetting(self, key):
        ''' Retrieves the data associated with the key in the OSMC database.

        Arguments:
            key (str): must be alphanumeric. Converted to lowercase prior to lookup.

        Returns:
            (bool|int|float|string) value associated with the provided key.

        Raises:
            KeyError: when the value cannot be found in the database with the provided key.
        '''

        try:
            self._confirm_type(key, str)
        except TypeError:
            raise TypeError('Key is not string')

        key = key.lower()

        return self._fetch(key)

    def setsetting(self, key, value, datatype=None):
        ''' Stores a single key:value pair in the OSMC database.

        Arguments:
            key (str): must be alphanumeric. Keys are stored in lowercase only, but get converted to lowercase
                        on lookup.
            value (bool|int|float|string): the value to be stored in the database.
            datatype (type, optional): The type of data that is being stored. Defaults to None. This is not
                        strictly required, but would operate as a 'type hint' and make the code easier to read.

        Raises:
            KeyError: when there are duplicate keys found
            TypeError: when key is not a string.
                     : when specified datatype does not match the actual type of the data.
            IOError: when the database does not exist, or otherwise cannot be read.
        '''

        try:
            self._confirm_type(key, str)
        except TypeError:
            raise TypeError('Key is not string')

        datatype = type(value) if datatype is None else datatype

        key = key.lower()

        if datatype == bool:
            if not isinstance(value, bool):
                raise TypeError('Value type does not match type provided.')
            return self._fling(key, value, None, None, None)

        elif datatype == int:
            if not isinstance(value, int):
                raise TypeError('Value type does not match type provided.')
            return self._fling(key, None, value, None, None)

        elif datatype == float:
            if not isinstance(value, float):
                raise TypeError('Value type does not match type provided.')
            return self._fling(key, None, None, value, None)

        else:
            return self._fling(key, None, None, None, str(value))

    def all_pairs(self):
        ''' Returns all the data stored in the database, as a python dictionary.'''

        q = 'SELECT * FROM OSMCSETTINGS'
        r = self._database_execution(q, {})

        r = [(x[0], self._extract_value([x])) for x in r]

        return dict(r)

    def _extract_value(self, result_tuple):

        r = [(i, v) for i, v in enumerate(result_tuple[0])][1:5]

        num, value = [x for x in r if x[1] is not None][0]

        if num == 1:  # boolean datapoint
            return value == 1

        elif value == 'None':  # string None values should be restored to actual None
            value = None

        return value

    def _confirm_type(self, value, datatype):

        if not isinstance(value, datatype):
            raise TypeError

    def _fetch(self, key):

        q = 'SELECT * FROM OSMCSETTINGS WHERE key=?'
        args = [key]
        r = self._database_execution(q, args)
        if r is None or not r:
            raise KeyError

        return self._extract_value(r)

    def _fling(self, key, value_bool, value_int, value_float, value_str):

        q = '''INSERT OR REPLACE INTO OSMCSETTINGS (key, value_bool, value_int, value_float, value_str) VALUES (?,?,?,?,?)
            '''
        args = (key, value_bool, value_int, value_float, value_str,)
        r = self._database_execution(q, args)
        return r

    def _check_schema(self):

        q = 'PRAGMA table_info(OSMCSETTINGS)'
        r = self._database_execution(q, [])

        if not r or set([x[2] for x in r]) != set(['VARCHAR(255)', 'INTEGER', 'INTEGER', 'REAL', 'TEXT']):
            return False

        return True

    def _create_schema(self):

        q = '''CREATE TABLE IF NOT EXISTS OSMCSETTINGS (key VARCHAR(255) PRIMARY KEY, value_bool INTEGER,
                value_int INTEGER, value_float REAL, value_str TEXT)'''
        self._database_execution(q, [])

        return None

    def _database_execution(self, action, args):

        # If the database is locked, retry for 2.5 seconds before throwing an error.
        max_time = 0
        while max_time < 25:
            try:
                with DatabaseConnection(self.path) as con:
                    return con.execute(action, args).fetchall()

            except sqlite3.OperationalError:
                max_time += 1
                sleep(0.1)

        else:
            raise sqlite3.OperationalError


def get_all_settings(provided_db=None):

    response = []
    global DATABASE_PATH

    DATABASE_PATH = provided_db if provided_db is not None else DATABASE_PATH

    kv = DBInterface(DATABASE_PATH).all_pairs().items()
    response.append('%-20s %-20s' % ('\n Key', ' Value'))
    response.append('-------------------- --------------------')
    kv.sort()
    for k, v in kv:
        response.append('%-20s %-20s' % (k, v))
    response.append('\n-----------------------------------------')
    return response


def get_setting(key, provided_db=None):

    global DATABASE_PATH

    DATABASE_PATH = provided_db if provided_db is not None else DATABASE_PATH

    try:
        return DBInterface(path=DATABASE_PATH).getsetting(key)
    except KeyError:
        return "KeyError: Key not found in database"


def cl_interface(args, provided_db=None):
    global DATABASE_PATH

    DATABASE_PATH = provided_db if provided_db is not None else DATABASE_PATH

    response = []

    if len(args) <= 1:

        if args[0].lower().endswith('osmc_getperfs'):
            response = get_all_settings(provided_db=DATABASE_PATH)
        else:
            response.append('add help')

    elif len(args) == 2:
        if args[1] == '-a':
            response = get_all_settings(provided_db=DATABASE_PATH)

        else:
            # process a GET request using the default db location
            r = get_setting(args[1], provided_db=DATABASE_PATH)
            response.append(str(r))

    elif len(args) == 3:  # No magic needed for osmc_setprefs, as it will still have 3 args
        # process a SET request with the default db location
        key = args[1]
        value = args[2]
        if value.lower() in ['true', 'false']:
            DBInterface().setsetting(key, bool(value), bool)
        else:
            try:
                DBInterface().setsetting(key, int(value), int)
            except ValueError:
                try:
                    DBInterface().setsetting(key, float(value), float)
                except ValueError:
                    DBInterface().setsetting(key, value)
        response.append('Set "%s" as "%s"' % (args[1], args[2]))

    else:
        response.append('add help')

    return '\n'.join(response)


if __name__ == '__main__':   # pragma: no cover

    # DATABASE_PATH='C:\\t\\test.db'
    print(cl_interface(sys.argv))
