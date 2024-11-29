from django.apps import AppConfig


class BotAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot_admin'

    def ready(self):
        import bot_admin.signals
