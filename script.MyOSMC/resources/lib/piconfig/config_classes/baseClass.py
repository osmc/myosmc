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

    def set_suppress_ifDefault(self, value):
        self.suppress_defaults = value

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