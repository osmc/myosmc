from baseClass import Duplicate
from passthru import PassThrough
from boolean import Boolean
from special_boolean import Boolean_specialValue
from range_value import RangeValue
from range_variable import RangeValue_VariableDefault
from raw_string import RawString
from selection import Selection
from alwaysdrop import AlwaysDrop


CLASS_LIBRARY = {
                'duplicate' : Duplicate,
                'passthru'  : PassThrough,
                'bool'      : Boolean,
                'boolspec'  : Boolean_specialValue,
                'range'     : RangeValue,
                'range_var' : RangeValue_VariableDefault,
                'string'    : RawString,
                'selection' : Selection,
                'alwaysdrop': AlwaysDrop
                }