from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, GSIToken


class GSITokenInline(admin.StackedInline):
    model = GSIToken
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [
        GSITokenInline,
    ]
    list_display = (
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'gsi_token', )
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
