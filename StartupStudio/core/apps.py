from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    def ready(self):
        from django.db.models.signals import post_save
        from django.conf import settings
        from core.signals.handlers import add_to_default_group
        post_save.connect(add_to_default_group, sender=settings.AUTH_USER_MODEL)

