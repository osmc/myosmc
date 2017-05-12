#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from dbinterface import DBInterface

DATABASE_PATH = "/home/osmc/.myosmc/preferences.db"


def get_all_settings(provided_db=None):

    response = []

    kv = DBInterface(provided_db).all_pairs().items()
    response.append('%-20s %-20s' % ('\n Key', ' Value'))
    response.append('-------------------- --------------------')
    kv.sort()
    for k, v in kv:
        response.append('%-20s %-20s' % (k, v))
    response.append('\n-----------------------------------------')
    return response


def get_setting(key, provided_db=None):

    try:
        return DBInterface(dbpath=provided_db).getsetting(key)
    except KeyError:
        return "KeyError: Key not found in database"


def osmcprefs(args, provided_db=None):

    response = []

    if len(args) <= 1:

        if args[0].lower().endswith('osmc_getperfs'):
            response = get_all_settings(provided_db=provided_db)
        else:
            response.append('add help')

    elif len(args) == 2:
        if args[1] == '-a':
            response = get_all_settings(provided_db=provided_db)

        else:
            # process a GET request using the default db location
            r = get_setting(args[1], provided_db=provided_db)
            response.append(str(r))

    elif len(args) == 3:  # No magic needed for osmc_setprefs, as it will still have 3 args
        # process a SET request with the default db location
        key = args[1]
        value = args[2]
        if value.lower() in ['true', 'false']:
            DBInterface(dbpath=provided_db).setsetting(key, bool(value), bool)
        else:
            try:
                DBInterface(dbpath=provided_db).setsetting(key, int(value), int)
            except ValueError:
                try:
                    DBInterface(dbpath=provided_db).setsetting(key, float(value), float)
                except ValueError:
                    DBInterface(dbpath=provided_db).setsetting(key, value)
        response.append('Set "%s" as "%s"' % (args[1], args[2]))

    else:
        response.append('add help')

    return '\n'.join(response)


if __name__ == '__main__':   # pragma: no cover

    dbpath = os.environ['DBPATH'] if 'DBPATH' in os.environ else DATABASE_PATH

    print(osmcprefs(sys.argv, provided_db=dbpath))
