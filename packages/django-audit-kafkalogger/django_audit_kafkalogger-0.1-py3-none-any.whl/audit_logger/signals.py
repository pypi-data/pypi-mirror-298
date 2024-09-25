from django.apps import apps
from .logger import AuditLogger

def register_all_audit_logs(sender, **kwargs):
    """Registers audit logs for all models in the system."""
    all_models = apps.get_models()

    for model in all_models:
        # Automatically register for log auditing
        AuditLogger.register_auditoria_logs(model)

        # You can skip registering models for config auditing here.
