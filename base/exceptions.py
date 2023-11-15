from django.utils.translation import gettext_lazy as _


class JSONWebTokenError(Exception):
    default_message = ""

    def __init__(self, message=""):
        if len(message) == 0:
            message = self.default_message

        super().__init__(message)


class PermissionDenied(JSONWebTokenError):
    default_message = _("You do not have permission to perform this action")

