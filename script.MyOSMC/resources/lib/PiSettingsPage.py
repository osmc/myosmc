
# XBMC Modules
import xbmc
import xbmcaddon
import xbmcgui

# STANDARD Modules
import subprocess
import sys
import os
import threading
import traceback

from piconfig import ConfigFileInterface, MASTER_SETTINGS
from CommonTools import *

__addon__  = xbmcaddon.Addon()
DIALOG     = xbmcgui.Dialog()


lang = language(__addon__=__addon__).lang
log  = logger(whodisis='PiConfig').log

class PageLauncher(threading.Thread):


	def __init__(self, gui, location='/boot/config.txt'):

		self.config_interface = ConfigFileInterface(location)
		self.gui = gui

	def run(self):

		# get the settings as they are in the config.txt
		self.configfile = self.config_interface.read_config_txt()
		config_settings = self.config_interface.extract_settings_from_doc(self.configfile)

		# Launch the page, populating the settings with the values that have been retrieved


		# on close of that page, get the new settings
		new_settings = """{something or other}"""

		# update all the settings with their new values.
		self.configfile = self.config_interface.update_settings(self.configfile, new_settings)

		# write the new config
		self.config_interface.write_config_txt(self.configfile, OpenWithBackup=OpenWithBackup)



	def get_defaults(self):

		return {key: value[default] for key, value in MASTER_SETTINGS.iteritems()}



if __name__ == "__main__":
	pass

