import env
import os
import unittest

from datetime import datetime
from lib.common.openwithbackup import OpenWithBackup
from mock import patch


def raise_KeyError():
    raise KeyError


# class OpenWithBackupTest(unittest.TestCase):

#     def setUp(self):
#         this_file_loc = os.path.dirname(os.path.abspath(__file__))
#         self.goldenfile = os.path.join(this_file_loc, 'test_data', 'config.txt')
#         self.owb = OpenWithBackup(self.goldenfile, 'w')
#         self.test_bupath =  os.path.join(this_file_loc, 'test_data')
#         self.owb.backup_path = self.test_bupath

#     def TearDown(self):
#         pass

#     def test_inst_missing_goldenfile(self):
#         with self.assertRaises(TypeError):
#             OpenWithBackup()

#     def test_inst_blank_goldenfile(self):
#         with self.assertRaises(TypeError):
#             OpenWithBackup('')

#     @patch('os.makedirs')
#     @patch('os.path.isdir', return_value=False)
#     def test_touchbackupfolder(self, mock_isdir, mock_makedirs):
#         self.owb._touchbackupfolder()
#         mock_makedirs.assert_called_once_with(self.test_bupath)

#     def test_get_latest_backup_bad(self):
#         self.assertIs(self.owb.get_latest_backup([]), None)

#     def test_get_latest_backup_god(self):
#         self.assertEquals(self.owb.get_latest_backup([0]), 0)

#     @patch('subprocess.call')
#     def test_harddropbackup(self, mock_spcall):
#         self.owb._harddropbackup('test')
#         mock_spcall.assert_called_once_with(['sudo','rm','test'])

#     @patch('lib.common.openwithbackup.OpenWithBackup._harddropbackup')
#     def test_drop_extra_one(self, mock_hdbu):
#         self.owb.max_backups = 2
#         self.owb._drop_extras(['a','b','c'])
#         mock_hdbu.assert_called_once_with('a')

#     @patch('lib.common.openwithbackup.OpenWithBackup._harddropbackup')
#     def test_drop_extras_three(self, mock_hdbu):
#         self.owb.max_backups = 2
#         self.owb._drop_extras(['a','b','c','d','e'])
#         mock_hdbu.assert_any_call('a')
#         mock_hdbu.assert_any_call('b')
#         mock_hdbu.assert_any_call('c')

#     @patch('lib.common.openwithbackup.OpenWithBackup._harddropbackup')
#     def test_drop_extras_none(self, mock_hdbu):
#         self.owb.max_backups = 2
#         self.owb._drop_extras(['a','b'])
#         mock_hdbu.assert_not_called()

#     def test_collate_backups(self):
#         self.owb.golden_fn = 'a'

#         test = [    'exclude_this',
#                     '/test/a_backup00000000000009',
#                     '/test/a_backup00000000000008',
#                     '/test/a_backup00000000000003',
#                     '/test/a_backup00000000000004',
#                     'exclude_this',
#                     '/test/a_backup00000000000005',]

#         target = [  '/test/a_backup00000000000003',
#                     '/test/a_backup00000000000004',
#                     '/test/a_backup00000000000005',
#                     '/test/a_backup00000000000008',
#                     '/test/a_backup00000000000009',]

#         self.assertEquals(self.owb._collate_backups(test), target)

#     @patch('glob.glob')
#     def test_collect_backups(self, mock_glob):
#         self.owb.backup_path = 'path'
#         self.owb.golden_fn = 'fn'
#         self.owb._collect_backups()
#         mock_glob.assert_called_once_with(os.path.join('path','fn') + '_backup*')

#     @patch('lib.common.openwithbackup.datetime', side_effect=raise_KeyError)
#     @patch('time.sleep')
#     def test_get_now_fallback(self, mock_time, mock_datae):

#         with patch('lib.common.openwithbackup.datetime') as mock_date:
#             # mock_date.now.return_value = datetime.now()
#             mock_date.now.side_effect = raise_KeyError

#             # datetime.now is intended to fail
#             self.assertEqual(self.owb._get_now('/test/a_backup00000000000005'), '6')
#             self.assertEqual(self.owb._get_now('/test/a_backup00000000000011'), '12')
#             self.assertEqual(self.owb._get_now('/test/a_backup11'), '12')

#     @patch('lib.common.openwithbackup.datetime', side_effect=raise_KeyError)
#     @patch('time.sleep')
#     def test_get_now_fallback_fail(self, mock_time, mock_datae):

#         with patch('lib.common.openwithbackup.datetime') as mock_date:
#             # mock_date.now.return_value = datetime.now()
#             mock_date.now.side_effect = raise_KeyError

#             # datetime.now is intended to fail
#             self.assertEqual(self.owb._get_now('/test/a_backupzz'), '0')

#     @patch('lib.common.openwithbackup.datetime', side_effect=raise_KeyError)
#     @patch('time.sleep')
#     def test_get_now_fallback_none(self, mock_time, mock_datae):

#         with patch('lib.common.openwithbackup.datetime') as mock_date:
#             # mock_date.now.return_value = datetime.now()
#             mock_date.now.side_effect = raise_KeyError

#             # datetime.now is intended to fail
#             self.assertEqual(self.owb._get_now(None), '0')

#     @patch('time.sleep')
#     def test_get_now_good(self, mock_time):
#         # datetime.now is intended to fail
#         with patch('lib.common.openwithbackup.datetime') as mock_date:
#             # mock_date.now.return_value = datetime.now()
#             now = datetime.now()
#             string_now = now.strftime("%Y%m%d%H%M%S")
#             mock_date.now.return_value = now

#             self.assertEqual(self.owb._get_now(None), string_now)

#     @patch('subprocess.call')
#     def test_full_build(self, mock_spcall):
#         self.owb.max_backups = 1
#         lines = ['#arm_freq=900\n', 'core_freq=450\n', 'force_turbo=0\n', 'initial_turbo=0\n', 'sdram_freq=450\n']
#         lines.append('#' + datetime.now().strftime("%Y%m%d%H%M%S"))
#         with self.owb as f:
#             f.writelines(lines)
#         self.assertTrue(os.path.isfile(self.owb.new_fn))
#         os.remove(self.owb.new_fn)
#         with open(self.goldenfile, 'w') as f:
#             f.writelines(lines[:5])
