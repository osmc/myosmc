""" environment file
 - adds the resources folder to the system path.
 - pre-mocks the xbmc modules which are usually unavailable in our development environment.
."""

# !/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys

from mock import Mock

# this appends the lib folder to system path
# you will need to refer to underlying modules directly in your test imports
# for example, from database.dbinterface import DBInterface
myosmc_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(myosmc_folder, 'script.MyOSMC', 'resources'))

sys.modules['xbmc'] = Mock()
sys.modules['xbmcaddon'] = Mock()
sys.modules['xbmcgui'] = Mock()
sys.modules['xbmccvfs'] = Mock()
