# imports - standard imports
import getpass
import os

# imports - third partyimports
import click

# imports - module imports
import boraq
from boraq.app import use_rq
from boraq.boraq import Boraq
from boraq.config.common_site_config import (
	get_gunicorn_workers,
	update_config,
	get_default_max_requests,
	compute_max_requests_jitter,
)
from boraq.utils import exec_cmd, which, get_boraq_name


def generate_systemd_config(
	boraq_path,
	user=None,
	yes=False,
	stop=False,
	create_symlinks=False,
	delete_symlinks=False,
):

	if not user:
		user = getpass.getuser()

	config = Boraq(boraq_path).conf

	boraq_dir = os.path.abspath(boraq_path)
	boraq_name = get_boraq_name(boraq_path)

	if stop:
		exec_cmd(
			f"sudo systemctl stop -- $(systemctl show -p Requires {boraq_name}.target | cut -d= -f2)"
		)
		return

	if create_symlinks:
		_create_symlinks(boraq_path)
		return

	if delete_symlinks:
		_delete_symlinks(boraq_path)
		return

	number_of_workers = config.get("background_workers") or 1
	background_workers = []
	for i in range(number_of_workers):
		background_workers.append(
			get_boraq_name(boraq_path) + "-clairview-default-worker@" + str(i + 1) + ".service"
		)

	for i in range(number_of_workers):
		background_workers.append(
			get_boraq_name(boraq_path) + "-clairview-short-worker@" + str(i + 1) + ".service"
		)

	for i in range(number_of_workers):
		background_workers.append(
			get_boraq_name(boraq_path) + "-clairview-long-worker@" + str(i + 1) + ".service"
		)

	web_worker_count = config.get(
		"gunicorn_workers", get_gunicorn_workers()["gunicorn_workers"]
	)
	max_requests = config.get(
		"gunicorn_max_requests", get_default_max_requests(web_worker_count)
	)

	boraq_info = {
		"boraq_dir": boraq_dir,
		"sites_dir": os.path.join(boraq_dir, "sites"),
		"user": user,
		"use_rq": use_rq(boraq_path),
		"http_timeout": config.get("http_timeout", 120),
		"redis_server": which("redis-server"),
		"node": which("node") or which("nodejs"),
		"redis_cache_config": os.path.join(boraq_dir, "config", "redis_cache.conf"),
		"redis_queue_config": os.path.join(boraq_dir, "config", "redis_queue.conf"),
		"webserver_port": config.get("webserver_port", 8000),
		"gunicorn_workers": web_worker_count,
		"gunicorn_max_requests": max_requests,
		"gunicorn_max_requests_jitter": compute_max_requests_jitter(max_requests),
		"boraq_name": get_boraq_name(boraq_path),
		"worker_target_wants": " ".join(background_workers),
		"boraq_cmd": which("boraq"),
	}

	if not yes:
		click.confirm(
			"current systemd configuration will be overwritten. Do you want to continue?",
			abort=True,
		)

	setup_systemd_directory(boraq_path)
	setup_main_config(boraq_info, boraq_path)
	setup_workers_config(boraq_info, boraq_path)
	setup_web_config(boraq_info, boraq_path)
	setup_redis_config(boraq_info, boraq_path)

	update_config({"restart_systemd_on_update": False}, boraq_path=boraq_path)
	update_config({"restart_supervisor_on_update": False}, boraq_path=boraq_path)


def setup_systemd_directory(boraq_path):
	if not os.path.exists(os.path.join(boraq_path, "config", "systemd")):
		os.makedirs(os.path.join(boraq_path, "config", "systemd"))


def setup_main_config(boraq_info, boraq_path):
	# Main config
	boraq_template = boraq.config.env().get_template("systemd/clairview-boraq.target")
	boraq_config = boraq_template.render(**boraq_info)
	boraq_config_path = os.path.join(
		boraq_path, "config", "systemd", boraq_info.get("boraq_name") + ".target"
	)

	with open(boraq_config_path, "w") as f:
		f.write(boraq_config)


def setup_workers_config(boraq_info, boraq_path):
	# Worker Group
	boraq_workers_target_template = boraq.config.env().get_template(
		"systemd/clairview-boraq-workers.target"
	)
	boraq_default_worker_template = boraq.config.env().get_template(
		"systemd/clairview-boraq-clairview-default-worker.service"
	)
	boraq_short_worker_template = boraq.config.env().get_template(
		"systemd/clairview-boraq-clairview-short-worker.service"
	)
	boraq_long_worker_template = boraq.config.env().get_template(
		"systemd/clairview-boraq-clairview-long-worker.service"
	)
	boraq_schedule_worker_template = boraq.config.env().get_template(
		"systemd/clairview-boraq-clairview-schedule.service"
	)

	boraq_workers_target_config = boraq_workers_target_template.render(**boraq_info)
	boraq_default_worker_config = boraq_default_worker_template.render(**boraq_info)
	boraq_short_worker_config = boraq_short_worker_template.render(**boraq_info)
	boraq_long_worker_config = boraq_long_worker_template.render(**boraq_info)
	boraq_schedule_worker_config = boraq_schedule_worker_template.render(**boraq_info)

	boraq_workers_target_config_path = os.path.join(
		boraq_path, "config", "systemd", boraq_info.get("boraq_name") + "-workers.target"
	)
	boraq_default_worker_config_path = os.path.join(
		boraq_path,
		"config",
		"systemd",
		boraq_info.get("boraq_name") + "-clairview-default-worker@.service",
	)
	boraq_short_worker_config_path = os.path.join(
		boraq_path,
		"config",
		"systemd",
		boraq_info.get("boraq_name") + "-clairview-short-worker@.service",
	)
	boraq_long_worker_config_path = os.path.join(
		boraq_path,
		"config",
		"systemd",
		boraq_info.get("boraq_name") + "-clairview-long-worker@.service",
	)
	boraq_schedule_worker_config_path = os.path.join(
		boraq_path,
		"config",
		"systemd",
		boraq_info.get("boraq_name") + "-clairview-schedule.service",
	)

	with open(boraq_workers_target_config_path, "w") as f:
		f.write(boraq_workers_target_config)

	with open(boraq_default_worker_config_path, "w") as f:
		f.write(boraq_default_worker_config)

	with open(boraq_short_worker_config_path, "w") as f:
		f.write(boraq_short_worker_config)

	with open(boraq_long_worker_config_path, "w") as f:
		f.write(boraq_long_worker_config)

	with open(boraq_schedule_worker_config_path, "w") as f:
		f.write(boraq_schedule_worker_config)


def setup_web_config(boraq_info, boraq_path):
	# Web Group
	boraq_web_target_template = boraq.config.env().get_template(
		"systemd/clairview-boraq-web.target"
	)
	boraq_web_service_template = boraq.config.env().get_template(
		"systemd/clairview-boraq-clairview-web.service"
	)
	boraq_node_socketio_template = boraq.config.env().get_template(
		"systemd/clairview-boraq-node-socketio.service"
	)

	boraq_web_target_config = boraq_web_target_template.render(**boraq_info)
	boraq_web_service_config = boraq_web_service_template.render(**boraq_info)
	boraq_node_socketio_config = boraq_node_socketio_template.render(**boraq_info)

	boraq_web_target_config_path = os.path.join(
		boraq_path, "config", "systemd", boraq_info.get("boraq_name") + "-web.target"
	)
	boraq_web_service_config_path = os.path.join(
		boraq_path, "config", "systemd", boraq_info.get("boraq_name") + "-clairview-web.service"
	)
	boraq_node_socketio_config_path = os.path.join(
		boraq_path,
		"config",
		"systemd",
		boraq_info.get("boraq_name") + "-node-socketio.service",
	)

	with open(boraq_web_target_config_path, "w") as f:
		f.write(boraq_web_target_config)

	with open(boraq_web_service_config_path, "w") as f:
		f.write(boraq_web_service_config)

	with open(boraq_node_socketio_config_path, "w") as f:
		f.write(boraq_node_socketio_config)


def setup_redis_config(boraq_info, boraq_path):
	# Redis Group
	boraq_redis_target_template = boraq.config.env().get_template(
		"systemd/clairview-boraq-redis.target"
	)
	boraq_redis_cache_template = boraq.config.env().get_template(
		"systemd/clairview-boraq-redis-cache.service"
	)
	boraq_redis_queue_template = boraq.config.env().get_template(
		"systemd/clairview-boraq-redis-queue.service"
	)

	boraq_redis_target_config = boraq_redis_target_template.render(**boraq_info)
	boraq_redis_cache_config = boraq_redis_cache_template.render(**boraq_info)
	boraq_redis_queue_config = boraq_redis_queue_template.render(**boraq_info)

	boraq_redis_target_config_path = os.path.join(
		boraq_path, "config", "systemd", boraq_info.get("boraq_name") + "-redis.target"
	)
	boraq_redis_cache_config_path = os.path.join(
		boraq_path, "config", "systemd", boraq_info.get("boraq_name") + "-redis-cache.service"
	)
	boraq_redis_queue_config_path = os.path.join(
		boraq_path, "config", "systemd", boraq_info.get("boraq_name") + "-redis-queue.service"
	)

	with open(boraq_redis_target_config_path, "w") as f:
		f.write(boraq_redis_target_config)

	with open(boraq_redis_cache_config_path, "w") as f:
		f.write(boraq_redis_cache_config)

	with open(boraq_redis_queue_config_path, "w") as f:
		f.write(boraq_redis_queue_config)


def _create_symlinks(boraq_path):
	boraq_dir = os.path.abspath(boraq_path)
	etc_systemd_system = os.path.join("/", "etc", "systemd", "system")
	config_path = os.path.join(boraq_dir, "config", "systemd")
	unit_files = get_unit_files(boraq_dir)
	for unit_file in unit_files:
		filename = "".join(unit_file)
		exec_cmd(
			f'sudo ln -s {config_path}/{filename} {etc_systemd_system}/{"".join(unit_file)}'
		)
	exec_cmd("sudo systemctl daemon-reload")


def _delete_symlinks(boraq_path):
	boraq_dir = os.path.abspath(boraq_path)
	etc_systemd_system = os.path.join("/", "etc", "systemd", "system")
	unit_files = get_unit_files(boraq_dir)
	for unit_file in unit_files:
		exec_cmd(f'sudo rm {etc_systemd_system}/{"".join(unit_file)}')
	exec_cmd("sudo systemctl daemon-reload")


def get_unit_files(boraq_path):
	boraq_name = get_boraq_name(boraq_path)
	unit_files = [
		[boraq_name, ".target"],
		[boraq_name + "-workers", ".target"],
		[boraq_name + "-web", ".target"],
		[boraq_name + "-redis", ".target"],
		[boraq_name + "-clairview-default-worker@", ".service"],
		[boraq_name + "-clairview-short-worker@", ".service"],
		[boraq_name + "-clairview-long-worker@", ".service"],
		[boraq_name + "-clairview-schedule", ".service"],
		[boraq_name + "-clairview-web", ".service"],
		[boraq_name + "-node-socketio", ".service"],
		[boraq_name + "-redis-cache", ".service"],
		[boraq_name + "-redis-queue", ".service"],
	]
	return unit_files
