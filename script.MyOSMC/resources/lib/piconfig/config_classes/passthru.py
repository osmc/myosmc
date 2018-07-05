from baseClass import piSetting

class PassThrough(piSetting):
    ''' Class assigned to lines for which no Setting could be found.
    Those lines will simply be replicated, as is in the new config.txt.
     '''

    def isChanged(self):
        '''Settings for which the values have not changed will have the original
        line used in the new config.txt.    '''

        return False

    def _validate(self, value):
        ''' Passthroughs always pass validation. '''

        return value

    def _convert_to_piconfig_setting(self, value):

        return value

    def construct_final_line(self):

        return self.original_line