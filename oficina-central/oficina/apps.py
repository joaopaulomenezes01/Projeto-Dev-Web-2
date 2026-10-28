from django.apps import AppConfig


class OficinaConfig(AppConfig):
    name = 'oficina'

    def ready(self):
        from . import signals  # noqa: F401