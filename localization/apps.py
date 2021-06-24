from django.apps import AppConfig
from .conf import settings as rosetta_settings

class LocalizationConfig(AppConfig):
    name = 'localization'

    def ready(self):
        from django.contrib import admin

        if rosetta_settings.SHOW_AT_ADMIN_PANEL:
            admin.site.index_template = 'rosetta/admin_index.html'

