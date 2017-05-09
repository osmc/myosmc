import sys
import os

# this appends the lib folder to system path
# you will need to refer to underlying modules directly in your test imports
# for example, from database.dbinterface import DBInterface
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

