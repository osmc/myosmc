import env
import os
import unittest

from lib.piconfig.configfileinterface import ConfigFileInterface
from lib.piconfig.pisettings import CLASS_LIBRARY, SettingClassFactory
from lib.piconfig.mastersettings import MASTER_SETTING_PATTERNS

from mock import patch, mock_open

SAMPLES = {
        '#': '',
        None: '',
        'test  # commented out': 'test',
        'extraspaces  ': 'extraspaces',
        '  extraspaces': 'extraspaces',
        ' ' : '',
        '   ': '',
        'perfect:1231234': 'perfect:1231234',
        }

RANGE_ITEMS = {
            'hdmi_boost': xrange(1,12),
            'config_hdmi_boost': xrange(1,12),
            'sdtv_aspect': xrange(1,4),
            'hdmi_mode': xrange(1,87),
            'over_voltage': xrange(10),
            'over_voltage_sdram': xrange(10),
            'core_freq': xrange(150,651),
            'gpu_mem_256': xrange(16,193),
            'gpu_mem_512': xrange(16,257),
            'gpu_mem_1024': xrange(16,321),
            'hdmi_force_hotplug': xrange(2),
            'hdmi_ignore_cec': xrange(2),
            'hdmi_ignore_cec_init': xrange(2),
            'hdmi_safe': xrange(2),
            'hdmi_edid_file': xrange(2),
            'force_turbo': xrange(2),
            'start_x': xrange(2),
            'sdram_freq': xrange(300,701),
            'hdmi_group': xrange(4),
            'sdtv_mode': xrange(5),
            'hdmi_pixel_encoding': xrange(6),
            'arm_freq': xrange(600,1201),
            'initial_turbo': xrange(62),
        }


class ConfigFileInterfaceTest(unittest.TestCase):

    def setUp(self):

        this_file_loc = os.path.dirname(os.path.abspath(__file__))
        self.location = os.path.join(this_file_loc, 'test_data', 'config.txt')
        self.cfi = ConfigFileInterface(self.location)

    def test_construction_default_location(self):
        test_cfi = ConfigFileInterface()
        self.assertEqual(test_cfi.location, '/boot/config.txt')

    def test_construction_provided_location(self):
        self.assertEqual(self.cfi.location, self.location)

    def test_clean_this_line(self):
        for original_line, clean_line in SAMPLES.iteritems():
            self.assertEqual(self.cfi._clean_this_line(original_line=original_line),
                clean_line, msg='Failed to clean %s into %s' % (original_line, clean_line))

    def test_clean_this_doc(self):
        doc = SAMPLES.keys()
        test_doc = self.cfi._clean_this_doc(doc=doc)
        # test the values in test_doc, match those in SAMPLE
        for line_dict in test_doc:
            key = line_dict['original']
            self.assertDictEqual(line_dict, {'original': key, 'clean': SAMPLES[key], 'setting':None})
        # test the keys in SAMPLE are represented in test_doc
        target_keys = SAMPLES.keys()
        target_keys.sort()
        test_keys = [x['original'] for x in test_doc]
        test_keys.sort()
        self.assertEqual(test_keys, target_keys)



    def test_range_items_inrange(self):

        test_count = 0
        for k, v in MASTER_SETTING_PATTERNS.iteritems():

            if v['type'] not in ['range', 'range_var']:
                continue

            target_class = CLASS_LIBRARY[v['type']]
            test_count += 1


            for i in xrange(v['valid'][0], v['valid'][1]):
                fake_entry = v['stub'] % i

                _setting_classes = SettingClassFactory()
                clean_doc = self.cfi._clean_this_doc([fake_entry])

                clean_doc = self.cfi._assign_setting_classes_to_doc(clean_doc, _setting_classes)
                try:
                    self.assertEqual(clean_doc[0]['original'], fake_entry, msg='%s failed range test (original)' % k)
                    self.assertEqual(clean_doc[0]['clean'], fake_entry, msg='%s failed range test (clean)' % k)
                    self.assertIsInstance(clean_doc[0]['setting'], target_class, msg='%s failed range test %s (%s vs %s)' \
                        % (i, k, type(clean_doc[0]['setting']), target_class))
                except KeyError:
                    self.fail(msg='Failed Range test. Key not found for %s' % k)

        self.assertTrue(test_count > 0, msg='No Rrange tests were run.' )

