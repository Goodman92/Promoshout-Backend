from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from timezone_field import TimeZoneField


class User(AbstractBaseUser):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    avatar = models.ImageField(upload_to='images/profiles/', null=True, blank=True)

    objects = UserManager()

    country = CountryField()
    timezone = TimeZoneField()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

