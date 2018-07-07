
     
PiModels = {

    '0x2': {
        'Name': 'A+',
        'normal': {
            'arm_freq': 700,
            'core_freq': 400,
            'force_turbo': 0,
            'initial_turbo': 0,
            'over_voltage': 0,
            'over_voltage_sdram': 0,
            'sdram_freq': 400,
        },
    },
    '0x3': {
        'Name': 'B+',
        'normal': {
            'arm_freq': 700,
            'core_freq': 400,
            'force_turbo': 0,
            'initial_turbo': 0,
            'over_voltage': 0,
            'over_voltage_sdram': 0,
            'sdram_freq': 400,
        },
    },
    '0x4': {
        'Name': '2B',
        'medium': {
            'arm_freq': 1000,
            'core_freq': 500,
            'force_turbo': 0,
            'initial_turbo': 0,
            'over_voltage': 2,
            'over_voltage_sdram': 0,
            'sdram_freq': 500,
        },
        'normal': {
            'arm_freq': 900,
            'core_freq': 450,
            'force_turbo': 0,
            'initial_turbo': 0,
            'over_voltage': 0,
            'over_voltage_sdram': 0,
            'sdram_freq': 450,
        },
    },
# No infomation about these models. Probably test models?
# Since there is no normal profile defined, then these models
# cannot be overclocked.    
    '0x5': {'Name': 'Alpha'},
    '0x6': {'Name': 'CM1'},
    '0xa': {'Name': 'CM3'},
    '0x8': {
        'Name': '3B',
        'normal': {
            'arm_freq': 1200,
            'core_freq': 400,
            'force_turbo': 0,
            'initial_turbo': 0,
            'over_voltage': 0,
            'over_voltage_sdram': 0,
            'sdram_freq': 400,
        },
    },
# Do not allow custom OC for the Pi Zero/Zero W    
    '0x9': {'Name': 'Zero'},
    '0xc': {'Name': 'Zero W'},
    '0xd': {
        'Name': '3B+',
        'normal': {
            'arm_freq': 1400,
            'core_freq': 400,
            'force_turbo': 0,
            'initial_turbo': 0,
            'over_voltage': 0,
            'over_voltage_sdram': 0,
            'sdram_freq': 400,
        },
    },
    'legacy': {
        'Name': 'B',
        'higher': {
            'arm_freq': 950,
            'core_freq': 450,
            'force_turbo': 0,
            'initial_turbo': 0,
            'over_voltage': 6,
            'over_voltage_sdram': 0,
            'sdram_freq': 450,
        },
        'middle': {
            'arm_freq': 900,
            'core_freq': 375,
            'force_turbo': 0,
            'initial_turbo': 0,
            'over_voltage': 0,
            'over_voltage_sdram': 0,
            'sdram_freq': 400,
        },
        'normal': {
            'arm_freq': 850,
            'core_freq': 375,
            'force_turbo': 0,
            'initial_turbo': 0,
            'over_voltage': 0,
            'over_voltage_sdram': 0,
            'sdram_freq': 400,
        },
    },
}
