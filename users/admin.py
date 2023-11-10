from django.contrib import admin

from users.models import CustomUser, FollowRequest, Follows
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

# Register your models here.
admin.site.register(CustomUser, UserAdmin)
admin.site.register(FollowRequest)
admin.site.register(Follows)
