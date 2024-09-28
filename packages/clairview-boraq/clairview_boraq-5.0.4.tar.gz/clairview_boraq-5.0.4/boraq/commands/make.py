# imports - third party imports
import click


@click.command("init", help="Initialize a new boraq instance in the specified path")
@click.argument("path")
@click.option(
	"--version",
	"--clairview-branch",
	"clairview_branch",
	default=None,
	help="Clone a particular branch of clairview",
)
@click.option(
	"--ignore-exist", is_flag=True, default=False, help="Ignore if Boraq instance exists."
)
@click.option(
	"--python", type=str, default="python3", help="Path to Python Executable."
)
@click.option(
	"--apps_path", default=None, help="path to json files with apps to install after init"
)
@click.option("--clairview-path", default=None, help="path to clairview repo")
@click.option("--clone-from", default=None, help="copy repos from path")
@click.option(
	"--clone-without-update", is_flag=True, help="copy repos from path without update"
)
@click.option("--no-procfile", is_flag=True, help="Do not create a Procfile")
@click.option(
	"--no-backups",
	is_flag=True,
	help="Do not set up automatic periodic backups for all sites on this boraq",
)
@click.option(
	"--skip-redis-config-generation",
	is_flag=True,
	help="Skip redis config generation if already specifying the common-site-config file",
)
@click.option("--skip-assets", is_flag=True, default=False, help="Do not build assets")
@click.option("--install-app", help="Install particular app after initialization")
@click.option("--verbose", is_flag=True, help="Verbose output during install")
@click.option(
	"--dev",
	is_flag=True,
	default=False,
	help="Enable developer mode and install development dependencies.",
)
def init(
	path,
	apps_path,
	clairview_path,
	clairview_branch,
	no_procfile,
	no_backups,
	clone_from,
	verbose,
	skip_redis_config_generation,
	clone_without_update,
	ignore_exist=False,
	skip_assets=False,
	python="python3",
	install_app=None,
	dev=False,
):
	import os

	from boraq.utils import log
	from boraq.utils.system import init

	if not ignore_exist and os.path.exists(path):
		log(f"Boraq instance already exists at {path}", level=2)
		return

	try:
		init(
			path,
			apps_path=apps_path,  # can be used from --config flag? Maybe config file could have more info?
			no_procfile=no_procfile,
			no_backups=no_backups,
			clairview_path=clairview_path,
			clairview_branch=clairview_branch,
			install_app=install_app,
			clone_from=clone_from,
			skip_redis_config_generation=skip_redis_config_generation,
			clone_without_update=clone_without_update,
			skip_assets=skip_assets,
			python=python,
			verbose=verbose,
			dev=dev,
		)
		log(f"Boraq {path} initialized", level=1)
	except SystemExit:
		raise
	except Exception:
		import shutil
		import time

		from boraq.utils import get_traceback

		# add a sleep here so that the traceback of other processes doesnt overlap with the prompts
		time.sleep(1)
		print(get_traceback())

		log(f"There was a problem while creating {path}", level=2)
		if click.confirm("Do you want to rollback these changes?", abort=True):
			log(f'Rolling back Boraq "{path}"')
			if os.path.exists(path):
				shutil.rmtree(path)


@click.command("drop")
@click.argument("path")
def drop(path):
	from boraq.boraq import Boraq
	from boraq.exceptions import BoraqNotFoundError, ValidationError

	boraq = Boraq(path)

	if not boraq.exists:
		raise BoraqNotFoundError(f"Boraq {boraq.name} does not exist")

	if boraq.sites:
		raise ValidationError("Cannot remove non-empty boraq directory")

	boraq.drop()

	print("Boraq dropped")


@click.command(
	["get", "get-app"],
	help="Clone an app from the internet or filesystem and set it up in your boraq",
)
@click.argument("name", nargs=-1)  # Dummy argument for backward compatibility
@click.argument("git-url")
@click.option("--branch", default=None, help="branch to checkout")
@click.option("--overwrite", is_flag=True, default=False)
@click.option("--skip-assets", is_flag=True, default=False, help="Do not build assets")
@click.option(
	"--soft-link",
	is_flag=True,
	default=False,
	help="Create a soft link to git repo instead of clone.",
)
@click.option(
	"--init-boraq", is_flag=True, default=False, help="Initialize Boraq if not in one"
)
@click.option(
	"--resolve-deps",
	is_flag=True,
	default=False,
	help="Resolve dependencies before installing app",
)
@click.option(
	"--cache-key",
	type=str,
	default=None,
	help="Caches get-app artifacts if provided (only first 10 chars is used)",
)
@click.option(
	"--compress-artifacts",
	is_flag=True,
	default=False,
	help="Whether to gzip get-app artifacts that are to be cached",
)
def get_app(
	git_url,
	branch,
	name=None,
	overwrite=False,
	skip_assets=False,
	soft_link=False,
	init_boraq=False,
	resolve_deps=False,
	cache_key=None,
	compress_artifacts=False,
):
	"clone an app from the internet and set it up in your boraq"
	from boraq.app import get_app

	get_app(
		git_url,
		branch=branch,
		skip_assets=skip_assets,
		overwrite=overwrite,
		soft_link=soft_link,
		init_boraq=init_boraq,
		resolve_deps=resolve_deps,
		cache_key=cache_key,
		compress_artifacts=compress_artifacts,
	)


@click.command("new-app", help="Create a new Clairview application under apps folder")
@click.option(
	"--no-git",
	is_flag=True,
	flag_value="--no-git",
	help="Do not initialize git repository for the app (available in Clairview v14+)",
)
@click.argument("app-name")
def new_app(app_name, no_git=None):
	from boraq.app import new_app

	new_app(app_name, no_git)


@click.command(
	["remove", "rm", "remove-app"],
	help=(
		"Completely remove app from boraq and re-build assets if not installed on any site"
	),
)
@click.option("--no-backup", is_flag=True, help="Do not backup app before removing")
@click.option("--force", is_flag=True, help="Force remove app")
@click.argument("app-name")
def remove_app(app_name, no_backup=False, force=False):
	from boraq.boraq import Boraq

	boraq = Boraq(".")
	boraq.uninstall(app_name, no_backup=no_backup, force=force)


@click.command("exclude-app", help="Exclude app from updating")
@click.argument("app_name")
def exclude_app_for_update(app_name):
	from boraq.app import add_to_excluded_apps_txt

	add_to_excluded_apps_txt(app_name)


@click.command("include-app", help="Include app for updating")
@click.argument("app_name")
def include_app_for_update(app_name):
	"Include app from updating"
	from boraq.app import remove_from_excluded_apps_txt

	remove_from_excluded_apps_txt(app_name)


@click.command(
	"pip",
	context_settings={"ignore_unknown_options": True, "help_option_names": []},
	help="For pip help use `boraq pip help [COMMAND]` or `boraq pip [COMMAND] -h`",
)
@click.argument("args", nargs=-1)
@click.pass_context
def pip(ctx, args):
	"Run pip commands in boraq env"
	import os

	from boraq.utils.boraq import get_env_cmd

	env_py = get_env_cmd("python")
	os.execv(env_py, (env_py, "-m", "pip") + args)


@click.command(
	"validate-dependencies",
	help="Validates that all requirements specified in clairview-dependencies are met curently.",
)
@click.pass_context
def validate_dependencies(ctx):
	"Validate all specified clairview-dependencies."
	from boraq.boraq import Boraq
	from boraq.app import App

	boraq = Boraq(".")

	for app_name in boraq.apps:
		app = App(app_name, boraq=boraq)
		app.validate_app_dependencies(throw=True)
