from baseClass import piSetting

class AlwaysDrop(piSetting):
    ''' Class assigned to lines that should always be dropped '''

    def _validate(self, *args, **kwargs):
        ''' Validation always returns None.

            if Validation fails, raise a ValueError.
        '''

        return None

    def _convert_to_piconfig_setting(self, value):

        return self.default_value