from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'phone', 'is_active',)
    list_display_links = ('pk', 'username', 'email')

    search_fields = (
        'uuid',
        'email',
        'username',
        'first_name',
        'last_name',
    )

    list_filter = (
        'is_active',
        'is_staff',
        'date_joined',
        'updated_at',
        'deleted_at',
    )

    readonly_fields = ('uuid', 'password',)

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

    fieldsets = (
        (None, {'fields': ('uuid', 'username', 'password',)}),
        ('User info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'metadata')}),
        ('Account', {'fields': ('confirmed', 'confirmed_at', 'date_joined', 'updated_at', 'last_login',)}),
        ('Warning', {'fields': ('is_active', 'deleted_at'), 'classes': ('collapse',)}),
        ('Django ACL', {'fields': ('is_staff', 'is_superuser', 'user_permissions',), 'classes': ('collapse',)})
    )
