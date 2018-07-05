from common import Logger
import re


class piSetting(Logger):

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

        # saved_original_line indicates that the line contains an inline comment that
        # begins with '#origional:' which indicates the the original line in the config
        # has been replaced by MyOSMC with the original line saved in an inline comment.
        self.saved_original_line = False

        # If the user adds '#lock' to the end of any config line, the values of that 
        # line will not be changed. The original line is returned in its place.
        self.is_locked = False

        self.valid_values = []

        # this list collects the identification and extraction patterns
        # these are used in a regex search on each line of the config.txt
        self.patterns = []

        self.original_line = ''
        self.inline_comment = ''


    def __repr__(self):

        if self.isChanged():
            return '{name} \n\t\t\t- default: {dflt}\n\t\t\t- current: {curr} \n\t\t\t- kodi repr: {krep} \n\t\t\t- is_locked: {lock} \n\t\t\t- changed to: {newv}'.format(
                name=self.name, 
                dflt=self.default_value,
                curr=self.current_config_value, 
                krep=self._convert_to_kodi_setting(self.current_config_value),
                lock=self.is_locked,
                newv=self.new_value)
        else:
            return '{name} \n\t\t\t- default: {dflt}\n\t\t\t- current: {curr} \n\t\t\t- kodi repr: {krep} \n\t\t\t- is_locked: {lock} \n\t\t\t- no change'.format(
                name=self.name, 
                dflt=self.default_value,
                curr=self.current_config_value,
                krep=self._convert_to_kodi_setting(self.current_config_value),
                lock=self.is_locked,)

    def isChanged(self):

        # self.log('%s: %s vs %s changed=%s' % (self.name, self.current_config_value, self.new_value, self.current_config_value != self.new_value))
        return self.current_config_value != self.new_value

    def isDefault(self):
        return self.default_value == self.new_value

    def set_stub(self, value):
        self.stub = value

    def set_default_value(self, value):
        self.default_value = value

    def set_original_line(self, value):
        self.original_line = value

    def set_inline_comment(self, value):
        self.inline_comment = value

        # If there is an inline comment, confirm whether it is an original line that has
        # been saved/replaced by MyOSMC.
        if self.inline_comment:
            if '#original:' in self.inline_comment:
                self.saved_original_line = True

            # Confirms whether the line is locked (which blocks any settings changes)
            # by MyOSMC.
            if ('#lock' in self.inline_comment) or ('#locked' in self.inline_comment):
                self.is_locked = True

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
        # self.log(self.name)
        self.new_value = self._convert_to_piconfig_setting(value)

    def _construct_stub(self):

        # If there is an original saved line, then append that to the normal stub.
        # We don't want to always be adding originals.
        if self.saved_original_line:
            self.log(self.inline_comment)
            return '%s %s\n' % (self.stub, self.inline_comment.rstrip())

        # If there isn't a saved original line, then we are free to take the full
        # original line (which includes any inline comments) and save it as an
        # inline comment prepended with '#original':. Next time, this line will be
        # picked up as a saved_original_line
        return '%s #original:%s \n' % (
                                    self.stub, 
                                    self.original_line.rstrip()
                                    )

    def construct_final_line(self):

        # self.log(self.name)

        # If the setting is locked (i.e. the line has an inline comment starting #lock)
        # then simply return the original line as it is, with no changes.
        if self.is_locked:
            # self.log('isLocked\n')
            return self.original_line

        # Settings that are the default values, and where defaults are set to be suppressed 
        # and that were not found in the originl config.txt should be ignored
        # (i.e. dont write them to the new config.txt)
        if self.isDefault() and self.suppress_defaults and not self.foundinDoc:
            # self.log('isDefault, not found in doc\n')
            return 'NULLSETTING'

        # Settings that are not changed but that were found in the original document
        # should just have the original line replicated in the new config.txt.
        # This will, hopefully, allow dtoverlays to remain in the format that the user prefers.
        if not self.isChanged() and self.foundinDoc:
            # self.log('notChanged, found in doc\n')
            return self.original_line

        # Otherwise we construct the stub, and insert the new_value into it.
        # self.log('constructing line\n')
        return self._construct_stub() % self.new_value

    def _validate(self, *args, **kwargs):
        ''' Invalid values should raise a ValueError '''
        raise NotImplementedError

    def _convert_to_kodi_setting(self, *args, **kwargs):
        return 'NULLSETTING'

    def _convert_to_piconfig_setting(self, *args, **kwargs):
        return NotImplementedError

    def _extract_setting_value_from_line(self, line, pattern, value = None):

        raw_values = re.search(pattern, line)
        if raw_values:
            try:
                raw_value = raw_values.group(1)
                value = self._validate(raw_value)
            except ValueError:
                self.log('Line failed validation: \n{line}\nfailed value:{raw_value}'.format(line=line, raw_value=raw_value))

                # Use the default value instead
                self.log('Using default value: %s' % self.default_value)
                value = self.default_value
            except:
                self.log('Line validation error: \n{line}'.format(line=line))
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
                    self.log('Assigning as duplicate: %s' % config_line['original'])
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

        # We don't want to double hash duplicated comment lines
        if duplicated_line.strip().startswith('#'):
            stub = '%s'
        else:
            stub = '#%s'

        self.stub, self.new_value = stub, duplicated_line

    def _validate(self, value):
        ''' Duplicates always pass validation. '''

        return value

    def construct_final_line(self):

        return self.stub % self.original_line