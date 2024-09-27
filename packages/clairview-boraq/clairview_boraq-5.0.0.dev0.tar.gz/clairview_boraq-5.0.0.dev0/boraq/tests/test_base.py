# imports - standard imports
import getpass
import json
import os
import shutil
import subprocess
import sys
import traceback
import unittest

# imports - module imports
from boraq.utils import paths_in_boraq, exec_cmd
from boraq.utils.system import init
from boraq.boraq import Boraq

PYTHON_VER = sys.version_info

CLAIRVIEW_BRANCH = "version-13-hotfix"
if PYTHON_VER.major == 3:
	if PYTHON_VER.minor >= 10:
		CLAIRVIEW_BRANCH = "develop"


class TestBoraqBase(unittest.TestCase):
	def setUp(self):
		self.boraqes_path = "."
		self.boraqes = []

	def tearDown(self):
		for boraq_name in self.boraqes:
			boraq_path = os.path.join(self.boraqes_path, boraq_name)
			boraq = Boraq(boraq_path)
			mariadb_password = (
				"travis"
				if os.environ.get("CI")
				else getpass.getpass(prompt="Enter MariaDB root Password: ")
			)

			if boraq.exists:
				for site in boraq.sites:
					subprocess.call(
						[
							"boraq",
							"drop-site",
							site,
							"--force",
							"--no-backup",
							"--root-password",
							mariadb_password,
						],
						cwd=boraq_path,
					)
				shutil.rmtree(boraq_path, ignore_errors=True)

	def assert_folders(self, boraq_name):
		for folder in paths_in_boraq:
			self.assert_exists(boraq_name, folder)
		self.assert_exists(boraq_name, "apps", "clairview")

	def assert_virtual_env(self, boraq_name):
		boraq_path = os.path.abspath(boraq_name)
		python_path = os.path.abspath(os.path.join(boraq_path, "env", "bin", "python"))
		self.assertTrue(python_path.startswith(boraq_path))
		for subdir in ("bin", "lib", "share"):
			self.assert_exists(boraq_name, "env", subdir)

	def assert_config(self, boraq_name):
		for config, search_key in (
			("redis_queue.conf", "redis_queue.rdb"),
			("redis_cache.conf", "redis_cache.rdb"),
		):

			self.assert_exists(boraq_name, "config", config)

			with open(os.path.join(boraq_name, "config", config)) as f:
				self.assertTrue(search_key in f.read())

	def assert_common_site_config(self, boraq_name, expected_config):
		common_site_config_path = os.path.join(
			self.boraqes_path, boraq_name, "sites", "common_site_config.json"
		)
		self.assertTrue(os.path.exists(common_site_config_path))

		with open(common_site_config_path) as f:
			config = json.load(f)

		for key, value in list(expected_config.items()):
			self.assertEqual(config.get(key), value)

	def assert_exists(self, *args):
		self.assertTrue(os.path.exists(os.path.join(*args)))

	def new_site(self, site_name, boraq_name):
		new_site_cmd = ["boraq", "new-site", site_name, "--admin-password", "admin"]

		if os.environ.get("CI"):
			new_site_cmd.extend(["--mariadb-root-password", "travis"])

		subprocess.call(new_site_cmd, cwd=os.path.join(self.boraqes_path, boraq_name))

	def init_boraq(self, boraq_name, **kwargs):
		self.boraqes.append(boraq_name)
		clairview_tmp_path = "/tmp/clairview"

		if not os.path.exists(clairview_tmp_path):
			exec_cmd(
				f"git clone https://github.com/clairview/clairview -b {CLAIRVIEW_BRANCH} --depth 1 --origin upstream {clairview_tmp_path}"
			)

		kwargs.update(
			dict(
				python=sys.executable,
				no_procfile=True,
				no_backups=True,
				clairview_path=clairview_tmp_path,
			)
		)

		if not os.path.exists(os.path.join(self.boraqes_path, boraq_name)):
			init(boraq_name, **kwargs)
			exec_cmd(
				"git remote set-url upstream https://github.com/clairview/clairview",
				cwd=os.path.join(self.boraqes_path, boraq_name, "apps", "clairview"),
			)

	def file_exists(self, path):
		if os.environ.get("CI"):
			return not subprocess.call(["sudo", "test", "-f", path])
		return os.path.isfile(path)

	def get_traceback(self):
		exc_type, exc_value, exc_tb = sys.exc_info()
		trace_list = traceback.format_exception(exc_type, exc_value, exc_tb)
		return "".join(str(t) for t in trace_list)
