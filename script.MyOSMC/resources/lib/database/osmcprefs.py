#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


def osmcprefs(whodat, key=None, value=None, *args):

    db = DBInterface()
    whodat = whodat.lower()

    if whodat.endswith('osmc_getprefs'):

        if key is None:
            return '\n'.join(_get_all_settings(db=db))

        else:
            return str(_get_setting(key, db=db))

    elif whodat.endswith('osmc_setprefs'):

        if key is None or value is None:
            return 'Error, no params provided\Example: osmc_setprefs key value'

        else:
            if value.lower() in ['true', 'false']:
                db.setsetting(key, bool(value), bool)
            else:
                try:
                    db.setsetting(key, int(value), int)
                except ValueError:
                    try:
                        db.setsetting(key, float(value), float)
                    except ValueError:
                        try:
                            db.setsetting(key, value)
                        except:   # pragma: no cover
                            return 'Failed to set value'

            return 'Set "%s" to "%s"' % (key, value)


if __name__ == '__main__':   # pragma: no cover

    print(osmcprefs(*sys.argv))
