from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from core import models

# Register your models here.

admin.site.site_header = 'Recipe-API'
admin.site.index_title = 'Admin Recipe-API'


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


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    '''register tag model to admin app'''
    list_display = ('name', 'user')
