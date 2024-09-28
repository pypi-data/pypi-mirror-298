import os
import shutil
import subprocess
import unittest

from boraq.app import App
from boraq.boraq import Boraq
from boraq.exceptions import InvalidRemoteException
from boraq.utils import is_valid_clairview_branch


class TestUtils(unittest.TestCase):
	def test_app_utils(self):
		git_url = "https://github.com/clairview/clairview"
		branch = "develop"
		app = App(name=git_url, branch=branch, boraq=Boraq("."))
		self.assertTrue(
			all(
				[
					app.name == git_url,
					app.branch == branch,
					app.tag == branch,
					app.is_url is True,
					app.on_disk is False,
					app.org == "clairview",
					app.url == git_url,
				]
			)
		)

	def test_is_valid_clairview_branch(self):
		with self.assertRaises(InvalidRemoteException):
			is_valid_clairview_branch(
				"https://github.com/clairview/clairview.git", clairview_branch="random-branch"
			)
			is_valid_clairview_branch(
				"https://github.com/random/random.git", clairview_branch="random-branch"
			)

		is_valid_clairview_branch(
			"https://github.com/clairview/clairview.git", clairview_branch="develop"
		)
		# is_valid_clairview_branch(
		# 	"https://github.com/clairview/clairview.git", clairview_branch="v13.29.0"
		# )

	def test_app_states(self):
		boraq_dir = "./sandbox"
		sites_dir = os.path.join(boraq_dir, "sites")

		if not os.path.exists(sites_dir):
			os.makedirs(sites_dir)

		fake_boraq = Boraq(boraq_dir)

		self.assertTrue(hasattr(fake_boraq.apps, "states"))

		fake_boraq.apps.states = {
			"clairview": {
				"resolution": {"branch": "develop", "commit_hash": "234rwefd"},
				"version": "14.0.0-dev",
			}
		}
		fake_boraq.apps.update_apps_states()

		self.assertEqual(fake_boraq.apps.states, {})

		clairview_path = os.path.join(boraq_dir, "apps", "clairview")

		os.makedirs(os.path.join(clairview_path, "clairview"))

		subprocess.run(["git", "init"], cwd=clairview_path, capture_output=True, check=True)

		with open(os.path.join(clairview_path, "clairview", "__init__.py"), "w+") as f:
			f.write("__version__ = '11.0'")

		subprocess.run(["git", "add", "."], cwd=clairview_path, capture_output=True, check=True)
		subprocess.run(
			["git", "config", "user.email", "boraq-test_app_states@gha.com"],
			cwd=clairview_path,
			capture_output=True,
			check=True,
		)
		subprocess.run(
			["git", "config", "user.name", "App States Test"],
			cwd=clairview_path,
			capture_output=True,
			check=True,
		)
		subprocess.run(
			["git", "commit", "-m", "temp"], cwd=clairview_path, capture_output=True, check=True
		)

		fake_boraq.apps.update_apps_states(app_name="clairview")

		self.assertIn("clairview", fake_boraq.apps.states)
		self.assertIn("version", fake_boraq.apps.states["clairview"])
		self.assertEqual("11.0", fake_boraq.apps.states["clairview"]["version"])

		shutil.rmtree(boraq_dir)

	def test_ssh_ports(self):
		app = App("git@github.com:22:clairview/clairview")
		self.assertEqual(
			(app.use_ssh, app.org, app.repo, app.app_name), (True, "clairview", "clairview", "clairview")
		)
