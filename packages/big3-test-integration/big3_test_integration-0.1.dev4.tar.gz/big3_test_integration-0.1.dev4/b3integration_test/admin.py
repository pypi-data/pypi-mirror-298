from big3_data_main_app.custom_admin import custom_admin_site
from django.contrib import admin

from .models import SettingsTestIntegration


@admin.register(SettingsTestIntegration, site=custom_admin_site)
class SettingsAdmin(admin.ModelAdmin):
    pass
