class InvalidBranchException(Exception):
	pass


class InvalidRemoteException(Exception):
	pass


class PatchError(Exception):
	pass


class CommandFailedError(Exception):
	pass


class BoraqNotFoundError(Exception):
	pass


class ValidationError(Exception):
	pass


class AppNotInstalledError(ValidationError):
	pass


class CannotUpdateReleaseBoraq(ValidationError):
	pass


class FeatureDoesNotExistError(CommandFailedError):
	pass


class NotInBoraqDirectoryError(Exception):
	pass


class VersionNotFound(Exception):
	pass
