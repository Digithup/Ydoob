from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        try:
            import apps.notis.signals
        except ImportError:
            pass
