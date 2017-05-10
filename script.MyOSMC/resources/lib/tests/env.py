import os
import sys

from mock import Mock

# this appends the lib folder to system path
# you will need to refer to underlying modules directly in your test imports
# for example, from database.dbinterface import DBInterface
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.modules['xbmc'] = Mock()
sys.modules['xbmcaddon'] = Mock()
sys.modules['xbmcgui'] = Mock()
sys.modules['xbmccvfs'] = Mock()
