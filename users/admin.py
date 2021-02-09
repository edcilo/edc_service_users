from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'phone', 'is_active',)
    list_display_links = ('pk', 'username', 'email')

    search_fields = (
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

    readonly_fields = ('date_joined', 'updated_at',)
