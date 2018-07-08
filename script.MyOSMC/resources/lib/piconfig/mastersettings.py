
# SETTING TYPES

# "alwaysdrop": if line is matched, drop it,

# "bool"      : booleans are stored as 0 or 1 in the config, 
#                but "false" and "true" in kodi,

# "boolspec"  : this is a special type of boolean where the 
#               representation in the config is a string, but 
#               kodi will treat it as "true" if the string is 
#               present,

# "range"     : the data in the config can be anything within 
#               a range,

# "range_var" : it is a normal range, but the range differs 
#               depending on some external variable, like the 
#               Pi version,

# "selection" : the value in the config can be one of a set 
#               number of items, the ordinal position of the 
#               value in the set is passed to kodi,

# "string"    : this is just a string that gets passed to 
#               kodi as is, like the codec serials


MASTER_SETTING_PATTERNS =    {

        "start_x": {
            "type"      : "bool",
            "default"   : 1,
            "sprssDef"  : False,
            "stub"      : "start_x=%s",
            "valid"     : [0,1],
            "patterns": [{  "id_pattern"      : r"\s*start_x\s*=",
                            "ext_pattern"     : r"\s*start_x\s*=\s*(\d)",}
                            ],
        },

        "gpu_mem_1024": {
            "type"      : "range",
            "default"   : "256",
            "sprssDef"  : True,
            "stub"      : "gpu_mem_1024=%s",
            "valid"     : [16, 321],
            "patterns": [{  "id_pattern"      : r"\s*gpu_mem_1024\s*=",
                            "ext_pattern"     : r"\s*gpu_mem_1024\s*=\s*(\d+)"},
                        {   "id_pattern"      : r"\s*gpu_mem\s*=",
                            "ext_pattern"     : r"\s*gpu_mem\s*=\s*(\d+)"},
                            ],
        },

        "gpu_mem_512": {
            "type"      : "range",
            "default"   : "144",
            "sprssDef"  : True,
            "stub"      : "gpu_mem_512=%s",
            "valid"     : [16,257],
            "patterns": [{  "id_pattern"      : r"\s*gpu_mem_512\s*=",
                            "ext_pattern"     : r"\s*gpu_mem_512\s*=\s*(\d+)"},
                        {   "id_pattern"      : r"\s*gpu_mem\s*=",
                            "ext_pattern"     : r"\s*gpu_mem\s*=\s*(\d+)"},
                            ],
        },

        "gpu_mem_256": {
            "type"      : "range",
            "default"   : "112",
            "sprssDef"  : True,
            "stub"      : "gpu_mem_256=%s",
            "valid"     : [16,193],
            "patterns": [{  "id_pattern"      : r"\s*gpu_mem_256\s*=",
                            "ext_pattern"     : r"\s*gpu_mem_256\s*=\s*(\d+)"   },
                        {   "id_pattern"      : r"\s*gpu_mem\s*=",
                            "ext_pattern"     : r"\s*gpu_mem\s*=\s*(\d+)"},
                            ],
        },

        "config_hdmi_boost": {
            "type"      : "range",
            "default"   : "",
            "sprssDef"  : True,
            "stub"      : "config_hdmi_boost=%s",
            "valid"     : [1,12],
            "patterns": [{  "id_pattern"      : r"\s*(?:hdmi_boost|config_hdmi_boost)\s*=",
                            "ext_pattern"     : r"\s*(?:hdmi_boost|config_hdmi_boost)\s*=\s*(\d*)",}
                            ],
        },

        "decode_MPG2": {
            "type"      : "string",
            "default"   : "",
            "sprssDef"  : True,
            "stub"      : "decode_MPG2=%s",
            "valid"     : [],
            "patterns": [{  "id_pattern"      : r"\s*decode_MPG2\s*=\s*",
                            "ext_pattern"     : r"\s*decode_MPG2\s*=\s*(\w+)",}
                            ],
        },

        "decode_WVC1": {
            "type"      : "string",
            "default"   : "",
            "sprssDef"  : True,
            "stub"      : "decode_WVC1=%s",
            "valid"     : [],
            "patterns": [{  "id_pattern"      : r"\s*decode_WVC1\s*=\s*",
                            "ext_pattern"     : r"\s*decode_WVC1\s*=\s*(\w+)",}
                            ],
        },

        "display_rotate": {
            "type"      : "selection",
            "default"   : "0",
            "sprssDef"  : True,
            "stub"      : "display_rotate=%s",
            "valid"     : [
                            ("off",     0),
                            ("1",       1),
                            ("2",       2),
                            ("3",       3),
                            ("0x10000", 4),
                            ("0x20000", 5),
                            ],
            "patterns": [{  "id_pattern"      : r"\s*display_rotate\s*=\s*",
                            "ext_pattern"     : r"\s*display_rotate\s*=\s*(\w+)",}
                            ],
        },

        "hdmi_force_hotplug": {
            "type"      : "bool",
            "default"   : 0,
            "sprssDef"  : True,
            "stub"      : "hdmi_force_hotplug=%s",
            "valid"     : [0,1],
            "patterns": [{  "id_pattern"      : r"\s*hdmi_force_hotplug\s*=",
                            "ext_pattern"     : r"\s*hdmi_force_hotplug\s*=\s*(\d+)",}
                            ],
        },

        "hdmi_edid_file": {
            "type"      : "bool",
            "default"   : 0,
            "sprssDef"  : True,
            "stub"      : "hdmi_edid_file=%s",
            "valid"     : [0,1],
            "patterns": [{  "id_pattern"      : r"\s*hdmi_edid_file\s*=",
                            "ext_pattern"     : r"\s*hdmi_edid_file\s*=\s*(\d+)",}
                            ],
        },

        "hdmi_group": {
            "type"      : "range",
            "default"   : "0",
            "sprssDef"  : True,
            "stub"      : "hdmi_group=%s",
            "valid"     : [0, 3],
            "patterns": [{  "id_pattern"      : r"\s*hdmi_group\s*=",
                            "ext_pattern"     : r"\s*hdmi_group\s*=\s*(\d+)",}
                            ],
        },

        "hdmi_ignore_cec": {
            "type"      : "bool",
            "default"   : 0,
            "sprssDef"  : True,
            "stub"      : "hdmi_ignore_cec=%s",
            "valid"     : [0,1],
            "patterns": [{  "id_pattern"      : r"\s*hdmi_ignore_cec\s*=",
                            "ext_pattern"     : r"\s*hdmi_ignore_cec\s*=\s*(\d+)",}
                            ],
        },

        "hdmi_ignore_cec_init": {
            "type"      : "bool",
            "default"   : 0,
            "sprssDef"  : True,
            "stub"      : "hdmi_ignore_cec_init=%s",
            "valid"     : [0,1],
            "patterns": [{  "id_pattern"      : r"\s*hdmi_ignore_cec_init\s*=",
                            "ext_pattern"     : r"\s*hdmi_ignore_cec_init\s*=\s*(\d+)",}
                            ],
        },

        "hdmi_ignore_edid": {
            "type"      : "boolspec",
            "default"   : "off",
            "sprssDef"  : True,
            "stub"      : "hdmi_ignore_edid=%s",
            "valid"     : [
                            ("off", "false"),
                            ("0xa5000080", "true")
                            ],
            "patterns": [{  "id_pattern"      : r"\s*hdmi_ignore_edid\s*=",
                            "ext_pattern"     : r"\s*hdmi_ignore_edid\s*=\s*(\w+)",}
                            ],
        },

        "hdmi_mode": {
            "type"      : "range",
            "default"   : "0",
            "sprssDef"  : True,
            "stub"      : "hdmi_mode=%s",
            "valid"     : [1,87],
            "patterns": [{  "id_pattern"      : r"\s*hdmi_mode\s*=",
                            "ext_pattern"     : r"\s*hdmi_mode\s*=\s*(\d+)",}
                            ],
        },

        "hdmi_pixel_encoding": {
            "type"      : "range",
            "default"   : "0",
            "sprssDef"  : True,
            "stub"      : "hdmi_pixel_encoding=%s",
            "valid"     : [0,5],
            "patterns": [{  "id_pattern"      : r"\s*hdmi_pixel_encoding\s*=",
                            "ext_pattern"     : r"\s*hdmi_pixel_encoding\s*=\s*(\d+)",}
                            ],
        },

        "sdtv_aspect": {
            "type"      : "range",
            "default"   : "1",
            "sprssDef"  : True,
            "stub"      : "sdtv_aspect=%s",
            "valid"     : [1,4],
            "patterns": [{  "id_pattern"      : r"\s*sdtv_aspect\s*=",
                            "ext_pattern"     : r"\s*sdtv_aspect\s*=\s*(\d+)",}
                            ],
        },

        "sdtv_mode": {
            "type"      : "range",
            "default"   : "0",
            "sprssDef"  : True,
            "stub"      : "sdtv_mode=%s",
            "valid"     : [0,4],
            "patterns": [{  "id_pattern"      : r"\s*sdtv_mode\s*=",
                            "ext_pattern"     : r"\s*sdtv_mode\s*=\s*(\d+)",}
                            ],
        },

        "hdmi_safe": {
            "type"      : "bool",
            "default"   : "false",
            "sprssDef"  : True,
            "stub"      : "hdmi_safe=%s",
            "valid"     : [0,1],
            "patterns": [{  "id_pattern"      : r"\s*hdmi_safe\s*=",
                            "ext_pattern"     : r"\s*hdmi_safe\s*=\s*(\d+)",}
                            ],
        },


        "spi-bcm2835-overlay": {
            "type"      : "boolspec",
            "default"   : "off",
            "sprssDef"  : True,
            "stub"      : "dtoverlay=%s",
            "valid"     : [
                            ("off", "false"),
                            ("spi-bcm2835-overlay", "true")
                                ],
            "patterns": [{  "id_pattern"      : r"\s*(?:dtoverlay|device_tree_overlay)\s*=\s*[-\w\d]*spi-bcm2835[-\w\d]*",
                            "ext_pattern"     : r"\s*(?:dtoverlay|device_tree_overlay)\s*=\s*([-\w\d]*spi-bcm2835[-\w\d]*)",}
                            ],
        },

        "audio":{
            "type"      : "alwaysdrop",
            "default"   : 0,
            "sprssDef"  : True,
            "stub"      : "dtparam=audio=%s",
            "valid"     : [],
            "patterns": [{  "id_pattern"    : r"\s*(?:dtparam|dtparams|device_tree_param|device_tree_params)\s*=.*audio\s*=",
                            "ext_pattern"   : r"\s*(?:dtparam|dtparams|device_tree_param|device_tree_params)\s*=.*audio\s*=\s*(\w+)",}
                                ],
        },

        "w1gpio": {
            "type"      : "selection",
            "default"   : "off",
            "sprssDef"  : True,
            "stub"      : "dtoverlay=%s",
            "valid"     : [
                            # config value              KODI value
                            ("off"                      , 0),
                            ("w1-gpio-overlay"          , 1),
                            ("w1-gpio-pullup-overlay"   , 2)
                            ],
            "patterns": [{  "id_pattern"      : r"\s*(?:dtoverlay|device_tree_overlay)\s*=.*w1-gpio",
                            "ext_pattern"     : r"\s*(?:dtoverlay|device_tree_overlay)\s*=\s*([-\w\d]*w1-gpio[-\w\d]*)",}
                            ],
        },

        "soundcard_dac": {
            "type"      : "selection",
            "default"   : "off",
            "sprssDef"  : True,
            "stub"      : "dtoverlay=%s",
            "valid"     : [
                            ("off"                                                      , 0),

                            # string to write back to the config.txt
                            ("hifiberry-dac-overlay\ndtparam=audio=off"                 , 1 ),
                            ("hifiberry-dacplus-overlay\ndtparam=audio=off"             , 2 ),
                            ("hifiberry-digi-overlay\ndtparam=audio=off"                , 3 ),
                            ("iqaudio-dac-overlay,unmute_amp\ndtparam=audio=off"        , 4 ),
                            ("iqaudio-dacplus-overlay,unmute_amp\ndtparam=audio=off"    , 5 ),

                            # config.txt string                     # KODI value
                            ("hifiberry-dac-overlay"                , 1 ),
                            ("hifiberry-dac"                        , 1 ),
                            ("hifiberry-dacplus-overlay"            , 2 ),
                            ("hifiberry-dacplus"                    , 2 ),
                            ("hifiberry-digi-overlay"               , 3 ),
                            ("hifiberry-digi"                       , 3 ),
                            ("iqaudio-dac-overlay,unmute_amp"       , 4 ),
                            ("iqaudio-dac-overlay"                  , 4 ),
                            ("iqaudio-dac"                          , 4 ),
                            ("iqaudio-dac,unmute_amp"               , 4 ),
                            ("iqaudio-dacplus-overlay,unmute_amp"   , 5 ),
                            ("iqaudio-dacplus-overlay"              , 5 ),
                            ("iqaudio-dacplus,unmute_amp"           , 5 ),
                            ("iqaudio-dacplus"                      , 5 ),
                        ],
            "patterns": [{  "id_pattern"      : r"\s*(?:dtoverlay|device_tree_overlay)\s*=\s*[-\w\d]*(?:hifiberry-d|iqaudio-d)",
                            "ext_pattern"     : r"\s*(?:dtoverlay|device_tree_overlay)\s*=\s*([-\w\d]*(?:hifiberry-d|iqaudio-d)[-\w\d]*)",}
                            ],
        },

        "lirc-rpi-overlay": {
            "type"      : "boolspec",
            "default"   : "off",
            "sprssDef"  : True,
            "stub"      : "dtoverlay=%s",
            "valid"     : [
                            ("off", "false"),
                            ("lirc-rpi-overlay", "true"),
                            ("lirc-rpi", "true")
                            ],
            "patterns": [{  "id_pattern"      : r"\s*(?:dtoverlay|device_tree_overlay)\s*=\s*[-\w\d]*lirc-rpi[-\w\d]*",
                            "ext_pattern"     : r"\s*(?:dtoverlay|device_tree_overlay)\s*=\s*([-\w\d]*lirc-rpi[-\w\d]*)",}
                            ],
        },

        "gpio_in_pin": {
            "type"      : "range",
            "default"   : "18",
            "sprssDef"  : True,
            "stub"      : "dtparam=gpio_in_pin=%s",
            "valid"     : [1,26],
            "patterns": [{  "id_pattern"      : r"\s*(?:dtoverlay|device_tree_overlay|dtparam|dtparams|device_tree_param|device_tree_params)\s*=(?:lirc-rpi:)?.*gpio_in_pin[-\w\d]*=",
                            "ext_pattern"     : r"\s*(?:dtoverlay|device_tree_overlay|dtparam|dtparams|device_tree_param|device_tree_params)\s*=(?:lirc-rpi:)?.*gpio_in_pin[-\w\d]*=\s*(\w*)",}
                            ],
        },

        "gpio_in_pull": {
            "type"      : "selection",
            "default"   : "off",
            "sprssDef"  : True,
            "stub"      : "dtparam=gpio_in_pull=%s",
            "valid"     : [
                            ("off", 0),
                            ("down", 1),
                            ("up", 2),
                            ],
            "patterns": [{  "id_pattern"      : r"\s*(?:dtoverlay|device_tree_overlay|dtparam|dtparams|device_tree_param|device_tree_params)\s*=(?:lirc-rpi:)?.*gpio_in_pull[-\w\d]*=",
                            "ext_pattern"     : r"\s*(?:dtoverlay|device_tree_overlay|dtparam|dtparams|device_tree_param|device_tree_params)\s*=(?:lirc-rpi:)?.*gpio_in_pull[-\w\d]*=\s*(\w*)",}
                            ],
        },

        "gpio_out_pin": {
            "type"      : "range",
            "default"   : "17",
            "sprssDef"  : True,
            "stub"      : "dtparam=gpio_out_pin=%s",
            "valid"     : [1,26],
            "patterns": [{  "id_pattern"      : r"\s*(?:dtoverlay|device_tree_overlay|dtparam|dtparams|device_tree_param|device_tree_params)\s*=(?:lirc-rpi:)?.*gpio_out_pin[-\w\d]*=",
                            "ext_pattern"     : r"\s*(?:dtoverlay|device_tree_overlay|dtparam|dtparams|device_tree_param|device_tree_params)\s*=(?:lirc-rpi:)?.*gpio_out_pin[-\w\d]*=\s*(\w*)",}
                            ],
        },


        "arm_freq": {
            "type"      : "range_var",
            "default"   : "NULLSETTING",
            "sprssDef"  : True,
            "stub"      : "arm_freq=%s",
            "valid"     : [600, 1201],
            "patterns": [{  "id_pattern"      : r"\s*arm_freq\s*=\s*",
                            "ext_pattern"     : r"\s*arm_freq\s*=\s*(\d+)",}
                            ],
        },

        "sdram_freq": {
            "type"      : "range_var",
            "default"   : "NULLSETTING",
            "sprssDef"  : True,
            "stub"      : "sdram_freq=%s",
            "valid"     : [300, 701],
            "patterns": [{  "id_pattern"      : r"\s*sdram_freq\s*=\s*",
                            "ext_pattern"     : r"\s*sdram_freq\s*=\s*(\d+)",}
                            ],
        },

        "core_freq": {
            "type"      : "range_var",
            "default"   : "NULLSETTING",
            "sprssDef"  : True,
            "stub"      : "core_freq=%s",
            "valid"     : [150, 651],
            "patterns": [{  "id_pattern"      : r"\s*core_freq\s*=\s*",
                            "ext_pattern"     : r"\s*core_freq\s*=\s*(\d+)",}
                            ],
        },

        "initial_turbo": {
            "type"      : "range",
            "default"   : "0",
            "sprssDef"  : True,
            "stub"      : "initial_turbo=%s",
            "valid"     : [0, 61],
            "patterns": [{  "id_pattern"      : r"\s*initial_turbo\s*=\s*",
                            "ext_pattern"     : r"\s*initial_turbo\s*=\s*(\d+)",}
                            ],
        },

        "over_voltage": {
            "type"      : "range",
            "default"   : "0",
            "sprssDef"  : True,
            "stub"      : "over_voltage=%s",
            "valid"     : [0,9],
            "patterns": [{  "id_pattern"      : r"\s*over_voltage\s*=\s*",
                            "ext_pattern"     : r"\s*over_voltage\s*=\s*(\d+)",}
                            ],
        },

        "over_voltage_sdram": {
            "type"      : "range",
            "default"   : "0",
            "sprssDef"  : True,
            "stub"      : "over_voltage_sdram=%s",
            "valid"     : [0,9],
            "patterns": [{  "id_pattern"      : r"\s*over_voltage_sdram\s*=\s*",
                            "ext_pattern"     : r"\s*over_voltage_sdram\s*=\s*(\d+)",}
                            ],
        },

        "force_turbo": {
            "type"      : "bool",
            "default"   : 0,
            "sprssDef"  : True,
            "stub"      : "force_turbo=%s",
            "valid"     : [0,1],
            "patterns": [{  "id_pattern"      : r"\s*force_turbo\s*=\s*",
                            "ext_pattern"     : r"\s*force_turbo\s*=\s*(\d+)",}
                            ],
        },

    }

if __name__ == "__main__":

    # from pprintpp import pprint

    # pprint(MASTER_SETTING_PATTERNS)
    
    for k, v in MASTER_SETTING_PATTERNS.items():
        try:
            print v["stub"] % v["valid"][0]
        except:
            print "Error %s" % k
