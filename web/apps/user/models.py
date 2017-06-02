"""
Sample user/profile models for testing.  These aren't enabled by default in the
sandbox
僅用於測試，sandbox 預設不啟用?
"""
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _

# ~~from oscar.core import compat # 這裡其實指向'auth.user'，以至於會跟 oscar.user不相容。~~
# oscar 有用一個機制，不會不相容
from django.contrib.auth.models import Permission
from oscar.apps.customer.abstract_models import AbstractUser, UserManager # 如果使用 oscar的 AbstractUser, 則會報要有

from oscar.core.loading import get_model

Partner = get_model('partner', 'Partner')

class MyUserManager(UserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and
        password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(
            email=email, is_staff=False, is_active=True,
            is_superuser=False,
            last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        be_a_partner = Partner(name=user.email)
        be_a_partner.save()
        be_a_partner.users.add(user)
        if not user.is_staff:
            dashboard_access_perm = Permission.objects.get(
                codename='dashboard_access',
                content_type__app_label='partner')
            user.user_permissions.add(dashboard_access_perm)
        return user

class Profile(AbstractUser):
    """
    Dummy profile model used for testing
    """
    phone_number = PhoneNumberField(blank=True)
    fax_number = PhoneNumberField(blank=True)
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

    objects = MyUserManager()



