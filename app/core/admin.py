from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from core import models

# Register your models here.


@admin.register(models.AuthUser)
class AuthUserAdmin(UserAdmin):
    '''register and customise user admin page'''
    ordering = ('id',)
    list_display = ('email', 'name', 'is_active', 'is_staff')
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Personal Info'), {
            'fields': ('name',)
        }),
        (_('Permissions'), {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        (_('dates'), {
            'classes': ('collapse',),
            'fields': ('last_login',)
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2')
        }),
    )
