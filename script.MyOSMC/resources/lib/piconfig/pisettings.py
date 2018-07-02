import re

from mastersettings import MASTER_SETTING_PATTERNS

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

        # is_original indicates that the line is not one that's been touched by 
        # MyOSMC. All lines that are altered or added by the addon will be
        # appended with "#MyOSMC", with the original line added before it, commented
        # out, and with "#original" appended to the end.
        self.is_original = False

        # If the user adds '#lock' to the end of any config line, the values of that 
        # line will not be changed. The original line is returned in its place.
        self.is_locked = False

        self.valid_values = []

        # this list collects the identification and extraction patterns
        # these are used in a regex search on each line of the config.txt
        self.patterns = []


    def __repr__(self):

        if self.isChanged():
            return '{name} \n\t\t\t- default: {dflt}\n\t\t\t- current: {curr} \n\t\t\t- kodi repr: {krep} \n\t\t\t- is_locked: {lock} \n\t\t\t- is_original: {orig} \n\t\t\t- changed to: {newv}'.format(
                name=self.name, 
                dflt=self.default_value,
                curr=self.current_config_value, 
                krep=self._convert_to_kodi_setting(self.current_config_value),
                orig=self.is_original,
                lock=self.is_locked,
                newv=self.new_value)
        else:
            return '{name} \n\t\t\t- default: {dflt}\n\t\t\t- current: {curr} \n\t\t\t- kodi repr: {krep} \n\t\t\t- is_original: {orig} \n\t\t\t- is_locked: {lock} \n\t\t\t- no change'.format(
                name=self.name, 
                dflt=self.default_value,
                curr=self.current_config_value,
                krep=self._convert_to_kodi_setting(self.current_config_value),
                orig=self.is_original,
                lock=self.is_locked,)

    def isChanged(self):
        return  self.current_config_value == self.new_value

    def isDefault(self):
        return self.default_value == self.new_value

    def isOriginal(self, line):
        return '#MyOSMC' not in line

    def isLocked(self, line):
        return '#lock' in line

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

    def _construct_stub(self):

        if self.is_original:
            constructed_stub = '#%s #original\n%s #MyOSMC' % (self.original, self.stub)
        else:
            constructed_stub = '%s #MyOSMC' % self.stub

        return constructed_stub

    def final_line(self):

        if not self.is_locked:
            return self._construct_stub() % self.new_value

        return self.original

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
                    print 'Assigning as duplicate: %s' % config_line['original']
                    return Duplicate(duplicated_line=config_line['original'])

                value = self._extract_setting_value_from_line(clean_line, pattern_pair[1])
                if value is not None:
                    # a valid value has been found for this setting, set the original value to the one we found
                    # then break out of all the loops
                    self.foundinDoc = True
                    self.current_config_value = value

                    # Confirm that the line is original.
                    if self.isOriginal(config_line['original']):
                        self.is_original = True
                    
                    # Confirm that the line is locked (which blocks any changes)
                    if self.isLocked(config_line['original']):
                        self.is_locked = True

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

        # We don't want to double hash duplicated comment lines
        if duplicated_line.strip().startswith('#'):
            stub = '%s'
        else:
            stub = '#%s'

        self.stub, self.new_value = stub, duplicated_line

    def _validate(self, value):
        ''' Duplicates always pass validation. '''

        return value

class PassThrough(piSetting):
    ''' Class assigned to lines for which no Setting could be found.
    Those lines will simply be replicated, as is in the new config.txt.
     '''

    def isChanged(self):
        '''Settings for which the values have not changed will have the original
        line used in the new config.txt.    '''

        return False

    def _validate(self, value):
        ''' Passthroughs always pass validation. '''

        return value


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

        # Convert the value to an integer, if possible
        try:
            value = int(value)
        except ValueError:
            pass

        if value not in self.valid_values:
            raise ValueError
        else:
            return value

    def _convert_to_kodi_setting(self, value):

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
        The flags should all be strings.
     '''

    def _convert_to_kodi_setting(self, value):

        try:
            if value in self.valid_values:
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

        if not (self.valid_values[0] <= value < self.valid_values[1]):
            raise ValueError

        return value


    def _convert_to_kodi_setting(self, value):
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


    def _convert_to_kodi_setting(self, value):
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
                'bool'      : Boolean,
                'boolspec'  : Boolean_specialValue,
                'range'     : RangeValue,
                'range_var' : RangeValue_VariableDefault,
                'string'    : RawString,
                'selection' : Selection,
                'alwaysdrop': AlwaysDrop
                }


def SettingClassFactory():
    '''
        Builds the library of Settings instances. These are used against each line in the
        config.txt, with the first match being assigned as the Setting for that line.
    '''
    _setting_classes = []

    for key, attributes in MASTER_SETTING_PATTERNS.iteritems():

        typ = attributes['type']
        piclass = CLASS_LIBRARY[typ]
        setting = piclass(name=key)

        setting.set_stub(attributes['stub'])
        setting.set_default_value(attributes['default'])
        setting.set_valid_values(attributes['valid'])

        for pattern in attributes['patterns']:
            setting.add_pattern(pattern['id_pattern'], pattern['ext_pattern'])

        _setting_classes.append(setting)

    return _setting_classes

