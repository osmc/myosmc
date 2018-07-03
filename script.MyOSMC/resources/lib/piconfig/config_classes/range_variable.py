from range_value import RangeValue


def PiVersion():
    ''' Determines the version of Pi currently being used '''

    with open('/proc/cpuinfo', 'r') as f:

        cpu_count = sum([1 for x in f.readlines() if x.startswith('processor')])

    if cpu_count == 1:
        return 'PiB'
    else:
        return 'Pi2'


class RangeValue_VariableDefault(RangeValue):
    ''' Class for Pi Overclock settings where the defaults are dependent upon the
        version of PI
    '''

    def set_default_value(self, value):
        # the value provided in this case will be a dictionary of
        # versions and defaults

        try:
            version = PiVersion()
        except IOError:
            version = "PiB"

        if not version: version = "PiB"

        self.default_value = value[version]
        
    def _convert_to_piconfig_setting(self, value):

        return value