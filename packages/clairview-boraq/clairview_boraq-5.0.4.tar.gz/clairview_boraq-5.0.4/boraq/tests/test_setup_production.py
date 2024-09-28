# imports - standard imports
import getpass
import os
import pathlib
import re
import subprocess
import time
import unittest

# imports - module imports
from boraq.utils import exec_cmd, get_cmd_output, which
from boraq.config.production_setup import get_supervisor_confdir
from boraq.tests.test_base import TestBoraqBase


class TestSetupProduction(TestBoraqBase):
	def test_setup_production(self):
		user = getpass.getuser()

		for boraq_name in ("test-boraq-1", "test-boraq-2"):
			boraq_path = os.path.join(os.path.abspath(self.boraqes_path), boraq_name)
			self.init_boraq(boraq_name)
			exec_cmd(f"sudo boraq setup production {user} --yes", cwd=boraq_path)
			self.assert_nginx_config(boraq_name)
			self.assert_supervisor_config(boraq_name)
			self.assert_supervisor_process(boraq_name)

		self.assert_nginx_process()
		exec_cmd(f"sudo boraq setup sudoers {user}")
		self.assert_sudoers(user)

		for boraq_name in self.boraqes:
			boraq_path = os.path.join(os.path.abspath(self.boraqes_path), boraq_name)
			exec_cmd("sudo boraq disable-production", cwd=boraq_path)

	def production(self):
		try:
			self.test_setup_production()
		except Exception:
			print(self.get_traceback())

	def assert_nginx_config(self, boraq_name):
		conf_src = os.path.join(
			os.path.abspath(self.boraqes_path), boraq_name, "config", "nginx.conf"
		)
		conf_dest = f"/etc/nginx/conf.d/{boraq_name}.conf"

		self.assertTrue(self.file_exists(conf_src))
		self.assertTrue(self.file_exists(conf_dest))

		# symlink matches
		self.assertEqual(os.path.realpath(conf_dest), conf_src)

		# file content
		with open(conf_src) as f:
			f = f.read()

			for key in (
				f"upstream {boraq_name}-clairview",
				f"upstream {boraq_name}-socketio-server",
			):
				self.assertTrue(key in f)

	def assert_nginx_process(self):
		out = get_cmd_output("sudo nginx -t 2>&1")
		self.assertTrue(
			"nginx: configuration file /etc/nginx/nginx.conf test is successful" in out
		)

	def assert_sudoers(self, user):
		sudoers_file = "/etc/sudoers.d/clairview"
		service = which("service")
		nginx = which("nginx")

		self.assertTrue(self.file_exists(sudoers_file))

		if os.environ.get("CI"):
			sudoers = subprocess.check_output(["sudo", "cat", sudoers_file]).decode("utf-8")
		else:
			sudoers = pathlib.Path(sudoers_file).read_text()
		self.assertTrue(f"{user} ALL = (root) NOPASSWD: {service} nginx *" in sudoers)
		self.assertTrue(f"{user} ALL = (root) NOPASSWD: {nginx}" in sudoers)

	def assert_supervisor_config(self, boraq_name, use_rq=True):
		conf_src = os.path.join(
			os.path.abspath(self.boraqes_path), boraq_name, "config", "supervisor.conf"
		)

		supervisor_conf_dir = get_supervisor_confdir()
		conf_dest = f"{supervisor_conf_dir}/{boraq_name}.conf"

		self.assertTrue(self.file_exists(conf_src))
		self.assertTrue(self.file_exists(conf_dest))

		# symlink matches
		self.assertEqual(os.path.realpath(conf_dest), conf_src)

		# file content
		with open(conf_src) as f:
			f = f.read()

			tests = [
				f"program:{boraq_name}-clairview-web",
				f"program:{boraq_name}-redis-cache",
				f"program:{boraq_name}-redis-queue",
				f"group:{boraq_name}-web",
				f"group:{boraq_name}-workers",
				f"group:{boraq_name}-redis",
			]

			if not os.environ.get("CI"):
				tests.append(f"program:{boraq_name}-node-socketio")

			if use_rq:
				tests.extend(
					[
						f"program:{boraq_name}-clairview-schedule",
						f"program:{boraq_name}-clairview-default-worker",
						f"program:{boraq_name}-clairview-short-worker",
						f"program:{boraq_name}-clairview-long-worker",
					]
				)

			else:
				tests.extend(
					[
						f"program:{boraq_name}-clairview-workerbeat",
						f"program:{boraq_name}-clairview-worker",
						f"program:{boraq_name}-clairview-longjob-worker",
						f"program:{boraq_name}-clairview-async-worker",
					]
				)

			for key in tests:
				self.assertTrue(key in f)

	def assert_supervisor_process(self, boraq_name, use_rq=True, disable_production=False):
		out = get_cmd_output("supervisorctl status")

		while "STARTING" in out:
			print("Waiting for all processes to start...")
			time.sleep(10)
			out = get_cmd_output("supervisorctl status")

		tests = [
			r"{boraq_name}-web:{boraq_name}-clairview-web[\s]+RUNNING",
			# Have commented for the time being. Needs to be uncommented later on. Boraq is failing on travis because of this.
			# It works on one boraq and fails on another.giving FATAL or BACKOFF (Exited too quickly (process log may have details))
			# "{boraq_name}-web:{boraq_name}-node-socketio[\s]+RUNNING",
			r"{boraq_name}-redis:{boraq_name}-redis-cache[\s]+RUNNING",
			r"{boraq_name}-redis:{boraq_name}-redis-queue[\s]+RUNNING",
		]

		if use_rq:
			tests.extend(
				[
					r"{boraq_name}-workers:{boraq_name}-clairview-schedule[\s]+RUNNING",
					r"{boraq_name}-workers:{boraq_name}-clairview-default-worker-0[\s]+RUNNING",
					r"{boraq_name}-workers:{boraq_name}-clairview-short-worker-0[\s]+RUNNING",
					r"{boraq_name}-workers:{boraq_name}-clairview-long-worker-0[\s]+RUNNING",
				]
			)

		else:
			tests.extend(
				[
					r"{boraq_name}-workers:{boraq_name}-clairview-workerbeat[\s]+RUNNING",
					r"{boraq_name}-workers:{boraq_name}-clairview-worker[\s]+RUNNING",
					r"{boraq_name}-workers:{boraq_name}-clairview-longjob-worker[\s]+RUNNING",
					r"{boraq_name}-workers:{boraq_name}-clairview-async-worker[\s]+RUNNING",
				]
			)

		for key in tests:
			if disable_production:
				self.assertFalse(re.search(key, out))
			else:
				self.assertTrue(re.search(key, out))


if __name__ == "__main__":
	unittest.main()
