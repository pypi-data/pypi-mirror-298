VERSION = "5.0.4"
PROJECT_NAME = "clairview-boraq"
CLAIRVIEW_VERSION = None
current_path = None
updated_path = None
LOG_BUFFER = []


def set_clairview_version(boraq_path="."):
	from .utils.app import get_current_clairview_version

	global CLAIRVIEW_VERSION
	if not CLAIRVIEW_VERSION:
		CLAIRVIEW_VERSION = get_current_clairview_version(boraq_path=boraq_path)
