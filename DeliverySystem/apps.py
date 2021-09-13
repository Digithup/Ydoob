from django.apps import AppConfig


class DeliverySystemConfig(AppConfig):
    name = 'DeliverySystem'

    def ready(self):
        import core.signals
