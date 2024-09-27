from boraq.config.common_site_config import update_config


def execute(boraq_path):
	update_config({"live_reload": True}, boraq_path)
