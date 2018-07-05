from mock import Mock
from pprint import pprint
import os
import sys

MCR_changes = {
 'arm_freq': 601,
 'audio': 1,
 'config_hdmi_boost': 2,
 'core_freq': 151,
 'decode_MPG2': 'newcodecstring',
 'decode_WVC1': 'newcodecstring',
 'display_rotate': '2',
 'force_turbo': 0,
 'gpio_in_pin': 2,
 'gpio_in_pull': 2,
 'gpio_out_pin': 2,
 'gpu_mem_1024': 162,
 'gpu_mem_256': 121,
 'gpu_mem_512': 162,
 'hdmi_edid_file': 1,
 'hdmi_force_hotplug': 1,
 'hdmi_group': 1,
 'hdmi_ignore_cec': 1,
 'hdmi_ignore_cec_init': 1,
 'hdmi_ignore_edid': 'false',
 'hdmi_mode': 2,
 'hdmi_pixel_encoding': 1,
 'hdmi_safe': 1,
 'initial_turbo': 1,
 'lirc-rpi-overlay': 'true',
 'over_voltage': 1,
 'over_voltage_sdram': 1,
 'passthrough': 'NULLSETTING',
 'sdram_freq': 301,
 'sdtv_aspect': 2,
 'sdtv_mode': 1,
 'soundcard_dac': 1,
 'spi-bcm2835-overlay': 'false',
 'start_x': 1,
 'w1gpio': 0
 }

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(base + '/script.MyOSMC')

samples = base + '/tests/test_data/public_configs/'

sys.modules['xbmc'] = Mock()
sys.modules['xbmcaddon'] = Mock()
sys.modules['xbmcgui'] = Mock()
sys.modules['xbmccvfs'] = Mock()

from resources.lib.piconfig.configfileinterface import ConfigFileInterface

CONFIG_FILE = 'master_config.txt'

with open(samples + CONFIG_FILE, 'r') as f:
  orig_lines = f.readlines()

cfi = ConfigFileInterface(location=samples + CONFIG_FILE, writer=open)
res, settings = cfi.read_config_txt()

fin = [x for x in res if all([x['clean'].strip(), x['clean'] != 'NULL'])]

fin_orig = [x['original'] for x in fin]

passthroughs = [x['original'] for x in fin if 'passthrough' in str(x['setting'])]

fin = [x for x in fin if x['original'] not in passthroughs]

for x in fin:
    pprint(x)
    print '\n'

missing = []
for line in orig_lines:
    if line not in fin_orig:
        if line.strip():
            missing.append(line)

if passthroughs:
    print '\nLINES PASSED THROUGH: \n\t%s' % '\t'.join(passthroughs)

if missing:
    print '\nLINES MISSING: \n\t%s' % '\t'.join(missing)

if __name__ == '__main__':
	cfi.write_config_txt(MCR_changes)
