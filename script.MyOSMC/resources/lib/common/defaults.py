# This dictionary contains all the default values used by the MyOSMC addon.
# Other modules should only ever retrieve default values from here.
#
# Example usage:
#
# from defaults import DEFAULT_DICT
# from dbinterface import DBInterface
#
# db = DBInterface()
# try:
#     setting = db.getsetting('unknownKey')
# except KeyError:
#     setting = DEFAULT_DICT.get('unknownKey', None)


DEFAULT_DICT = {

    # This is a basic key-value pair.
    'a': 'standard value',

    # Values can themselves be dictionaries, but we'd prefer to have unique values
    # in the first layer.
    'b': {
        'sub_setting': 'sub_value'
    },

    # The preferred use of sub-dicts is to overwrite the main values;
    # i.e. to accomodate hardware specific values.
    # This example shows how the 'standard value', can be replaced with the
    # special rPi3 value:
    #     >>> from defaults import DEFAULT_DICT
    #     >>> DEFAULT_DICT.update( DEFAULT_DICT.get(common.getHardwareID(), {} )
    'rPi3': {
        'a': 'rPi3 special value'
    },
}
