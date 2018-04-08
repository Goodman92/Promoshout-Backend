from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from Promoshout import settings


class ChannelManager(models.Manager):

    def retrieve_existing_channel_or_create(self, user, connection_name):
        try:
            channel = Channel.objects.get(name=connection_name)
        except ObjectDoesNotExist:
            channel = Channel.objects.create(user=user, name=connection_name)
        return channel


class Channel(models.Model):
    opened = models.DateTimeField(_('date joined'), auto_now_add=True)
    name = models.CharField(_('channel name'), max_length=1024)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = ChannelManager()

    class Meta:
        verbose_name = _('channel')
        verbose_name_plural = _('channels')

