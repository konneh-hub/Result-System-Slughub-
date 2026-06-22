from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        # Ensure model signals are registered when the users app is loaded.
        import apps.users.signals  # noqa: F401
