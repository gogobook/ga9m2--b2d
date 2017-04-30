"""
Sample user/profile models for testing.  These aren't enabled by default in the
sandbox
"""

from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, AbstractBaseUser)
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from oscar.core import compat
from oscar.apps.customer import abstract_models


class Profile(models.Model):
    """
    Dummy profile model used for testing
    """
    user = models.OneToOneField(compat.AUTH_USER_MODEL, related_name="profile",
                                on_delete=models.CASCADE)
    MALE, FEMALE = 'M', 'F'
    choices = (
        (MALE, 'Male'),
        (FEMALE, 'Female'))

    submitted_notifications = models.BooleanField(
        verbose_name=_('submitted notifications'),
        default=True,
        help_text=_("Receive notification when a page is submitted for moderation")
    )

    approved_notifications = models.BooleanField(
        verbose_name=_('approved notifications'),
        default=True,
        help_text=_("Receive notification when your page edit is approved")
    )

    rejected_notifications = models.BooleanField(
        verbose_name=_('rejected notifications'),
        default=True,
        help_text=_("Receive notification when your page edit is rejected")
    )

    preferred_language = models.CharField(
        verbose_name=_('preferred language'),
        max_length=10,
        help_text=_("Select language for the admin"),
        default=''
    )

    last_seen = models.DateTimeField(_("last seen"), auto_now=True)
    last_ip = models.GenericIPAddressField(_("last ip"), blank=True, null=True)
    timezone = models.CharField(_("time zone"), max_length=32, default='UTC')
    is_moderator = models.BooleanField(_('moderator status'), default=False)
    on_sale = models.BooleanField(_('on sale status'), default=False)
    is_verified = models.BooleanField(_('verified'), default=False,
                                      help_text=_('Designates whether the user has verified his '
                                                  'account by email or by other means. Un-select this '
                                                  'to let the user activate his account.'))
    phone_number_verified = models.BooleanField(_('phone number verified'), default=False,
                                      help_text=_('Designates whether the user has verified his '
                                                  'account by phone or by other means. Un-select this '
                                                  'to let the user activate his account.'))


    topic_count = models.PositiveIntegerField(_("topic count"), default=0)
    comment_count = models.PositiveIntegerField(_("comment count"), default=0)

    last_post_hash = models.CharField(_("last post hash"), max_length=32, blank=True)
    last_post_on = models.DateTimeField(_("last post on"), null=True, blank=True)


# A simple extension of the core User model for Django 1.5+
class ExtendedUserModel(AbstractUser):
    twitter_username = models.CharField(max_length=255, unique=True)


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        now = timezone.now()
        email = BaseUserManager.normalize_email(email)
        user = self.model(email=email, last_login=now)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        return self.create_user(email, password)

# A user model which doesn't extend AbstractUser
@python_2_unicode_compatible
class CustomUserModel(AbstractBaseUser):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    twitter_username = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    get_short_name = get_full_name

# A simple extension of the core Oscar User model
class ExtendedOscarUserModel(abstract_models.AbstractUser):
    twitter_username = models.CharField(max_length=255, unique=True)
