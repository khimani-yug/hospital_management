

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('role','department')
        })
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Ward)
admin.site.register(Bed)
admin.site.register(Report)
admin.site.register(PatientsInformation)
admin.site.register(PatientHealthReport)

