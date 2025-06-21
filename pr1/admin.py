from django.contrib import admin

from pr1.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('-date_joined',)