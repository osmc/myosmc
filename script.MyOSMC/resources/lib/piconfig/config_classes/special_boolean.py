from boolean import Boolean

class Boolean_specialValue(Boolean):
    ''' Class to handle settings that show up as booleans in Kodi,
        but have specific flags in the config.txt, rather than just 0 or 1.
        The flags should all be strings.
     '''
    
    def _validate(self, value):
        ''' Validation always returns None.

            if Validation fails, raise a ValueError.
        '''
        for vv in self.valid_values:
            if value == vv[0]:
                return None

        raise ValueError

    def _convert_to_kodi_setting(self, value):

        for vv in self.valid_values:
            if value == vv[0]:
                return 'true'

        return 'false'
            
    def _convert_to_piconfig_setting(self, value):

        if value == 'true':
            return self.valid_values[1][0]
        else:
            return 'NULLSETTING'