from baseClass import piSetting

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

    def _convert_to_piconfig_setting(self, value):

        return value