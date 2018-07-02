from baseClass import piSetting

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