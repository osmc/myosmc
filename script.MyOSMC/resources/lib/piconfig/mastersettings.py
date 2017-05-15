
MASTER_SETTINGS =    {

		"start_x": {
			"type" 		: "bool",
			"default"   : "1",
			"sprssDef"  : False,
			"stub"      : "start_x=%s",
			"valid"		: [0,1],
			"patterns": [{	"id_pattern"      : r"\s*start_x\s*=",
							"ext_pattern"     : r"\s*start_x\s*=\s*(\d)",}
							],
		},

		"gpu_mem_1024": { 
			"type" 		: "range",
			"default"   : "256",
			"sprssDef"  : True,
			"stub"      : "gpu_mem_1024=%s",
			"valid"		: [16, 321],
			"patterns": [{  "id_pattern"      : r"\s*gpu_mem_1024\s*=",
							"ext_pattern"     : r"\s*gpu_mem_1024\s*=\s*(\d+)"},
						{	"id_pattern"      : r"\s*gpu_mem\s*=",
							"ext_pattern"     : r"\s*gpu_mem\s*=\s*(\d+)"},				
							],
		},

		"gpu_mem_512": { 
			"type" 		: "range",
			"default"   : "144",
			"sprssDef"  : True,
			"stub"      : "gpu_mem_512=%s",
			"valid"		: [16,257],
			"patterns": [{	"id_pattern"      : r"\s*gpu_mem_512\s*=",
							"ext_pattern"     : r"\s*gpu_mem_512\s*=\s*(\d+)"},
						{	"id_pattern"      : r"\s*gpu_mem\s*=",
							"ext_pattern"     : r"\s*gpu_mem\s*=\s*(\d+)"},				
							],
		},

		"gpu_mem_256": { 
			"type" 		: "range",
			"default"   : "112",
			"sprssDef"  : True,
			"stub"      : "gpu_mem_256=%s",
			"valid"		: [16,193],
			"patterns": [{	"id_pattern"      : r"\s*gpu_mem_256\s*=",
							"ext_pattern"     : r"\s*gpu_mem_256\s*=\s*(\d+)"	},
						{   "id_pattern"      : r"\s*gpu_mem\s*=",
							"ext_pattern"     : r"\s*gpu_mem\s*=\s*(\d+)"},				
							],
		},

		"config_hdmi_boost": { 
			"type" 		: "range",
			"default"   : "",
			"sprssDef"  : True,
			"stub"      : "config_hdmi_boost=%s",
			"valid"		: [1,12],
			"patterns": [{	"id_pattern"      : r"\s*(?:hdmi_boost|config_hdmi_boost)\s*=",
							"ext_pattern"     : r"\s*(?:hdmi_boost|config_hdmi_boost)\s*=\s*(\d*)",}
							],
		},
	
		"decode_MPG2": { 
			"type" 		: "string",
			"default"   : "",
			"sprssDef"  : True,
			"stub"      : "decode_MPG2=%s",
			"valid"		: [],
			"patterns": [{	"id_pattern"      : r"\s*decode_MPG2\s*=\s*",
							"ext_pattern"     : r"\s*decode_MPG2\s*=\s*(\w+)",}
							],
		},

		"decode_WVC1": { 
			"type" 		: "string",
			"default"   : "",
			"sprssDef"  : True,
			"stub"      : "decode_WVC1=%s",
			"valid"		: [],
			"patterns": [{	"id_pattern"      : r"\s*decode_WVC1\s*=\s*",
							"ext_pattern"     : r"\s*decode_WVC1\s*=\s*(\w+)",}
							],
		},

		"display_rotate": { 
			"type" 		: "selection",
			"default"   : "0",
			"sprssDef"  : True,
			"stub"      : "display_rotate=%s",
			"valid"		: [	
							('1', 		1),
							('2', 		2),
							('3', 		3),
							('0x10000', 4),
							('0x20000',	5),
							],
			"patterns": [{	"id_pattern"      : r"\s*display_rotate\s*=\s*",
							"ext_pattern"     : r"\s*display_rotate\s*=\s*(\w+)",}
							],
		},

		"hdmi_force_hotplug": { 
			"type" 		: "bool",
			"default"   : "false",
			"sprssDef"  : True,
			"stub"      : "hdmi_force_hotplug=%s",
			"valid"		: [0,1],
			"patterns": [{	"id_pattern"      : r"\s*hdmi_force_hotplug\s*=",
							"ext_pattern"     : r"\s*hdmi_force_hotplug\s*=\s*(\d+)",}
							],
		},

		"hdmi_edid_file": { 
			"type" 		: "bool",
			"default"   : "false",
			"sprssDef"  : True,
			"stub"      : "hdmi_edid_file=%s",
			"valid"		: [0,1],
			"patterns": [{	"id_pattern"      : r"\s*hdmi_edid_file\s*=",
							"ext_pattern"     : r"\s*hdmi_edid_file\s*=\s*(\d+)",}
							],
		},

		"hdmi_group": { 
			"type" 		: "range",
			"default"   : "0",
			"sprssDef"  : True,
			"stub"      : "hdmi_group=%s",
			"valid"		: [0, 3],
			"patterns": [{	"id_pattern"      : r"\s*hdmi_group\s*=",
							"ext_pattern"     : r"\s*hdmi_group\s*=\s*(\d+)",}
							],
		},

		"hdmi_ignore_cec": { 
			"type" 		: "bool",
			"default"   : "false",
			"sprssDef"  : True,
			"stub"      : "hdmi_ignore_cec=%s",
			"valid"		: [0,1],
			"patterns": [{	"id_pattern"      : r"\s*hdmi_ignore_cec\s*=",
							"ext_pattern"     : r"\s*hdmi_ignore_cec\s*=\s*(\d+)",}
							],
		},

		"hdmi_ignore_cec_init": { 
			"type" 		: "bool",
			"default"   : "false",
			"sprssDef"  : True,
			"stub"      : "hdmi_ignore_cec_init=%s",
			"valid"		: [0,1],
			"patterns": [{	"id_pattern"      : r"\s*hdmi_ignore_cec_init\s*=",
							"ext_pattern"     : r"\s*hdmi_ignore_cec_init\s*=\s*(\d+)",}
							],
		},

		"hdmi_ignore_edid": { 
			"type" 		: "boolspec",
			"default"   : "false",
			"sprssDef"  : True,
			"stub"      : "hdmi_ignore_edid=%s",
			"valid"		: ['0xa5000080'],
			"patterns": [{	"id_pattern"      : r"\s*hdmi_ignore_edid\s*=",
							"ext_pattern"     : r"\s*hdmi_ignore_edid\s*=\s*(\w+)",}
							],
		},

		"hdmi_mode": { 
			"type" 		: "range",
			"default"   : "0",
			"sprssDef"  : True,
			"stub"      : "hdmi_mode=%s",
			"valid"		: [1,87],
			"patterns": [{	"id_pattern"      : r"\s*hdmi_mode\s*=",
							"ext_pattern"     : r"\s*hdmi_mode\s*=\s*(\d+)",}
							],
		},

		"hdmi_pixel_encoding": { 
			"type" 		: "range",
			"default"   : "0",
			"sprssDef"  : True,
			"stub"      : "hdmi_pixel_encoding=%s",
			"valid"		: [0,5],
			"patterns": [{	"id_pattern"      : r"\s*hdmi_pixel_encoding\s*=",
							"ext_pattern"     : r"\s*hdmi_pixel_encoding\s*=\s*(\d+)",}
							],
		},

		"sdtv_aspect": { 
			"type" 		: "range",
			"default"   : "1",
			"sprssDef"  : True,
			"stub"      : "sdtv_aspect=%s",
			"valid"		: [1,4],
			"patterns": [{	"id_pattern"      : r"\s*sdtv_aspect\s*=",
							"ext_pattern"     : r"\s*sdtv_aspect\s*=\s*(\d+)",}
							],
		},

		"sdtv_mode": { 
			"type" 		: "range",
			"default"   : "0",
			"sprssDef"  : True,
			"stub"      : "sdtv_mode=%s",
			"valid"		: [0,4],
			"patterns": [{	"id_pattern"      : r"\s*sdtv_mode\s*=",
							"ext_pattern"     : r"\s*sdtv_mode\s*=\s*(\d+)",}
							],
		},

		"spi-bcm2835-overlay": {
			"type" 		: "boolspec",
			"default"   : "false",
			"sprssDef"  : True,
			"stub"      : "dtoverlay=%s",
			"valid"		: ["spi-bcm2835-overlay"],
			"patterns": [{	"id_pattern"      : r"\s*(?:dtoverlay|device_tree_overlay)\s*=\s*[-\w\d]*spi-bcm2835[-\w\d]*",
							"ext_pattern"     : r"\s*(?:dtoverlay|device_tree_overlay)\s*=\s*([-\w\d]*spi-bcm2835[-\w\d]*)",}
							],
		},

		"hdmi_safe": { 
			"type" 		: 'bool',
			"default"   : "false",
			"sprssDef"  : True,
			"stub"      : "hdmi_safe=%s",
			"valid"		: [0,1],
			"patterns": [{	"id_pattern"      : r"\s*hdmi_safe\s*=",
							"ext_pattern"     : r"\s*hdmi_safe\s*=\s*(\d+)",}
							],
		},

		"audio":{ 
			"type" 		: "alwaysdrop",
			"default"   : 0,
			"sprssDef"  : True,
			"stub"		: "dtparam=audio=%s",
			"valid"		: [],
			"patterns": [{	"id_pattern" 	: r"\s*(?:dtparam|dtparams|device_tree_param|device_tree_params)\s*=.*audio\s*=",
							"ext_pattern"	: r"\s*(?:dtparam|dtparams|device_tree_param|device_tree_params)\s*=.*audio\s*=\s*(\w+)",}
								],
		},

		"w1gpio": { 
			"type" 		: "selection",
			"default"   : "0",
			"sprssDef"  : True,
			"stub"      : "dtoverlay=%s",
			"valid"		: [	
							# config value				KODI value
							('w1-gpio-overlay'			, 1),
							('w1-gpio-pullup-overlay'	, 2)
							],
			"patterns": [{	"id_pattern"      : r"\s*(?:dtoverlay|device_tree_overlay)\s*=.*w1-gpio",
							"ext_pattern"     : r"\s*(?:dtoverlay|device_tree_overlay)\s*=\s*([-\w\d]*w1-gpio[-\w\d]*)",}
							],
		},

		"soundcard_dac": {
			"type" 		: 'selection',
			"default"   : 0,
			"sprssDef"  : True,
			"stub"      : "dtoverlay=%s",
			"valid"		: [
							# string to write back to the config.txt					
							('hifiberry-dac-overlay\ndtparam=audio=off' 				, 1 ),
							('hifiberry-dacplus-overlay\ndtparam=audio=off' 			, 2 ),
							('hifiberry-digi-overlay\ndtparam=audio=off' 				, 3 ),
							('iqaudio-dac-overlay,unmute_amp\ndtparam=audio=off' 		, 4 ),
							('iqaudio-dacplus-overlay,unmute_amp\ndtparam=audio=off' 	, 5 ),

							# config.txt string						# KODI value
							('hifiberry-dac-overlay' 				, 1 ),
							('hifiberry-dac' 						, 1 ),
							('hifiberry-dacplus-overlay' 			, 2 ),
							('hifiberry-dacplus' 					, 2 ),
							('hifiberry-digi-overlay' 				, 3 ),
							('hifiberry-digi' 						, 3 ),
							('iqaudio-dac-overlay,unmute_amp' 		, 4 ),
							('iqaudio-dac-overlay' 					, 4 ),
							('iqaudio-dac' 							, 4 ),
							('iqaudio-dac,unmute_amp' 				, 4 ),
							('iqaudio-dacplus-overlay,unmute_amp' 	, 5 ),
							('iqaudio-dacplus-overlay' 				, 5 ),
							('iqaudio-dacplus,unmute_amp' 			, 5 ),
							('iqaudio-dacplus' 						, 5 ),
						],
			"patterns": [{	"id_pattern"      : r"\s*(?:dtoverlay|device_tree_overlay)\s*=\s*[-\w\d]*(?:hifiberry-d|iqaudio-d)",
							"ext_pattern"     : r"\s*(?:dtoverlay|device_tree_overlay)\s*=\s*([-\w\d]*(?:hifiberry-d|iqaudio-d)[-\w\d]*)",}
							],
		},

		"lirc-rpi-overlay": { 
			"type" 		: "boolspec",
			"default"   : 0,
			"sprssDef"  : True,
			"stub"      : "dtoverlay=%s",
			"valid"		: [	
							"lirc-rpi-overlay", 
							"lirc-rpi"
							],
			"patterns": [{	"id_pattern"      : r"\s*(?:dtoverlay|device_tree_overlay)\s*=\s*[-\w\d]*lirc-rpi[-\w\d]*",
							"ext_pattern"     : r"\s*(?:dtoverlay|device_tree_overlay)\s*=\s*([-\w\d]*lirc-rpi[-\w\d]*)",}
							],
		},

		"gpio_in_pin": { 
			"type" 		: "range",
			"default"   : "18",
			"sprssDef"  : True,
			"stub"      : "dtparam=gpio_in_pin=%s",
			"valid"		: [1,26],
			"patterns": [{	"id_pattern"      : r"\s*(?:dtoverlay|device_tree_overlay|dtparam|dtparams|device_tree_param|device_tree_params)\s*=(?:lirc-rpi:)?.*gpio_in_pin[-\w\d]*=",
							"ext_pattern"     : r"\s*(?:dtoverlay|device_tree_overlay|dtparam|dtparams|device_tree_param|device_tree_params)\s*=(?:lirc-rpi:)?.*gpio_in_pin[-\w\d]*=\s*(\w*)",}
							],
		},

		"gpio_in_pull": { 
			"type" 		: "boolspec",
			"default"   : "off",
			"sprssDef"  : True,
			"stub"      : "dtparam=gpio_in_pull=%s",
			"valid"		: [
							('down', 1),
							('up', 2),
							],
			"patterns": [{	"id_pattern"      : r"\s*(?:dtoverlay|device_tree_overlay|dtparam|dtparams|device_tree_param|device_tree_params)\s*=(?:lirc-rpi:)?.*gpio_in_pull[-\w\d]*=",
							"ext_pattern"     : r"\s*(?:dtoverlay|device_tree_overlay|dtparam|dtparams|device_tree_param|device_tree_params)\s*=(?:lirc-rpi:)?.*gpio_in_pull[-\w\d]*=\s*(\w*)",}
							],
		},

		"gpio_out_pin": { 
			"type" 		: "range",
			"default"   : "17",
			"sprssDef"  : True,
			"stub"      : "dtparam=gpio_out_pin=%s",
			"valid"		: [1,26],
			"patterns": [{	"id_pattern"      : r"\s*(?:dtoverlay|device_tree_overlay|dtparam|dtparams|device_tree_param|device_tree_params)\s*=(?:lirc-rpi:)?.*gpio_out_pin[-\w\d]*=",
							"ext_pattern"     : r"\s*(?:dtoverlay|device_tree_overlay|dtparam|dtparams|device_tree_param|device_tree_params)\s*=(?:lirc-rpi:)?.*gpio_out_pin[-\w\d]*=\s*(\w*)",}
							],
		},

		"arm_freq": { 
			"type" 		: "range_var",
			"default"   : {"PiB": 700, "Pi2": 900},
			"sprssDef"  : True,
			"stub"      : "arm_freq=%s",
			"valid"		: [600, 1201],
			"patterns": [{	"id_pattern"      : r"\s*arm_freq\s*=\s*",
							"ext_pattern"     : r"\s*arm_freq\s*=\s*(\d+)",}
							],
		},

		"sdram_freq": { 
			"type" 		: "range_var",
			"default"   : {"PiB": 400, "Pi2": 450},
			"sprssDef"  : True,
			"stub"      : "sdram_freq=%s",
			"valid"		: [300, 701],
			"patterns": [{	"id_pattern"      : r"\s*sdram_freq\s*=\s*",
							"ext_pattern"     : r"\s*sdram_freq\s*=\s*(\d+)",}
							],
		},

		"core_freq": { 
			"type" 		: "range_var",
			"default"   : {"PiB": 250, "Pi2": 450},
			"sprssDef"  : True,
			"stub"      : "core_freq=%s",
			"valid"		: [150, 651],
			"patterns": [{	"id_pattern"      : r"\s*core_freq\s*=\s*",
							"ext_pattern"     : r"\s*core_freq\s*=\s*(\d+)",}
							],
		},		

		"initial_turbo": { 
			"type" 		: "range",
			"default"   : "0",
			"sprssDef"  : True,
			"stub"      : "initial_turbo=%s",
			"valid"		: [0, 61],
			"patterns": [{	"id_pattern"      : r"\s*initial_turbo\s*=\s*",
							"ext_pattern"     : r"\s*initial_turbo\s*=\s*(\d+)",}
							],
		},		

		"over_voltage": { 
			"type" 		: "range",
			"default"   : "0",
			"sprssDef"  : True,
			"stub"      : "over_voltage=%s",
			"valid"		: [0,9],
			"patterns": [{	"id_pattern"      : r"\s*over_voltage\s*=\s*",
							"ext_pattern"     : r"\s*over_voltage\s*=\s*(\d+)",}
							],
		},		

		"over_voltage_sdram": { 
			"type" 		: "range",
			"default"   : "0",
			"sprssDef"  : True,
			"stub"      : "over_voltage_sdram=%s",
			"valid"		: [0,9],
			"patterns": [{	"id_pattern"      : r"\s*over_voltage_sdram\s*=\s*",
							"ext_pattern"     : r"\s*over_voltage_sdram\s*=\s*(\d+)",}
							],
		},		

		"force_turbo": { 
			"type" 		: "bool",
			"default"   : "0",
			"sprssDef"  : True,
			"stub"      : "force_turbo=%s",
			"valid"		: [0,1],
			"patterns": [{	"id_pattern"      : r"\s*force_turbo\s*=\s*",
							"ext_pattern"     : r"\s*force_turbo\s*=\s*(\d+)",}
							],
		},		
	
	}

