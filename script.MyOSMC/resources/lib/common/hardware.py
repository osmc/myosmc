
import os

def get_proc_info(info_file='/proc/cpuinfo', revision=None):
    '''
      Get processor information for all pi models. If revision is None then read from /proc/cpuinfo,
      otherwise assume we've been feed a revision (mainly for testing)
    '''
    if not revision:
        with open(info_file, 'r') as f:
            lines = f.readlines()
        try:
            revision = int([r for r in lines if r.startswith('Revision')][0].split()[-1], 16)
        except IndexError: # Revision was not found
            return {}

    return {
        'raw': hex(revision),
        'revision': '1.' + str(revision & 0xf),
        'type': hex((revision & 0xff0) >> 4),
        'processor': hex((revision & 0xf000) >> 12),
        'manufacturer': hex((revision & 0xf0000) >> 16),
        'memory': hex((revision & 0x700000) >> 20),
        'new': int((revision & 0x800000) >> 23),
    }


def get_Pi_clock_settings(pimodels):
    '''
       Read clock settings from xml
    '''

    procinfo = get_proc_info()

    if not procinfo.get('new', None):
        # Lump all older and any unknown versions of the Pi as a legacy model
        ptype = 'legacy'
    else:
        ptype = procinfo['type']

    try:
        return pimodels[ptype]
    except KeyError:
        return None
