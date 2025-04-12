from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Extended User model with additional security features"""
    email = models.EmailField(_('email address'), unique=True)
    email_verified = models.BooleanField(default=False)

    # For implementing account lockout
    login_attempts = models.IntegerField(default=0)
    last_login_attempt = models.DateTimeField(null=True, blank=True)
    account_locked_until = models.DateTimeField(null=True, blank=True)

    # For 2FA (basic implementation)
    two_factor_enabled = models.BooleanField(default=False)

    # Configure email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
