from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import UserCreationFormExtend


class UserAdminExtend(UserAdmin):
    add_form = UserCreationFormExtend
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


admin.site.unregister(User)
admin.site.register(User, UserAdminExtend)
