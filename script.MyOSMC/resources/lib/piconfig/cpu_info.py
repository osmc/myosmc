
import os
from xml.etree import ElementTree


def get_proc_info(info_file='/proc/cpuinfo', revision=None):
    """
      Get processor information for all pi models. If revision is None then read from /proc/cpuinfo,
      otherwise assume we've been feed a revision (mainly for testing)
    """
    if not revision:
        with open(info_file, 'r') as f:
            lines = f.readlines()
        try:
            revision = int([r for r in lines if r.startswith('Revision')][0].split()[-1], 16)
        except IndexError: # Revision was not found
            return None

    return {
        'raw': hex(revision),
        'revision': '1.' + str(revision & 0xf),
        'type': hex((revision & 0xff0) >> 4),
        'processor': hex((revision & 0xf000) >> 12),
        'manufacturer': hex((revision & 0xf0000) >> 16),
        'memory': hex((revision & 0x700000) >> 20),
        'new': int((revision & 0x800000) >> 23),
    }


def get_clock_settings(procinfo):
    """
       Read clock settings from xml
    """

    curdir = os.path.dirname(os.path.realpath(__file__))
    et = ElementTree.parse(curdir + '/pimodels.xml').getroot()

    if not procinfo['new']:
        # Lump all older versions of the Pi as a legacy model
        ptype = 'legacy'
    else:
        ptype = procinfo['type']

    try:
        m = [e for e in et.findall('model') if e.get('code') == ptype][0]
    except IndexError:
        return None

    settings = {'name': m.get('name')}
    for preset in ('normal', 'medium', 'higher'):
        try:
            settings[preset] = {i.tag: i.text for i in m.find(preset).iter()}
        except AttributeError:
            settings[preset] = None
    return settings