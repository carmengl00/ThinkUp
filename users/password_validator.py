from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils.translation import ngettext

class PasswordValidator:
    def __init__(self, passwords=None):
        self.passwords = passwords or []

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("This password is too common."),
                code="password_too_common",
            )

        if password.isdigit():
            raise ValidationError(
                _("This password is entirely numeric."),
                code="password_entirely_numeric",
            )

        if len(password) < 8:
            raise ValidationError(
                ngettext(
                    "This password is too short. It must contain at least "
                    "8 character.",
                    "This password is too short. It must contain at least "
                    "8 characters.",
                    8,
                ),
                code="password_too_short",
                params={"min_length": 8},
            )
