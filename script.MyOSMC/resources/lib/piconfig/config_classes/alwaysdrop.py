from baseClass import piSetting

class AlwaysDrop(piSetting):
    ''' Class assigned to lines that should always be dropped '''

    def _validate(self, *args, **kwargs):

        return None

    def convert_to_piconfig_setting(self, value):

        return self.default_value