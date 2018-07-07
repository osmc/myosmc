
import env
from common import hardware
from piconfig import pimodels
from range_value import RangeValue


class RangeValue_VariableDefault(RangeValue):
    ''' Class for Pi Overclock settings where the defaults are dependent upon the
        version of Pi
    '''

    def set_default_value(self, value):

        normal_defaults = hardware.get_Pi_clock_settings(pimodels.PiModels)['normal']

        key = self.stub[:self.stub.index('=')]

        self.default_value = normal_defaults[key]
        
    def _convert_to_piconfig_setting(self, value):

        return value