from django.apps import AppConfig
from django.conf import settings


class DjangoCheckerConfig(AppConfig):
    name = "djangaudit"

    def ready(self):
        if not hasattr(settings, 'AUDIT_MAX_LINES_PER_FILE'):
            settings.AUDIT_MAX_LINES_PER_FILE = 500
