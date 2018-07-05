from baseClass import piSetting

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
                return x[0]

        raise ValueError

    def _convert_to_piconfig_setting(self, value):

        for x in self.valid_values:
            if int(value) == x[1]:
                return x[0]

        return self.default_value

    def _convert_to_kodi_setting(self, value):

        for config_string, kodi_value in self.valid_values:
            if value == config_string:
                return kodi_value