from django.contrib.auth.decorators import login_required

from pr1 import admin


@login_required
class StarterAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'role', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)


class SecondAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'role', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)

class newAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'role', 'is_staff', 'is_active')
    list_display = ('email', 'phone', 'role', 'is_staff', 'is_active')
    search_fields = ('email',)