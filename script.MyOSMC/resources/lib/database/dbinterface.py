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

from functools import partial
import os
import sqlite3
from time import sleep


DATABASE_PATH="/home/osmc/.myosmc/preferences.db"


class database_connection(object):
	''' Context manager for database activity.

	Context managers ensure clean exiting of database interaction. The code
	in the __exit__ method always runs, even if the function throws an error.
	'''

	def __init__(self, dbpath, *args, **kwargs):
		self.dbpath = dbpath
		self.con = None

	def __enter__(self, *args, **kwargs):

		self.con = sqlite3.connect(self.dbpath, timeout=1)

		return self.con

	def __exit__(self, *args):
		
		# Try to commit the executed actions.
		try:
			self.con.commit()
		except:
			pass

		self.con.close()


class DBInterface(object):
	''' Python Interface for the OSMC settings database.

	The OSMC settings database stores the settings for the OSMC addon and
	other clients.

	The database stores booleans, integers, floats and strings only.

	Keys are intended to be unique across all the standard tables. 

	Attributes:
		errors: list of errors encountered during default import.
		table_info: dictionary containing the table names as keys, and the datatype as values.

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

		self.key_type = 'VARCHAR(255)'
		self.table_info = { 'OSMCBOOL' :'INTEGER',
							'OSMCINT'  :'INTEGER',
							'OSMCFLOAT':'REAL',
							'OSMCSTR'  :'TEXT' }

		self.errors = []
		
		self.path = DATABASE_PATH if path is None else path

		if not self._check_file():
			self._create_file()

		if not self._check_schema():
			self._create_schema()

		self.defaults = defaults

		if defaults is not None:
			try:
				for key, value in defaults.iteritems():
					try:
						self.setSetting(key, value)
					except Exception as e:
						errors.append((key, e))
						continue

			except AttributeError:
				raise AttributeError('defaults not a dictionary')


	def getSetting(self, key):
		''' Retrieves the data associated with the key in the OSMC database.
		
		Method looks for key in bool table first, then integers, then floats, and finally strings.
		
		Arguments:
			key (str): must be alphanumeric. Converted to lowercase on prior to lookup.

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

		try:
			return self._get_bool(key)
		except KeyError:
			pass

		try:
			return self._get_int(key)
		except KeyError:
			pass

		try:
			return self._get_float(key)
		except KeyError:
			pass			

		return self._get_string(key)


	def setSetting(self, key, value, datatype=None, force_overwrite=False):
		''' Stores a single key:value pair in the OSMC database.

		Arguments:
			key (str): must be alphanumeric. Keys are stored in lowercase only, but get converted to lowercase 
						on lookup.
			value (bool|int|float|string): the value to be stored in the database.
			datatype (type, optional): The type of data that is being stored. Defaults to None. This is not 
						strictly required, but would operate as a 'type hint' and make the code easier to read.
			force_overwrite (bool): flag to override the duplicate check and remove the instance of the key 
						from the table in which it currently resides.

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

		existing_table = self._test_key_existence(key)

		test = partial( self._test_setting,
						key=key, 
						value=value, 
						datatype=datatype, 
						existing_table=existing_table, 
						force_overwrite=force_overwrite )

		if datatype == int and test(table='OSMCINT'):
				return self._set_int(key, value)

		elif datatype == float and test(table='OSMCFLOAT'):
				return self._set_float(key, value)

		elif datatype == bool and test(table='OSMCBOOL'):
				return self._set_bool(key, value)

		elif test(value=str(value), datatype=str, table='OSMCSTR'):
				return self._set_string(key, str(value))


	def allPairs(self):
		''' Returns all the data stored in the database, as a python dictionary.'''

		stub = 'SELECT key, value FROM %s"'
		q = ' UNION '.join([stub % table_name for table_name in self.table_info.keys()])
		r = self._database_execution(q)

		return dict(r)


	def _test_setting(self, key, value, datatype, table, existing_table, force_overwrite):

		# test to confirm that the value is the correct type
		try:
			self._confirm_type(value, datatype)
		except TypeError:
			raise TypeError('Value does not match specified datatype (%s)' % datatype)

		# test to confirm that the key is unique, or relates to an entry on the 
		# table corresponding to the values datatype
		if existing_table is not None and table != existing_table:

			# force_overwrite means we drop the duplicate and write our value instead
			if force_overwrite:
				self._drop_setting(key, existing_table)
			else:
				raise KeyError('Duplicate key found for conflicting datatype: %s' % table)

		return True


	def _confirm_type(self, value, datatype):

		if not isinstance(value, datatype):
			raise TypeError


	def _test_key_existence(self, key):

		stub = 'SELECT key, "%s" FROM %s WHERE key="%s"'
		q = ' UNION '.join([stub % (table_name, table_name, key) for table_name in self.table_info.keys()])
		r = self._database_execution(q)
		
		if r is None or not r:
			return None
		
		# this shouldn't occur unless the user has added something manually
		if len(r) > 1:
			raise KeyError('Duplicate existing keys found')

		return r[0][1]


	def _fetch(self, key, from_table):

		q = 'SELECT VALUE FROM %s WHERE key="%s"' % (from_table, key)
		r = self._database_execution(q)

		if r is None or not r:
			raise KeyError

		return r[0][0]


	def _fling(self, key, value, to_table):
		
		q = 'INSERT OR REPLACE INTO %s (key, value) VALUES ("%s", %s)' % (to_table, key, value)
		r = self._database_execution(q)


	def _get_string(self, key):
		
		return self._fetch(key, from_table='OSMCSTR')
		

	def _set_string(self, key, value):

		value = '"' + value + '"'
		
		return self._fling(key, value, to_table='OSMCSTR')
		

	def _get_int(self, key):
		
		return self._fetch(key, from_table='OSMCINT')
		

	def _set_int(self, key, value):
		
		return self._fling(key, value, to_table='OSMCINT')
		

	def _get_bool(self, key):

		if self._fetch(key, from_table='OSMCBOOL') == 1:
			return True

		return False
		

	def _set_bool(self, key, value):

		value = 1 if value == True else 0
		
		return self._fling(key, value, to_table='OSMCBOOL')


	def _get_float(self, key):
		
		return self._fetch(key, from_table='OSMCFLOAT')
		

	def _set_float(self, key, value):
		
		return self._fling(key, value, to_table='OSMCFLOAT')


	def _drop_setting(self, key, table):

		q = 'DELETE FROM %s WHERE key="%s"' % (table, key)
		r = self._database_execution(q)


	def _check_file(self):

		return os.path.isfile(self.path)


	def _create_file(self):

		return self._create_schema()


	def _check_schema(self):

		table_string = '","'.join(self.table_info.keys())

		for table_name, datatype in self.table_info.iteritems():
			q = 'PRAGMA table_info(%s)' % table_name
			r = self._database_execution(q)
			if r[0][2] != self.key_type or r[1][2] != datatype:
					return False

		return True
		

	def _create_schema(self):

		for table_name, datatype in self.table_info.iteritems():
			r = self._database_execution('DROP TABLE IF EXISTS %s' % table_name)
			q = 'CREATE TABLE IF NOT EXISTS %s (key %s PRIMARY KEY, value %s)' % (table_name, self.key_type, datatype)
			r = self._database_execution(q)
		
		return None


	def _database_execution(self, action):

		# If the database is locked, retry for 2.5 seconds before throwing an error.
		max_time = 0
		while max_time < 25:
			try:
				with database_connection(self.path) as con:	
					return con.execute(action).fetchall()
					
			except sqlite3.OperationalError:
				max_time += 1
				sleep(0.1)

		else:
			raise sqlite3.OperationalError



if __name__ == '__main__':
	# path='C:\\t\\test.db'
	# db = DBInterface(path)
	# db.setSetting('a',12122, force_overwrite=True)

	# print db.getSetting('a')

	print help(DBInterface)
