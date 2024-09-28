from boraq.config.common_site_config import get_config

from crontab import CronTab


def execute(boraq_path):
	"""
	This patch fixes a cron job that would backup sites every minute per 6 hours
	"""

	user = get_config(boraq_path=boraq_path).get("clairview_user")
	user_crontab = CronTab(user=user)
	for job in user_crontab.find_comment("boraq auto backups set for every 6 hours"):
		job.every(6).hours()
		user_crontab.write()
