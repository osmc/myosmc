from mock import Mock
from pprint import pprint
import os
import sys


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

cfi = ConfigFileInterface(location=samples + CONFIG_FILE )
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

pprint(settings)