import re


class piSetting(object):

	def __init__(self, name):

		self.name = name
		
		# the stub is how the settings will be written to the config.txt
		self.stub = ''

		# this setting prevents the default value from being written to the config.txt
		# use case is where a boolean flag is False or 0 and the line is ignored by the Pi's
		# configuration parser
		self.suppress_defaults = False

		# This flag indicates whether the setting is found within the config.txt.
		# It is set during the first extraction of settings from the config.txt
		self.foundinDoc = False

		# default, original and new values are stored as the PI CONFIG representations
		self.default_value = 'NULLSETTING'
		self.current_config_value = 'NULLSETTING'
		self.new_value = None

		self.valid_values = []

		# this list collects the identification and extraction patterns
		# these are used in a regex search on each line of the config.txt
		self.patterns = []


	def __repr__(self):

		if self.isChanged():
			return '{name} - default: {dflt} - current: {curr} - changed to: {newv}'.format(
				name=self.name, dflt=self.default_value, curr=self.current_config_value, newv=self.new_value)
		else:
			return '{name} - default: {dflt} - current: {curr} - no change'.format(
				name=self.name, dflt=self.default_value, curr=self.current_config_value)

	def isChanged(self):
		return 	self.current_config_value == self.new_value

	def isDefault(self):
		return self.default_value == self.new_value

	def set_stub(self, value):
		self.stub = value

	def set_default_value(self, value):
		self.default_value = value

	def set_current_value_to_default(self):
		self.current_config_value = self.default_value 

	def set_valid_values(self, valid_values=None):
		if valid_values is None:
			valid_values = []
		self.valid_values = valid_values

	def add_pattern(self, id_pattern, ext_pattern):
		id_pattern = re.compile(id_pattern, re.IGNORECASE)
		ext_pattern = re.compile(ext_pattern, re.IGNORECASE)
		self.patterns.append((id_pattern, ext_pattern))

	def set_current_config_value(self, value):
		self.current_config_value = value

	def set_new_value(self, value):
		self.new_value = self.convert_to_piconfig_setting(value)

	def final_line(self):
		return self.stub % self.new_value

	def _validate(self, *args, **kwargs):
		''' Invalid values should raise a ValueError '''
		raise NotImplementedError

	def _convert_to_kodi_setting(self, *args, **kwargs):
		return NotImplementedError

	def _convert_to_piconfig_setting(self, *args, **kwargs):
		return NotImplementedError

	def _extract_setting_value_from_line(self, line, pattern, value = None):

		raw_values = re.search(pattern, line)
		if raw_values:
			try:
				raw_value = raw_values.group(1)
				value = self._validate(raw_value)
			except ValueError:
				print 'Line failed validation: \n{line}\nfailed value:{raw_value}'.format(line=line, raw_value=raw_value)
			except:
				print 'Line validation error: \n{line}'.format(line=line)
		return value

	def extract_setting_from_line(self, config_line, value = None):
		''' This method processes a clean_line to see if it contains the instances relevent setting.
		If the line does not contain a relevant setting or the value cannot be parsed from the line, then we return None.
		If a relevant setting is found and the value can be parsed, then that value is set as the current_config_value and
		the setting instance is returned so that it can be attached to the ConfigLine.
		'''
		# The Setting instance should only ever accept the first value it finds (running from bottom to top in the config.txt).
		# Any other subsequent matches should be considered duplicates.
		# Any duplicate setting should be commented out when written back to the config.txt.

		for pattern_pair in self.patterns:
			clean_line = config_line['clean']
			matched = re.search(pattern_pair[0], clean_line)

			if matched:
				if self.foundinDoc: 
					print 'Assigning as duplicate'
					return Duplicate(duplicated_line=config_line['original'])

				value = self._extract_setting_value_from_line(clean_line, pattern_pair[1])
				if value is not None:
					# a valid value has been found for this setting, set the original value to the one we found
					# then break out of all the loops
					self.foundinDoc = True
					self.current_config_value = value
					break

		if value is None:
			raise ValueError

		return self


class Duplicate(piSetting):
	''' Class that is assigned to lines in the config.txt that are determined to 
		be duplicates. These will be retained, but commented out in the new
		config.txt
	'''

	def __init__(self, duplicated_line):
		
		super(Duplicate, self).__init__(name='dupe')

		self.stub, self.new_value = '#%s', duplicated_line


class PassThrough(piSetting):
	''' Class assigned to lines for which no Setting could be found.
	Those lines will simply be replicated, as is in the new config.txt.
	 '''

	def isChanged(self):
		'''Settings for which the values have not changed will have the original
		line used in the new config.txt.	'''

		return False


class AlwaysDrop(piSetting):
	''' Class assigned to lines that should always be dropped '''

	def _validate(self, *args, **kwargs):

		return None

	def convert_to_piconfig_setting(self, value):

		return self.default_value


class Boolean(piSetting):
	''' Class similar to selection, but the only valid config.txt values are either 0 or 1.
		These are converted to 'false' and 'true' for consumption by Kodi.
	'''

	def _validate(self, value):

		if int(value) not in self.valid_values:
			raise ValueError
		else:
			return value

	def convert_to_kodi_setting(self, value):

		try:
			if int(value) == 1:
				return 'true'
			else:
				raise
		except:
			return 'NULLSETTING'


	def convert_to_piconfig_setting(self, value):

		if value == 'true':
			return '1'
		else:
			return 'NULLSETTING'


class Boolean_specialValue(Boolean):
	''' Class to handle settings that show up as booleans in Kodi, 
		but have specific flags in the config.txt, rather than just 0 or 1.
	 '''


	def convert_to_kodi_setting(self, value):

		try:
			if int(value) in self.valid_values:
				return 'true'
			else:
				raise
		except:
			return 'NULLSETTING'


	def convert_to_piconfig_setting(self, value):

		if value == 'true':
			return self.valid_values[0]
		else:
			return 'NULLSETTING'


class RangeValue(piSetting):
	''' Class for settings that are in a defined range of integers in the config.txt.
		The values are the same in the config.txt and Kodi.
	'''

	def _validate(self, value):

		# Convert the value into a number.
		# Value is likely to be integer, but float is safer.
		value = int(float(value))

		if not (self.valid_values[0] <= value <= self.valid_values[1]):
			raise ValueError

		return value


	def convert_to_kodi_setting(self, value):
		'''All Kodi values are strings'''

		return str(value)


class RangeValue_VariableDefault(RangeValue):
	''' Class for Pi Overclock settings where the defaults are dependent upon the 
		version of PI
	'''		

	def set_default_value(self, value):
		# the value provided in this case will be a dictionary of 
		# versions and defaults

		try:
			version = PiVersion()
		except IOError:
			version = "PiB"

		if not version: version = "PiB"

		self.default_value = value[version]


class RawString(piSetting):
	''' Class to handle strings that pass directly from the config.txt to Kodi,
		and back again. Such as codec serial numbers.
	'''

	def _validate(self, value):
		''' This could include length validation, but is not needed right now. '''

		return value


	def convert_to_kodi_setting(self, value):
		'''All Kodi values are strings'''

		return str(value)


class Selection(piSetting):
	''' Class to handle settings that are one of a given set of valid strings
		in the config.txt. These are matched to a validation list of tuples or the form
		(config.txt string, kodi-value)
		Validation takes the form of checking if the string can be found in the tuple[0] in its
		entirety. The value returned will be the first item in the validation list with the 
		kodi value in tuple[1]
	'''

	def _validate(self, value):

		for x in self.valid_values:
			if x[0] == value:
				return x[1]

		raise ValueError

	def convert_to_piconfig_setting(self, value):

		for x in self.valid_values:
			if int(value) == x[1]:
				return x[0]

		return self.default_value


	def _convert_to_kodi_setting(self, value):

		for config_string, kodi_value in self.valid_values:
			if value == config_string:
				return kodi_value


def PiVersion():
	''' Determines the version of Pi currently being used '''

	with open('/proc/cpuinfo', 'r') as f:

		cpu_count = sum([1 for x in f.readlines() if x.startswith('processor')])

	if cpu_count == 1:
		return 'PiB'
	else:
		return 'Pi2'




CLASS_LIBRARY = {
				'duplicate' : Duplicate,
				'passthru'  : PassThrough,
				'bool'		: Boolean,
				'boolspec'  : Boolean_specialValue,
				'range'		: RangeValue,
				'range_var'	: RangeValue_VariableDefault,
				'string'    : RawString,
				'selection' : Selection,
				'alwaysdrop': AlwaysDrop
				}


