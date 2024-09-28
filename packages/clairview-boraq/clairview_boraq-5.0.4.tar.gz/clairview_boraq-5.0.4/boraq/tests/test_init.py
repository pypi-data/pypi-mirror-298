# imports - standard imports
import json
import os
import subprocess
import unittest

# imports - third paty imports
import git

# imports - module imports
from boraq.utils import exec_cmd
from boraq.app import App
from boraq.tests.test_base import CLAIRVIEW_BRANCH, TestBoraqBase
from boraq.boraq import Boraq


# changed from clairview_theme because it wasn't maintained and incompatible,
# chat app & wiki was breaking too. hopefully clairview_docs will be maintained
# for longer since docs.clairerp.com is powered by it ;)
TEST_CLAIRVIEW_APP = "clairview_docs"


class TestBoraqInit(TestBoraqBase):
	def test_utils(self):
		self.assertEqual(subprocess.call("boraq"), 0)

	def test_init(self, boraq_name="test-boraq", **kwargs):
		self.init_boraq(boraq_name, **kwargs)
		app = App("file:///tmp/clairview")
		self.assertTupleEqual(
			(app.mount_path, app.url, app.repo, app.app_name, app.org),
			("/tmp/clairview", "file:///tmp/clairview", "clairview", "clairview", "clairview"),
		)
		self.assert_folders(boraq_name)
		self.assert_virtual_env(boraq_name)
		self.assert_config(boraq_name)
		test_boraq = Boraq(boraq_name)
		app = App("clairview", boraq=test_boraq)
		self.assertEqual(app.from_apps, True)

	def basic(self):
		try:
			self.test_init()
		except Exception:
			print(self.get_traceback())

	def test_multiple_boraqes(self):
		for boraq_name in ("test-boraq-1", "test-boraq-2"):
			self.init_boraq(boraq_name, skip_assets=True)

		self.assert_common_site_config(
			"test-boraq-1",
			{
				"webserver_port": 8000,
				"socketio_port": 9000,
				"file_watcher_port": 6787,
				"redis_queue": "redis://127.0.0.1:11000",
				"redis_socketio": "redis://127.0.0.1:13000",
				"redis_cache": "redis://127.0.0.1:13000",
			},
		)

		self.assert_common_site_config(
			"test-boraq-2",
			{
				"webserver_port": 8001,
				"socketio_port": 9001,
				"file_watcher_port": 6788,
				"redis_queue": "redis://127.0.0.1:11001",
				"redis_socketio": "redis://127.0.0.1:13001",
				"redis_cache": "redis://127.0.0.1:13001",
			},
		)

	def test_new_site(self):
		boraq_name = "test-boraq"
		site_name = "test-site.local"
		boraq_path = os.path.join(self.boraqes_path, boraq_name)
		site_path = os.path.join(boraq_path, "sites", site_name)
		site_config_path = os.path.join(site_path, "site_config.json")

		self.init_boraq(boraq_name)
		self.new_site(site_name, boraq_name)

		self.assertTrue(os.path.exists(site_path))
		self.assertTrue(os.path.exists(os.path.join(site_path, "private", "backups")))
		self.assertTrue(os.path.exists(os.path.join(site_path, "private", "files")))
		self.assertTrue(os.path.exists(os.path.join(site_path, "public", "files")))
		self.assertTrue(os.path.exists(site_config_path))

		with open(site_config_path) as f:
			site_config = json.loads(f.read())

			for key in ("db_name", "db_password"):
				self.assertTrue(key in site_config)
				self.assertTrue(site_config[key])

	def test_get_app(self):
		self.init_boraq("test-boraq", skip_assets=True)
		boraq_path = os.path.join(self.boraqes_path, "test-boraq")
		exec_cmd(f"boraq get-app {TEST_CLAIRVIEW_APP} --skip-assets", cwd=boraq_path)
		self.assertTrue(os.path.exists(os.path.join(boraq_path, "apps", TEST_CLAIRVIEW_APP)))
		app_installed_in_env = TEST_CLAIRVIEW_APP in subprocess.check_output(
			["boraq", "pip", "freeze"], cwd=boraq_path
		).decode("utf8")
		self.assertTrue(app_installed_in_env)

	@unittest.skipIf(CLAIRVIEW_BRANCH != "develop", "only for develop branch")
	def test_get_app_resolve_deps(self):
		CLAIRVIEW_APP = "healthcare"
		self.init_boraq("test-boraq", skip_assets=True)
		boraq_path = os.path.join(self.boraqes_path, "test-boraq")
		exec_cmd(f"boraq get-app {CLAIRVIEW_APP} --resolve-deps --skip-assets", cwd=boraq_path)
		self.assertTrue(os.path.exists(os.path.join(boraq_path, "apps", CLAIRVIEW_APP)))

		states_path = os.path.join(boraq_path, "sites", "apps.json")
		self.assertTrue(os.path.exists(states_path))

		with open(states_path) as f:
			states = json.load(f)

		self.assertTrue(CLAIRVIEW_APP in states)

	def test_install_app(self):
		boraq_name = "test-boraq"
		site_name = "install-app.test"
		boraq_path = os.path.join(self.boraqes_path, "test-boraq")

		self.init_boraq(boraq_name, skip_assets=True)
		exec_cmd(
			f"boraq get-app {TEST_CLAIRVIEW_APP} --branch master --skip-assets", cwd=boraq_path
		)

		self.assertTrue(os.path.exists(os.path.join(boraq_path, "apps", TEST_CLAIRVIEW_APP)))

		# check if app is installed
		app_installed_in_env = TEST_CLAIRVIEW_APP in subprocess.check_output(
			["boraq", "pip", "freeze"], cwd=boraq_path
		).decode("utf8")
		self.assertTrue(app_installed_in_env)

		# create and install app on site
		self.new_site(site_name, boraq_name)
		installed_app = not exec_cmd(
			f"boraq --site {site_name} install-app {TEST_CLAIRVIEW_APP}",
			cwd=boraq_path,
			_raise=False,
		)

		if installed_app:
			app_installed_on_site = subprocess.check_output(
				["boraq", "--site", site_name, "list-apps"], cwd=boraq_path
			).decode("utf8")
			self.assertTrue(TEST_CLAIRVIEW_APP in app_installed_on_site)

	def test_remove_app(self):
		self.init_boraq("test-boraq", skip_assets=True)
		boraq_path = os.path.join(self.boraqes_path, "test-boraq")

		exec_cmd(
			f"boraq get-app {TEST_CLAIRVIEW_APP} --branch master --overwrite --skip-assets",
			cwd=boraq_path,
		)
		exec_cmd(f"boraq remove-app {TEST_CLAIRVIEW_APP}", cwd=boraq_path)

		with open(os.path.join(boraq_path, "sites", "apps.txt")) as f:
			self.assertFalse(TEST_CLAIRVIEW_APP in f.read())
		self.assertFalse(
			TEST_CLAIRVIEW_APP
			in subprocess.check_output(["boraq", "pip", "freeze"], cwd=boraq_path).decode("utf8")
		)
		self.assertFalse(os.path.exists(os.path.join(boraq_path, "apps", TEST_CLAIRVIEW_APP)))

	def test_switch_to_branch(self):
		self.init_boraq("test-boraq", skip_assets=True)
		boraq_path = os.path.join(self.boraqes_path, "test-boraq")
		app_path = os.path.join(boraq_path, "apps", "clairview")

		# * chore: change to 14 when avalible
		prevoius_branch = "version-13"
		if CLAIRVIEW_BRANCH != "develop":
			# assuming we follow `version-#`
			prevoius_branch = f"version-{int(CLAIRVIEW_BRANCH.split('-')[1]) - 1}"

		successful_switch = not exec_cmd(
			f"boraq switch-to-branch {prevoius_branch} clairview --upgrade",
			cwd=boraq_path,
			_raise=False,
		)
		if successful_switch:
			app_branch_after_switch = str(git.Repo(path=app_path).active_branch)
			self.assertEqual(prevoius_branch, app_branch_after_switch)

		successful_switch = not exec_cmd(
			f"boraq switch-to-branch {CLAIRVIEW_BRANCH} clairview --upgrade",
			cwd=boraq_path,
			_raise=False,
		)
		if successful_switch:
			app_branch_after_second_switch = str(git.Repo(path=app_path).active_branch)
			self.assertEqual(CLAIRVIEW_BRANCH, app_branch_after_second_switch)


if __name__ == "__main__":
	unittest.main()
