from boolean import Boolean

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