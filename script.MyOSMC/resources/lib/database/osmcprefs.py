#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from dbinterface import DBInterface


def _get_all_settings(db):

    response = []

    kv = db.all_pairs().items()
    response.append('%-20s %-20s' % ('\n Key', ' Value'))
    response.append('-------------------- --------------------')
    kv.sort()
    for k, v in kv:
        response.append('%-20s %-20s' % (k, v))
    response.append('\n-----------------------------------------')
    return response


def _get_setting(key, db):

    try:
        return db.getsetting(key)
    except KeyError:
        return "KeyError: Key not found in database"


def osmcprefs(args):

    db = DBInterface()

    response = []

    if len(args) <= 1:

        if args[0].lower().endswith('osmc_getperfs'):
            response = _get_all_settings(db=db)
        else:
            response.append('add help')

    elif len(args) == 2:
        if args[1] == '-a':
            response = _get_all_settings(db=db)

        else:
            # process a GET request using the default db location
            r = _get_setting(args[1], db=db)
            response.append(str(r))

    elif len(args) == 3:  # No magic needed for osmc_setprefs, as it will still have 3 args
        # process a SET request with the default db location
        key = args[1]
        value = args[2]
        if value.lower() in ['true', 'false']:
            db.setsetting(key, bool(value), bool)
        else:
            try:
                db.setsetting(key, int(value), int)
            except ValueError:
                try:
                    db.setsetting(key, float(value), float)
                except ValueError:
                    db.setsetting(key, value)
        response.append('Set "%s" as "%s"' % (args[1], args[2]))

    else:
        response.append('add help')

    return '\n'.join(response)


if __name__ == '__main__':   # pragma: no cover

    print(osmcprefs(sys.argv))
