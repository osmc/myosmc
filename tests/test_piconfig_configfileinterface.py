import env
import os
import unittest

from lib.piconfig.configfileinterface import ConfigFileInterface, SettingClassFactory
import lib.piconfig.config_classes as  config_classes
from lib.piconfig.mastersettings import MASTER_SETTING_PATTERNS

from test_database_dbinterface import FreshDatabase
from test_data import master_config_read as mcr

CLASS_LIBRARY = config_classes.CLASS_LIBRARY

from mock import patch, mock_open

SAMPLES = {
        '#': ('#', ''),
        None: ('',''),
        'test  # commented out': ('test','# commented out'),
        'extraspaces  ': ('extraspaces', ''),
        '  extraspaces': ('extraspaces', ''),
        ' ' : ('',''),
        '   ': ('', ''),
        'perfect:1231234': ('perfect:1231234', ''),
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

class pseudoWriter():
    ''' We cant test actually writing to the config file, so
        this class mocks that function.
    '''

    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def writelines(self, *args, **kwargs):
        pass

class ConfigFileInterfaceTest(unittest.TestCase):

    def setUp(self):

        self.this_file_loc = os.path.dirname(os.path.abspath(__file__))
        self.location = os.path.join(self.this_file_loc, 'test_data', 'config.txt')
        self.cfi = ConfigFileInterface(self.location)

        self.dbpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data', 'test.db')

        os.environ['DBPATH'] = self.dbpath

        try:
            os.remove(self.dbpath)
        except IOError:   # pragma: no cover
            pass
        except OSError:   # pragma: no cover
            pass
        except WindowsError:   # pragma: no cover
            pass

    def tearDown(self):
        try:
            os.remove(self.dbpath)
        except:
            pass

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
            self.assertDictEqual(line_dict, {
                                            'original': key, 
                                            'clean': SAMPLES[key][0], 
                                            'inline': SAMPLES[key][1], 
                                            'setting':None}
                                            )
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
                    self.assertEqual(clean_doc[0]['original'], fake_entry, msg='%s failed inrange test (original)' % k)
                    self.assertEqual(clean_doc[0]['clean'], fake_entry, msg='%s failed inrange test (clean)' % k)
                    self.assertIsInstance(clean_doc[0]['setting'], target_class, msg='%s failed inrange test %s (%s vs %s)' \
                        % (k, i, type(clean_doc[0]['setting']), target_class))
                except KeyError:
                    self.fail(msg='Failed inrange test. Key not found for %s' % k)

        self.assertTrue(test_count > 0, msg='No inrange tests were run.' )

    def test_range_items_outrange(self):

        test_count = 0
        for k, v in MASTER_SETTING_PATTERNS.iteritems():

            if v['type'] not in ['range']:
                continue

            target_class = CLASS_LIBRARY['range']
            test_count += 1

            invalid_value = max(xrange(v['valid'][0], v['valid'][1])) + 2
            fake_entry = v['stub'] % invalid_value

            _setting_classes = SettingClassFactory()
            clean_doc = self.cfi._clean_this_doc([fake_entry])

            clean_doc = self.cfi._assign_setting_classes_to_doc(clean_doc, _setting_classes)

            try:
                self.assertIsInstance(clean_doc[0]['setting'], target_class, msg='%s failed outrange test %s (%s vs %s)' \
                    % (k, invalid_value, type(clean_doc[0]['setting']), target_class))
            except KeyError:
                self.fail(msg='Failed outange test. Key not found for %s' % k)

        self.assertTrue(test_count > 0, msg='No outrange tests were run.' )

    def test_master_config_read(self):

        master_config_location = os.path.join(self.this_file_loc, 'test_data', 'public_configs', 'master_config.txt')
        target_results = mcr.MCR 

        cfi = ConfigFileInterface(master_config_location)

        _, settings = cfi.read_config_txt()

        for k, v in settings.items():
            self.assertEqual(str(v), str(target_results[k]), 
                msg='Returned setting value (%s) != target value (%s) for %s' % (v, target_results[k], k))

    def test_master_config_write(self):

        master_config_location = os.path.join(self.this_file_loc, 'test_data', 'public_configs', 'master_config.txt')
        settings_changes = mcr.MCR_changes

        cfi = ConfigFileInterface(master_config_location, writer=pseudoWriter)

        cfi.write_config_txt(settings_changes)
    
    def test_write_to_db(self):

        master_config_location = os.path.join(self.this_file_loc, 'test_data', 'public_configs', 'master_config.txt')
        cfi = ConfigFileInterface(master_config_location)