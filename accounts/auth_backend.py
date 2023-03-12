from django.contrib.auth.backends import ModelBackend
from .models import CustomUser


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """

    def authenticate(self, email=None):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
