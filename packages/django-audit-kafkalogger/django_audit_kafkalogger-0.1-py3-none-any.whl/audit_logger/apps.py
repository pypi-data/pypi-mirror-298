from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .signals import register_all_audit_logs

class AuditLoggerConfig(AppConfig):
    name = 'audit_logger'

    def ready(self):
        # Automatically audit all models after migrations
        post_migrate.connect(register_all_audit_logs, sender=self)