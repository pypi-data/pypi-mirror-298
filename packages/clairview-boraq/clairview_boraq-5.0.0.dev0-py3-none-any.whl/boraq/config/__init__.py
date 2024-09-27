"""Module for setting up system and respective boraq configurations"""


def env():
	from jinja2 import Environment, PackageLoader

	return Environment(loader=PackageLoader("boraq.config"))
