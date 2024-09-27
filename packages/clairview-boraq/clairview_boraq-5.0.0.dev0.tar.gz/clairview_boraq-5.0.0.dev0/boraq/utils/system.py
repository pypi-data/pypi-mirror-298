# imports - standard imports
import grp
import os
import pwd
import shutil
import sys

# imports - module imports
import boraq
from boraq.utils import (
	exec_cmd,
	get_process_manager,
	log,
	run_clairview_cmd,
	sudoers_file,
	which,
	is_valid_clairview_branch,
)
from boraq.utils.boraq import build_assets, clone_apps_from
from boraq.utils.render import job


@job(title="Initializing Boraq {path}", success="Boraq {path} initialized")
def init(
	path,
	apps_path=None,
	no_procfile=False,
	no_backups=False,
	clairview_path=None,
	clairview_branch=None,
	verbose=False,
	clone_from=None,
	skip_redis_config_generation=False,
	clone_without_update=False,
	skip_assets=False,
	python="python3",
	install_app=None,
	dev=False,
):
	"""Initialize a new boraq directory

	* create a boraq directory in the given path
	* setup logging for the boraq
	* setup env for the boraq
	* setup config (dir/pids/redis/procfile) for the boraq
	* setup patches.txt for boraq
	* clone & install clairview
	        * install python & node dependencies
	        * build assets
	* setup backups crontab
	"""

	# Use print("\033c", end="") to clear entire screen after each step and re-render each list
	# another way => https://stackoverflow.com/a/44591228/10309266

	import boraq.cli
	from boraq.app import get_app, install_apps_from_path
	from boraq.boraq import Boraq

	verbose = boraq.cli.verbose or verbose

	boraq = Boraq(path)

	boraq.setup.dirs()
	boraq.setup.logging()
	boraq.setup.env(python=python)
	config = {}
	if dev:
		config["developer_mode"] = 1
	boraq.setup.config(
		redis=not skip_redis_config_generation,
		procfile=not no_procfile,
		additional_config=config,
	)
	boraq.setup.patches()

	# local apps
	if clone_from:
		clone_apps_from(
			boraq_path=path, clone_from=clone_from, update_app=not clone_without_update
		)

	# remote apps
	else:
		clairview_path = clairview_path or "https://github.com/clairview/clairview.git"
		is_valid_clairview_branch(clairview_path=clairview_path, clairview_branch=clairview_branch)
		get_app(
			clairview_path,
			branch=clairview_branch,
			boraq_path=path,
			skip_assets=True,
			verbose=verbose,
			resolve_deps=False,
		)

		# fetch remote apps using config file - deprecate this!
		if apps_path:
			install_apps_from_path(apps_path, boraq_path=path)

	# getting app on boraq init using --install-app
	if install_app:
		get_app(
			install_app,
			branch=clairview_branch,
			boraq_path=path,
			skip_assets=True,
			verbose=verbose,
			resolve_deps=False,
		)

	if not skip_assets:
		build_assets(boraq_path=path)

	if not no_backups:
		boraq.setup.backups()


def setup_sudoers(user):
	from boraq.config.lets_encrypt import get_certbot_path

	if not os.path.exists("/etc/sudoers.d"):
		os.makedirs("/etc/sudoers.d")

		set_permissions = not os.path.exists("/etc/sudoers")
		with open("/etc/sudoers", "a") as f:
			f.write("\n#includedir /etc/sudoers.d\n")

		if set_permissions:
			os.chmod("/etc/sudoers", 0o440)

	template = boraq.config.env().get_template("clairview_sudoers")
	clairview_sudoers = template.render(
		**{
			"user": user,
			"service": which("service"),
			"systemctl": which("systemctl"),
			"nginx": which("nginx"),
			"certbot": get_certbot_path(),
		}
	)

	with open(sudoers_file, "w") as f:
		f.write(clairview_sudoers)

	os.chmod(sudoers_file, 0o440)
	log(f"Sudoers was set up for user {user}", level=1)


def start(no_dev=False, concurrency=None, procfile=None, no_prefix=False, procman=None):
	program = which(procman) if procman else get_process_manager()
	if not program:
		raise Exception("No process manager found")

	os.environ["PYTHONUNBUFFERED"] = "true"
	if not no_dev:
		os.environ["DEV_SERVER"] = "true"

	command = [program, "start"]
	if concurrency:
		command.extend(["-c", concurrency])

	if procfile:
		command.extend(["-f", procfile])

	if no_prefix:
		command.extend(["--no-prefix"])

	os.execv(program, command)


def migrate_site(site, boraq_path="."):
	run_clairview_cmd("--site", site, "migrate", boraq_path=boraq_path)


def backup_site(site, boraq_path="."):
	run_clairview_cmd("--site", site, "backup", boraq_path=boraq_path)


def backup_all_sites(boraq_path="."):
	from boraq.boraq import Boraq

	for site in Boraq(boraq_path).sites:
		backup_site(site, boraq_path=boraq_path)


def fix_prod_setup_perms(boraq_path=".", clairview_user=None):
	from glob import glob
	from boraq.boraq import Boraq

	clairview_user = clairview_user or Boraq(boraq_path).conf.get("clairview_user")

	if not clairview_user:
		print("clairview user not set")
		sys.exit(1)

	globs = ["logs/*", "config/*"]
	for glob_name in globs:
		for path in glob(glob_name):
			uid = pwd.getpwnam(clairview_user).pw_uid
			gid = grp.getgrnam(clairview_user).gr_gid
			os.chown(path, uid, gid)


def setup_fonts():
	fonts_path = os.path.join("/tmp", "fonts")

	if os.path.exists("/etc/fonts_backup"):
		return

	exec_cmd("git clone https://github.com/clairview/fonts.git", cwd="/tmp")
	os.rename("/etc/fonts", "/etc/fonts_backup")
	os.rename("/usr/share/fonts", "/usr/share/fonts_backup")
	os.rename(os.path.join(fonts_path, "etc_fonts"), "/etc/fonts")
	os.rename(os.path.join(fonts_path, "usr_share_fonts"), "/usr/share/fonts")
	shutil.rmtree(fonts_path)
	exec_cmd("fc-cache -fv")
