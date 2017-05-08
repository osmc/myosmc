import re
from MasterSettings import MASTER_SETTINGS
from piSettings import PassThrough, CLASS_LIBRARY


class ConfigFileInterface(object):

	def __init__(self, location='/boot/config.txt'):

		self.location = location
		self.OpenWithBackup = OpenWithBackup


	def _clean_this_line(self, original_line):

		clean_line = original_line

		clean_line = clean_line.strip()

		if not clean_line:
			return ''

		# ignore commented out lines
		if clean_line.startswith('#'):
			return ''

		# strip the line of any inline comments
		if '#' in clean_line: 
			clean_line = clean_line[:clean_line.index('#')]

			# restrip the line
			clean_line = clean_line.strip()

		return clean_line


	def _clean_this_doc(self, doc):

		# reverse the lines in the doc. 
		# the config.txt needs to be read from the bottom up
		doc = doc[::-1]

		clean_doc = []
		for original_line in doc:
			
			clean = self._clean_this_line(original_line)
			
			clean_doc.append( {'original': original_line, 'clean':clean, 'setting':None} )

		return clean_doc


	def _append_unmatched_settings_to_doc(self, clean_doc, _settings):
		# run through the settings again and add any that have not been assigned
		#  to the document with their default values
		for setting in _settings:

			if setting.foundinDoc:
				continue

			setting.set_current_value_to_default()

			clean_doc.append( {'original': 'NULL', 'clean':'NULL', 'setting':setting} )		

		return clean_doc


	def _assign_settings_to_doc(self, clean_doc, _settings):
		'''
		Goes through the clean doc, assigns a piSetting to each line.
		Settings that are not added to a line are added to the end of the document
		with their default values.
		This ensures that all settings in MASTERSETTINGS are represented in the final doc.
		'''

		for config_line in clean_doc:
			print '#' + config_line['clean']

			# check the config_line against all the settings, exiting loop on first valid find
			for setting in _settings:
				try:
					setting = setting.extract_setting_from_line( config_line )
					config_line['setting'] = setting
					
					symbol = '==' if str(setting.default_value) == str(setting.current_config_value) else '!='

					print 'Assigning -- %s %s %s \n' % (setting.default_value, symbol, setting.current_config_value)

					break  # go to the next config_line
				except ValueError:
					pass

			else: # if no break
				# passthrough the original line to the final document
				print 'passing through\n'
				config_line['setting'] = PassThrough(name='passthrough')

		return clean_doc


	def extract_settings_from_doc(self, final_doc):

		return { config_line['setting'].name: config_line['setting'].current_config_value for config_line in final_doc}


	def _generate_list_of_settings(self):
		'''
			Builds the library of Settings instances. These are used against each line in the 
			config.txt, with the first match being assigned as the Setting for that line.
		'''
		_settings = []

		for key, attributes in MASTER_SETTINGS.iteritems():

			typ = attributes['type']
			piClass = CLASS_LIBRARY[typ]
			setting = piClass(name=key)

			setting.set_stub(attributes['stub'])
			setting.set_default_value(attributes['default'])
			setting.set_valid_values(attributes['valid'])

			for x in attributes['patterns']:
				setting.add_pattern(x['id_pattern'], x['ext_pattern'])

			_settings.append(setting)

		return _settings


	def read_config_txt(self):
		'''
		Reads the config.txt found at the provided location and produces a list of config_lines.
		config_lines are dicts containing:
		- the original line from the config.txt
		- a cleaned up version of that line
		- the order the line is found in the config
		- a piSetting instance that has the retrieved validated value

		The final doc contains what will eventually be written to the new config.txt
		'''

		# first step is to use the Master_Settings information to create a list of piSetting instances
		_settings = self._generate_list_of_settings()

		with open(self.location, 'r') as f:
			dirty_doc = f.readlines()

		clean_doc = self._clean_this_doc( dirty_doc )

		clean_doc = self._assign_settings_to_doc( clean_doc, _settings )

		final_doc = self._append_unmatched_settings_to_doc(clean_doc, _settings)

		return final_doc


	def write_config_txt(self, final_doc, OpenWithBackup=None):
		''' Backs up the existing config.txt
		Runs through the final doc producing a list of lines to write back to a new config.txt
		'''

		new_lines = []

		for config_line in final_doc:
			setting = config_line['setting']

			# settings that are the default values, and where defaults are suppressed should be ignored
			# (i.e. dont write them to the new config.txt)
			if setting.isDefault and setting.suppress_defaults:
				continue

			# settings that are not changed should just have the original line replicated in the new config.txt
			if not setting.isChanged:
				new_lines.append(config_line['original'])

			# lines for which the values have changed should have the final_line brought in from the piSetting
			new_lines.append(setting.final_line)

		# reverse the lines back to the original order
		new_lines = new_lines[::-1]

		if self.OpenWithBackup:
			with self.OpenWithBackup(self.location, 'w') as f:
				f.writelines(new_lines)
		else:
			with open(self.location, 'w') as f:
				f.writelines(new_lines)


	def update_settings(self, final_doc, new_settings):

		for config_line in final_doc:
			
			setting = config_line['setting']

			setting.set_new_value( new_settings[ setting.name ] )

		return final_doc



if __name__ == "__main__":

	import sys
	from pprint import pprint

	sys.stdout = open('C:\\t\\logfile', 'w')

	c = ConfigFileInterface('samples\\config_05.txt')

	doc = c.read_config_txt()

	res = c.extract_settings_from_doc(doc)

	print '\n\n'

	pprint(res)
	print '\n\n'

	for x in doc:
		print x['clean']
		pprint(x['setting'].__dict__)
		print '\n'
