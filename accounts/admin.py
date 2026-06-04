from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('role', 'phone', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('role', 'phone', 'address', 'email')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)