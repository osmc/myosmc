from datetime import datetime
from glob import glob
import os
import subprocess
import time


class OpenWithBackup(object):

	def __init__(self, golden_file, *args, **kwds):

		self.golden_file = golden_file

		self.golden_path = os.path.dirname(self.golden_file)

		self.backup_path = '/home/osmc/.myosmc/backup_files'
		self._touchbackupfolder()

		self.max_backups = 50
		self.tmp_content = None
		self.file_object = None

		self.args = args
		self.kwargs = kwargs


	def __enter__(self):

		with open(self.tmp_content, 'r') as f:
			self.tmp_content = f.readlines()

		self.file_object = open(self.self.golden_file, *self.args, **self.kwargs)

		return self.file_object 


	def __exit__(self, *args):

		self.file_object.close()

		self._create_backup()


	def _touchbackupfolder(self):

		if not os.path.isdir(self.backup_path):
			os.makedirs(self.backup_path)


	def _create_backup(self):

		backups = self._collect_backups()
		backups = self._collate_backups(backups)
		
		self._drop_extras(backups)

		last_backup = self.get_latest_backup()

		# create the new backup filename
		new_fn = os.path.join(self.backup_path, golden_file + '_backup' + _get_now(last_backup))

		# write the backup file contents
		try:
			with open(new_fn, 'w') as f:
				f.writelines(self.tmp_content)
		except IOError:
			pass


	def _get_now(self, last_backup):
		''' Returns the current time as a string. If that cannot be determined,
			then the integer at the end of latest backup filename is sought, iterated, 
			and returned. Failing that, a string zero is sent.
		'''

		date_string = None
		tries = 0

		while tries < 10:

			try:
				return datetime.now().strftime("%Y%m%d%H%M%S")
			except:
				tries += 1
				time.sleep(0.05)

		try:
			return datetime.now().strftime("%Y%m%d%H%M%S")
		except:
			if last_backup is None:
				return '0'
			else:
				try:
					last_backup = last_backup[-21:]

					return str(int(last_backup[last_backup.index('_backup') + 7 : ]) + 1)
				except ValueError:
					return '0'


	def _collect_backups(self):

		return glob( os.path.join(self.backup_path, self.golden_file) + '_backup*' )


	def _collate_backups(self, backups):

		backups = [fn for fn in backups if '_backup' in fn[-21:]]

		backups.sort(key = lambda x: x[-14:])

		return backups


	def _drop_extras(self, backups):
		# delete the extra backups
		if len(backups) >= self.max_backups:
			for fn in backups[:-self.max_backups]:
				self_harddropbackup(fn)


	def _harddropbackup(self, fn):

		subprocess.call(['sudo','rm',fn])


	def get_latest_backup(self, backups):
		try:
			return backups[-1]
		except IndexError:
			return None
