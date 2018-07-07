from baseClass import piSetting

class RangeValue(piSetting):
    ''' Class for settings that are in a defined range of integers in the config.txt.
        The values are the same in the config.txt and Kodi.
    '''

    def _validate(self, value):
        ''' Validation always returns None.

            if Validation fails, raise a ValueError.
        '''
        # Convert the value into a number.
        # Value is likely to be integer, but float is safer.
        value = int(float(value))

        if any([(self.valid_values[0] > value), (value > self.valid_values[1])]):
            raise ValueError

        return None


    def _convert_to_kodi_setting(self, value):
        '''All Kodi values are strings'''

        return str(value)
        
    def _convert_to_piconfig_setting(self, value):

        return value