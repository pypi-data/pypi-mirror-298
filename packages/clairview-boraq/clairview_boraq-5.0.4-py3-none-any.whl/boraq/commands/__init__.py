import click

# imports - module imports
from boraq.utils.cli import (
	MultiCommandGroup,
	print_boraq_version,
	use_experimental_feature,
	setup_verbosity,
)


@click.group(cls=MultiCommandGroup)
@click.option(
	"--version",
	is_flag=True,
	is_eager=True,
	callback=print_boraq_version,
	expose_value=False,
)
@click.option(
	"--use-feature",
	is_eager=True,
	callback=use_experimental_feature,
	expose_value=False,
)
@click.option(
	"-v",
	"--verbose",
	is_flag=True,
	callback=setup_verbosity,
	expose_value=False,
)
def boraq_command(boraq_path="."):
	import boraq

	boraq.set_clairview_version(boraq_path=boraq_path)


from boraq.commands.make import (
	drop,
	exclude_app_for_update,
	get_app,
	include_app_for_update,
	init,
	new_app,
	pip,
	remove_app,
	validate_dependencies,
)

boraq_command.add_command(init)
boraq_command.add_command(drop)
boraq_command.add_command(get_app)
boraq_command.add_command(new_app)
boraq_command.add_command(remove_app)
boraq_command.add_command(exclude_app_for_update)
boraq_command.add_command(include_app_for_update)
boraq_command.add_command(pip)
boraq_command.add_command(validate_dependencies)


from boraq.commands.update import (
	retry_upgrade,
	switch_to_branch,
	switch_to_develop,
	update,
)

boraq_command.add_command(update)
boraq_command.add_command(retry_upgrade)
boraq_command.add_command(switch_to_branch)
boraq_command.add_command(switch_to_develop)


from boraq.commands.utils import (
	app_cache_helper,
	backup_all_sites,
	boraq_src,
	disable_production,
	download_translations,
	find_boraqes,
	migrate_env,
	renew_lets_encrypt,
	restart,
	set_mariadb_host,
	set_nginx_port,
	set_redis_cache_host,
	set_redis_queue_host,
	set_redis_socketio_host,
	set_ssl_certificate,
	set_ssl_certificate_key,
	set_url_root,
	start,
)

boraq_command.add_command(start)
boraq_command.add_command(restart)
boraq_command.add_command(set_nginx_port)
boraq_command.add_command(set_ssl_certificate)
boraq_command.add_command(set_ssl_certificate_key)
boraq_command.add_command(set_url_root)
boraq_command.add_command(set_mariadb_host)
boraq_command.add_command(set_redis_cache_host)
boraq_command.add_command(set_redis_queue_host)
boraq_command.add_command(set_redis_socketio_host)
boraq_command.add_command(download_translations)
boraq_command.add_command(backup_all_sites)
boraq_command.add_command(renew_lets_encrypt)
boraq_command.add_command(disable_production)
boraq_command.add_command(boraq_src)
boraq_command.add_command(find_boraqes)
boraq_command.add_command(migrate_env)
boraq_command.add_command(app_cache_helper)

from boraq.commands.setup import setup

boraq_command.add_command(setup)


from boraq.commands.config import config

boraq_command.add_command(config)

from boraq.commands.git import remote_reset_url, remote_set_url, remote_urls

boraq_command.add_command(remote_set_url)
boraq_command.add_command(remote_reset_url)
boraq_command.add_command(remote_urls)

from boraq.commands.install import install

boraq_command.add_command(install)
