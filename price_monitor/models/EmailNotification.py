from .mixins.PublicIDMixin import PublicIDMixin

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy

from six import text_type


class EmailNotification(PublicIDMixin, models.Model):
    """
    An email notification.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Owner'))
    email = models.EmailField(verbose_name=_('Email address'))

    def __str__(self):
        """
        Returns the unicode representation of the EmailNotification.
        :return: the unicode representation
        :rtype: unicode
        """
        return text_type(
            ' %(email)s' % {
                'email': self.email,
            }
        )

    class Meta:
        app_label = 'price_monitor'
        verbose_name = ugettext_lazy('Email Notification')
        verbose_name_plural = ugettext_lazy('Email Notifications')
        ordering = ('email', )
