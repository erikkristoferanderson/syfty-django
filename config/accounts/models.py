from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import secrets
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None):

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.username = email
        if password is None:
            user.set_unusable_password()
        user.save()

        return user

    def create_superuser(self, email=None, password=None, username=None):
        if username:
            email = username

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, default="")
    magic_token = models.CharField(max_length=255, null=True, blank=True)
    magic_token_expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def is_magic_link_valid(self):
        return self.magic_token is not None and self.magic_token_expires_at is not None and self.magic_token_expires_at > timezone.now()

    def send_magic_link(user):
        token = secrets.token_urlsafe(32)
        print('token', token)
        user.magic_token = token
        user.save()

        subject = 'Your magic login link'
        context = {'user': user,
                   'magic_link': f'{settings.BASE_URL}/accounts/validate-magic-link?magic_token={token}'}
        html_message = render_to_string('magic_link_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_FROM
        to_email = user.email

        send_mail(subject, plain_message, from_email, [
                  to_email], html_message=html_message)

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
