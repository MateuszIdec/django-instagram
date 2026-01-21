# apps.py
from django.apps import AppConfig
from django.contrib.auth import get_user_model

class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        User = get_user_model()
        if not User.objects.filter(username="testUser").exists():
            user = User.objects.create_user(
                username="testUser",
                email="test@email.com",
                password="test123",
            )