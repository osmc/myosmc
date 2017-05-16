import env
import os
import unittest

from lib.piconfig.configfileinterface import ConfigFileInterface


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
